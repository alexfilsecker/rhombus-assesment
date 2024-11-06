import time
from typing import List, Tuple

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction

from .models.generic_data_model import GenericData
from .models.table_col_model import TableCol
from .serializers.generic_data_serializer import GenericDataSerializer
from .serializers.table_col_serializer import TableColSerializer

ALL_KEYS = {
    "string_value",
    "int_sign_value",
    "uint_value",
    "double_value",
    "datetime_value",
    "time_zone_info_value",
    "bool_value",
}


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


@timer
# VERY VERY HEAVY FUNCTION, around .7 ms for data.
def validate(data):
    GenericDataSerializer(None, data=data).is_valid(raise_exception=True)


@transaction.atomic
@timer
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
                elif dtype.startswith("float"):
                    data["double_value"] = value
                elif dtype == "datetime64[ns]":
                    data["datetime_value"] = value
                elif dtype == "category":
                    data["string_value"] = value

                data["column"] = table_col
                generic_data.append(GenericData(**data))

        generic_data = GenericData.objects.bulk_create(generic_data)
        return generic_data, table_cols

    except Exception as e:
        raise ValidationError(f"Failed to create data. {str(e)}")
