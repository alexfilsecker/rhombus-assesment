from typing import Any, Dict, List, Set, Union

import numpy as np
from rest_framework.serializers import ModelSerializer, ValidationError

from api.models.generic_data_model import IMPORTANT_KEYS_BY_DTYPE, GenericData


class GenericDataSerializer(ModelSerializer):

    class Meta:
        model = GenericData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.starting_row = 0
        if "num_of_rows" in kwargs:
            self.num_of_rows = kwargs.pop("num_of_rows")
            self.starting_row = kwargs.pop("starting_row")
            super().__init__(*args, **kwargs)

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
        dtype = attrs["column"].col_type
        self.validate_nones(attrs, IMPORTANT_KEYS_BY_DTYPE[dtype])
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
