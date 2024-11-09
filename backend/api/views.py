from io import BytesIO
from time import time
from typing import Any, List

import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Case, When
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models.generic_data_model import GenericData
from .models.table_col_model import TableCol
from .scripts.infer_data_types import infer_and_convert_data_types
from .serializers.generic_data_serializer import GenericDataSerializer
from .serializers.get_data_serializer import GetDataSerializer
from .serializers.table_col_serializer import TableColSerializer
from .utils import create_data, get_force_casting


def error400(message: str):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


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

    # Get force casting options
    force_casting = get_force_casting(req)

    # Process the data frame
    df, errors = infer_and_convert_data_types(df, force_casting)

    # Create a unique identifier
    file_id = f"{name}-{int(time() * 100)}.{extension}"

    # Save data into db
    create_data(file_id, df)

    # file_id can later be used to retrieve the data
    return Response({"file_id": file_id, "errors": errors})


@api_view(["GET"])
def get_data(request: Request):


    # Get the request and ensure it is valid
    serialized_request = GetDataSerializer(data=request.query_params)
    serialized_request.is_valid(raise_exception=True)

    # Get parameters from request_query
    request_query = serialized_request.data
    file_id = request_query["file_id"]
    page_size = request_query["page_size"]
    page = request_query["page"]
    sort_by = request_query["sort_by"]

    # Get the tables associated with the file
    table_cols_models = TableCol.objects.filter(file_id=file_id)
    cols = TableColSerializer(list(table_cols_models)).data

    # Get all data from those columns
    filtered_data_models = GenericData.get_objects_by_columns(cols)

    # count the total ammount of data
    total_filtered_models = filtered_data_models.count()

    # If we sort by row_index, there is no need to do crazy shit

    if sort_by == "row_index":
        sorted_data_models = GenericData.slice_and_sort_by_row(
            filtered_data_models, cols, request_query
        )
        rows = GenericDataSerializer(
            list(sorted_data_models), num_of_cols=len(cols)
        ).data["rows"]

    else:
        sorted_sliced_col_data_models = GenericData.slice_and_sort_by_col(
            filtered_data_models, cols, request_query
        )

        sorted_row_indexes = [
            GenericDataSerializer(col_data_model).data["row_index"]
            for col_data_model in sorted_sliced_col_data_models
        ]

        row_filtered_data_models = filtered_data_models.filter(
            row__in=sorted_row_indexes
        )
        rows = GenericDataSerializer(
            list(row_filtered_data_models), row_order=sorted_row_indexes
        ).data["rows"]

    # Cleanup internal ids
    for _, col in cols.items():
        col.pop("id")

    return Response(
        {
            "cols": cols,
            "rows": rows,
            "total_rows": int(total_filtered_models / len(cols)),
            "page": page,
            "page_size": page_size,
        }
    )
