from rest_framework import serializers
from .models import GenericData, TableCol
from typing import Dict, Any, Set

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


# class DynamicValueField(serializers.Field):
#     def to_representation(self, value):
#         print(value)
#         return super().to_representation(value)


class GenericDataSerializer(serializers.ModelSerializer):
    # value = DynamicValueField(source="*")

    class Meta:
        model = GenericData
        fields = "__all__"

    def validate(self, values: Dict[str, Any]):
        dtype = values["column"].col_type
        validate_nones(values, IMPORTANT_KEYS_BY_DTYPE[dtype])
        return values


class TableColSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCol
        fields = "__all__"

    def validate_col_type(self, value):
        if value not in TableCol.TYPES.keys():
            raise serializers.ValidationError(
                f"Invalid column type. Must be one of {list(TableCol.TYPES.keys())}"
            )

        return value
