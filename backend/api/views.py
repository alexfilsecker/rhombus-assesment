from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from time import time
import pandas as pd
from io import BytesIO
from .scripts.infer_data_types import infer_and_convert_data_types
from .serializers import GenericDataSerializer


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
    _, extension = file.name.split(".")
    if extension not in ["csv", "xslx"]:
        return error400(f"Extension '.{extension}' not supported")

    # Create the pandas dataframe
    readable = BytesIO(file.read())
    if extension == "csv":
        df = pd.read_csv(readable)
    else:
        df = pd.read_excel(readable)

    # infer data types and transform it
    df = infer_and_convert_data_types(df)

    return Response({"message": "done"})
