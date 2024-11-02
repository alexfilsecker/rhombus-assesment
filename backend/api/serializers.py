from rest_framework import serializers
from .models import GenericData, TableCol
from typing import Dict, Any, Set, Union, List
import numpy as np
from django.core.exceptions import ValidationError

IMPORTANT_KEYS_BY_DTYPE = {
    "object": {"string_value"},
    **{f"uint{2 ** i}": {"uint_value"} for i in range(3, 7)},
    **{f"int{2 ** i}": {"int_value", "int_sign_value"} for i in range(3, 7)},
    **{f"float{2 ** i}": {"double_value"} for i in range(5, 7)},
    "bool": "bool_value",
}

ALL_KEYS = {
    "string_value",
    "int_sign_value",
    "uint_value",
    "double_value",
    "datetime_value",
    "time_zone_info_value",
    "bool_value",
}


def validate_nones(values: Dict[str, Any], important_keys: Set[str]) -> None:
    for key, value in values.items():
        if key in {"row", "column"}:
            continue

        if key in important_keys:
            if value is None:
                raise serializers.ValidationError(f"{key} cannot be None")
        else:
            if value is not None:
                raise serializers.ValidationError(f"{key} must be set to None")


class GenericDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericData
        fields = "__all__"

    def validate(self, values: Dict[str, Any]):
        dtype = values["column"].col_type
        validate_nones(values, IMPORTANT_KEYS_BY_DTYPE[dtype])
        return values

    def to_representation(self, instance: Union[GenericData, List[GenericData]]):
        dtype: str = instance.column.col_type
        data = {
            "row_index": instance.row,
            "col_index": instance.column.col_index,
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

    def to_representation(self, instance: TableCol):
        return {
            "col_index": instance.col_index,
            "col_name": instance.col_name,
            "col_type": instance.col_type,
            "human_col_type": TableCol.TYPES[instance.col_type],
        }
