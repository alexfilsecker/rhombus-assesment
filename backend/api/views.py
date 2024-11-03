from io import BytesIO
from time import time
from typing import Any, List

import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
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
from .utils import create_data


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

    # Process the data frame
    df = infer_and_convert_data_types(df)

    # Create a unique identifier
    file_id = f"{name}-{int(time() * 100)}.{extension}"

    # Save data into db
    create_data(file_id, df)

    # file_id can later be used to retrieve the data
    return Response({"file_id": file_id})


def printlist(l: List[Any]):
    for i in l:
        print(i)


@api_view(["GET"])
def get_data(request: Request):

    print("\n--- GET DATA ---\n")

    # Get the request and ensure it is valid
    serialized_request = GetDataSerializer(data=request.query_params)
    serialized_request.is_valid(raise_exception=True)

    request_query = serialized_request.data
    file_id = request_query["file_id"]

    page_size = request_query["page_size"]
    page = request_query["page"]

    sort_by = request_query["sort_by"]

    print(sort_by)

    if sort_by == "row_index":
        order_by = "row"

    order_by = "row"

    table_cols_models = TableCol.objects.filter(file_id=file_id)
    cols = TableColSerializer(list(table_cols_models)).data

    filtered_data_models = GenericData.get_objects_by_columns(cols)

    total_filtered_models = filtered_data_models.count()

    sorted_col_models = GenericData.get_sliced_sorted_cols(
        filtered_data_models, cols, request_query
    )

    rows_order = [
        GenericDataSerializer(model).data["row_index"] for model in sorted_col_models
    ]

    rows = GenericDataSerializer(
        list(filtered_data_models),
        num_of_rows=int(len(filtered_data_models) / len(cols)),
        starting_row=page * page_size,
    ).data

    # CleanUp internal ids
    for _, col in cols.items():
        col.pop("id")

    return Response(
        {
            "cols": cols,
            **rows,
            "total_rows": int(total_filtered_models / len(cols)),
            "page": page,
            "page_size": page_size,
        }
    )
