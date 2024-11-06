import time
from typing import Any, Dict, List, Set, Union

import numpy as np
from api.models.generic_data_model import IMPORTANT_KEYS_BY_DTYPE, GenericData
from rest_framework.serializers import ModelSerializer, ValidationError


class GenericDataSerializer(ModelSerializer):

    class Meta:
        model = GenericData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.row_order = None
        if "row_order" in kwargs:
            self.row_order = kwargs.pop("row_order")
        self.num_of_cols = None
        if "num_of_cols" in kwargs:
            self.num_of_cols = kwargs.pop("num_of_cols")

        super().__init__(*args, **kwargs)

    def validate_nones(self, values: Dict[str, Any], important_keys: Set[str]) -> None:
        for key, value in values.items():
            if key in {"row", "column"}:
                continue

            if key in important_keys:
                if value is None:
                    raise ValidationError(f"{key} cannot be None")
            else:
                if value is not None:
                    raise ValidationError(f"{key} must be set to None")

    def validate(self, attrs: Dict[str, Any]):
        col = attrs["column"]
        self.validate_nones(attrs, IMPORTANT_KEYS_BY_DTYPE[col.col_type])
        return attrs

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
                    "uint8": np.uint8,
                    "uint16": np.uint16,
                    "uint32": np.uint32,
                    "uint64": np.uint64,
                }
                if dtype not in uint_map:
                    raise ValidationError(f"{dtype} not supported in serializer")

                value = uint_map[dtype](instance.uint_value)

            elif dtype.startswith("int"):
                int_map = {
                    "int8": np.int8,
                    "int16": np.int16,
                    "int32": np.int32,
                    "int64": np.int64,
                }
                if dtype not in int_map:
                    raise ValidationError(f"{dtype} not supported in serializer")

                value = int_map[dtype](instance.uint_value * instance.int_sign_value)

            elif dtype.startswith("float"):
                float_map = {
                    "float32": np.float32,
                    "float64": np.float64,
                }
                if dtype not in float_map:
                    raise ValidationError(f"{dtype} not supported in serializer")

                value = float_map[dtype](instance.double_value)

            elif dtype == "datetime64[ns]":
                value = instance.datetime_value

            elif dtype == "category":
                value = instance.string_value

            else:
                raise ValidationError(f"DTYPE '{dtype}' NOT FOUND")

            return {**data, "value": value}

        if not isinstance(instance, list):
            return one_representation(instance)

        if self.row_order is None:
            rows = self.represent_without_row_order(instance)
        else:
            rows = self.represent_with_row_order(instance)

        return {"rows": rows}

    def represent_with_row_order(self, generic_data_models: List[GenericData]):
        # get model representations and hash them by row_index
        serialized_generic_data_hash: Dict[int, List[Any]] = dict()
        for generic_data_model in generic_data_models:
            serialized_generic_data = GenericDataSerializer(generic_data_model).data
            row_index = serialized_generic_data["row_index"]

            if row_index not in serialized_generic_data_hash:
                serialized_generic_data_hash[row_index] = []

            serialized_generic_data_hash[row_index].append(serialized_generic_data)

        rows: List[Dict[str, Any]] = []
        for row_index in self.row_order:
            serialized_generic_datas = serialized_generic_data_hash[row_index]

            row = {"row_index": row_index, "values": {}}

            for serialized_generic_data in serialized_generic_datas:
                col_name = serialized_generic_data["col_name"]
                value = serialized_generic_data["value"]
                row["values"][col_name] = value

            rows.append(row)

        return rows

    def represent_without_row_order(self, generic_data_models: List[GenericData]):
        rows: List[Dict[str, Any]] = [
            {"values": {}}
            for _ in range(int(len(generic_data_models) / self.num_of_cols))
        ]

        for count, generic_data_model in enumerate(generic_data_models):
            index = count // self.num_of_cols
            serialized_generic_data = GenericDataSerializer(generic_data_model).data

            col_name = serialized_generic_data["col_name"]
            value = serialized_generic_data["value"]
            row_index = serialized_generic_data["row_index"]

            if "row_index" not in rows[index]:
                rows[index]["row_index"] = row_index

            rows[index]["values"][col_name] = value

        return rows
