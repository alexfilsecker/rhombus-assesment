from io import BytesIO
from time import time
from typing import List, Tuple, Dict, Any, Union

import pandas as pd
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import GenericData, TableCol
from .scripts.infer_data_types import infer_and_convert_data_types
from .serializers import ALL_KEYS, GenericDataSerializer, TableColSerializer


def error400(message: str):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


@transaction.atomic
def create_data(
    file_id: str, df: pd.DataFrame
) -> Tuple[List[GenericData], List[TableCol]]:
    try:
        generic_data: List[GenericData] = []
        table_cols: List[TableCol] = []
        for col_index, col in enumerate(df.columns):
            table_col_serializer = TableColSerializer(
                data={
                    "file_id": file_id,
                    "col_name": col,
                    "col_type": df[col].dtype,
                    "col_index": col_index,
                }
            )

            # Check that the col has been created correctly
            table_col_serializer.is_valid(raise_exception=True)
            table_col = table_col_serializer.save()
            table_cols.append(table_col)

            for row_index, value in enumerate(df[col]):

                data = {
                    "column": table_col.id,
                    "row": row_index,
                    **{key: None for key in ALL_KEYS},
                }

                dtype: str = table_col.col_type
                if dtype == "object":
                    data["string_value"] = value
                elif dtype.startswith("uint"):
                    data["uint_value"] = value
                elif dtype.startswith("int"):
                    data["uint_value"] = abs(value)
                    data["int_sign_value"] = 1 if value >= 0 else -1

                generic_data_serializer = GenericDataSerializer(data=data)
                generic_data_serializer.is_valid(raise_exception=True)
                generic_data.append(
                    GenericData(**generic_data_serializer.validated_data)
                )

        generic_data = GenericData.objects.bulk_create(generic_data)
        return generic_data, table_cols

    except Exception as e:
        raise ValidationError(f"Failed to create data. {str(e)}")


def printlist(list):
    for i in list:
        print(i)


@api_view(["POST"])
def process_file(req: Request) -> Response:

    file = req.FILES.get("file")

    # Ensure file exists
    if type(file) != InMemoryUploadedFile:
        return error400("no file uploaded")

    # Ensure file has correct naming
    if file.name.count(".") != 1:
        return error400("Incorrect file name")

    # Ensure file has a correct extension
    name, extension = file.name.split(".")
    if extension not in ["csv", "xslx"]:
        return error400(f"Extension '.{extension}' not supported")

    # Create the pandas dataframe
    readable = BytesIO(file.read())
    if extension == "csv":
        df = pd.read_csv(readable)
    else:
        df = pd.read_excel(readable)

    # Process the data frame
    df = infer_and_convert_data_types(df)

    # Create a unique identifier
    file_id = f"{name}-{int(time() * 100)}.{extension}"

    # Save data into db
    generic_data_models, table_col_models = create_data(file_id, df)

    # serialize the saved data
    cols = {}
    for table_col_model in table_col_models:
        table_col = TableColSerializer(table_col_model).data
        cols[table_col["col_name"]] = table_col

    num_of_cols = len(cols)
    num_of_rows = int(len(generic_data_models) / num_of_cols)

    rows: List[Dict[str, Any]] = [{"values": {}} for _ in range(num_of_rows)]
    for generic_data_model in generic_data_models:
        serialized_generic_data = GenericDataSerializer(generic_data_model).data

        row_index = serialized_generic_data["row_index"]
        col_name = serialized_generic_data["col_name"]
        value = serialized_generic_data["value"]

        if "row_index" not in rows[row_index]:
            rows[row_index]["row_index"] = row_index

        rows[row_index]["values"][col_name] = value

    return Response(
        {
            "file_id": file_id,  # file_id can later be used to retrieve the data
            "cols": cols,
            "rows": rows,
        }
    )
