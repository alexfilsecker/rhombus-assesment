from rest_framework import serializers
from .models import GenericData, TableCol, IMPORTANT_KEYS_BY_DTYPE
from typing import Dict, Any, Optional, Set, Union, List
import numpy as np
from django.core.exceptions import ValidationError


ALL_KEYS = {
    "string_value",
    "int_sign_value",
    "uint_value",
    "double_value",
    "datetime_value",
    "time_zone_info_value",
    "bool_value",
}


class GenericDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.starting_row = 0
        if "num_of_rows" in kwargs:
            self.num_of_rows = kwargs.pop("num_of_rows")
            self.starting_row = kwargs.pop("starting_row")
            return super().__init__(*args, **kwargs)

        return super().__init__(*args, **kwargs)

    def validate_nones(self, values: Dict[str, Any], important_keys: Set[str]) -> None:
        for key, value in values.items():
            if key in {"row", "column"}:
                continue

            if key in important_keys:
                if value is None:
                    raise serializers.ValidationError(f"{key} cannot be None")
            else:
                if value is not None:
                    raise serializers.ValidationError(f"{key} must be set to None")

    def validate(self, values: Dict[str, Any]):
        dtype = values["column"].col_type
        self.validate_nones(values, IMPORTANT_KEYS_BY_DTYPE[dtype])
        return values

    def to_representation(self, instance: Union[GenericData, List[GenericData]]):
        def one_representation(instance: GenericData):
            dtype: str = instance.column.col_type
            data = {
                "row_index": instance.row,
                "col_name": instance.column.col_name,
            }

            if dtype == "object":
                value = instance.string_value
            elif dtype.startswith("uint"):
                uint_map = {
                    "uint8": np.uint8(instance.uint_value),
                    "uint16": np.uint16(instance.uint_value),
                    "uint32": np.uint32(instance.uint_value),
                    "uint64": np.uint64(instance.uint_value),
                }
                if dtype not in uint_map:
                    raise ValidationError(f"{dtype} not supported in serializer")

                value = uint_map[dtype]

            elif dtype.startswith("int"):
                int_map = {
                    "int8": np.int8(instance.uint_value * instance.int_sign_value),
                    "int16": np.int16(instance.uint_value * instance.int_sign_value),
                    "int32": np.int32(instance.uint_value * instance.int_sign_value),
                    "int64": np.int64(instance.uint_value * instance.int_sign_value),
                }
                if dtype not in int_map:
                    raise ValidationError(f"{dtype} not supported in serializer")

                value = int_map[dtype]

            else:
                raise ValidationError("SHOULDN'T BE HERE")

            return {**data, "value": value}

        if not isinstance(instance, list):
            return one_representation(instance)

        rows: List[Dict[str, Any]] = [{"values": {}} for _ in range(self.num_of_rows)]
        for generic_data_model in instance:
            serialized_generic_data = GenericDataSerializer(generic_data_model).data

            row_index = serialized_generic_data["row_index"]
            col_name = serialized_generic_data["col_name"]
            value = serialized_generic_data["value"]

            if "row_index" not in rows[row_index - self.starting_row]:
                rows[row_index - self.starting_row]["row_index"] = row_index

            rows[row_index - self.starting_row]["values"][col_name] = value

        return {"rows": rows}


class TableColSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCol
        fields = "__all__"

    def validate_col_type(self, value: str):
        if value not in TableCol.TYPES.keys():
            raise serializers.ValidationError(
                f"Invalid column type. Must be one of {list(TableCol.TYPES.keys())}"
            )

        return value

    def to_representation(self, instance: Union[TableCol, List[TableCol]]):
        def one_representation(instance: TableCol):
            return {
                "col_index": instance.col_index,
                "col_name": instance.col_name,
                "col_type": instance.col_type,
                "human_col_type": TableCol.TYPES[instance.col_type],
                "id": instance.id,
            }

        if isinstance(instance, list):
            cols = {}
            for table_col_model in instance:
                table_col = TableColSerializer(table_col_model).data
                cols[table_col["col_name"]] = table_col

            return cols

        return one_representation(instance)


class GetDataSerializer(serializers.Serializer):
    file_id = serializers.CharField(required=True)
    page_size = serializers.IntegerField(required=True)
    page = serializers.IntegerField(default=0)

    sort_by = serializers.CharField(default="row_index")
    asc = serializers.BooleanField(default=True)

    def validate_file_id(self, value: str):
        if TableCol.objects.filter(file_id=value).count() == 0:
            raise ValidationError(f"file_id '{value}' does not exist on db")

        return value
