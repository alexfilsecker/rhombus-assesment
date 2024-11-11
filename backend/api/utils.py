import time
from typing import Dict, List, Tuple

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .models.generic_data_model import GenericData
from .models.table_col_model import TableCol
from .serializers.generic_data_serializer import GenericDataSerializer
from .serializers.table_col_serializer import TableColSerializer


def get_force_casting(req: Request) -> Dict[str, str]:
    force_casting: Dict[str, str] = {}
    for key, value in req.data.items():
        if key != "file":
            column = key[len("cast-col-") :]
            force_casting[column] = value

    return force_casting


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Function {func.__name__} took {(end_time - start_time)*1000:.4f} ms to execute."
        )
        return result

    return wrapper


def error400(message: str) -> Response:
    """A simple function to return a 400 error response.

    Args:
        message (str): The message to return in the response.

    Returns:
        response (Response): The response with the error message and status code 400.
    """
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


@timer
# VERY VERY HEAVY FUNCTION, around .7 ms for data.
def validate(data):
    GenericDataSerializer(None, data=data).is_valid(raise_exception=True)


# All the keys of the GenericData model to represent data.
ALL_KEYS = {
    "string_value",
    "int_sign_value",
    "uint_value",
    "double_value",
    "double_imag_value",
    "datetime_value",
    "time_zone_info_value",
    "bool_value",
}


@transaction.atomic
@timer
def create_data(
    file_id: str, df: pd.DataFrame
) -> Tuple[List[GenericData], List[TableCol]]:
    """
    An atomic operation to create all data in the database to represent the file.

    Args:
        file_id (str): The pregenerated id of the file.
        df (DataFrame): The DataFrame to create the data from.

    Raises:
        ValidationError: When the data creation fails by any means.

    Returns:
        Tuple: A tuple containing:
            - generic_data (List[GenericData]): The list of all created data from the file cells.
            - table_cols (List[TableCol]): The list of all created columns.
    """
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
                elif dtype.startswith("float"):
                    data["double_value"] = value
                elif dtype.startswith("complex"):
                    value: complex
                    data["double_value"] = value.real
                    data["double_imag_value"] = value.imag
                elif dtype == "datetime64[ns]":
                    data["datetime_value"] = value
                elif dtype == "category":
                    value: str
                    data["string_value"] = value
                elif dtype == "timedelta64[ns]":
                    value: pd.Timedelta
                    data["uint_value"] = value.value

                # validate(data)  # Too time expensive function

                data["column"] = table_col
                generic_data.append(GenericData(**data))

        generic_data = GenericData.objects.bulk_create(generic_data)
        return generic_data, table_cols

    except Exception as e:
        raise ValidationError(f"Failed to create data. {str(e)}")
