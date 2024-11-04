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

                print("\nDATA")
                print(data)

                generic_data_serializer = GenericDataSerializer(None, data=data)
                generic_data_serializer.is_valid(raise_exception=True)
                generic_data.append(
                    GenericData(**generic_data_serializer.validated_data)
                )

        generic_data = GenericData.objects.bulk_create(generic_data)
        return generic_data, table_cols

    except Exception as e:
        raise ValidationError(f"Failed to create data. {str(e)}")
