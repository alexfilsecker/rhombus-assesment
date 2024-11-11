from typing import Any, Dict, List, Set, Union

import numpy as np
import pandas as pd
from api.models.generic_data_model import IMPORTANT_KEYS_BY_DTYPE, GenericData
from humanize import precisedelta
from rest_framework.serializers import ModelSerializer, ValidationError


class GenericDataSerializer(ModelSerializer):
    """The serializer for the `GenericData` model."""

    class Meta:
        model = GenericData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        We can pass `row_order` and `num_of_cols` as kwargs to the serializer.
        both are used in `to_representation`, `row_order` is used in `represent_with_row_order`
        and `num_of_cols` is used in `represent_without_row_order`.
        """

        self.row_order = None
        if "row_order" in kwargs:
            self.row_order = kwargs.pop("row_order")

        self.num_of_cols = None
        if "num_of_cols" in kwargs:
            self.num_of_cols = kwargs.pop("num_of_cols")

        super().__init__(*args, **kwargs)

    def validate_nones(self, attrs: Dict[str, Any], important_keys: Set[str]) -> None:
        """
        It ensures that the important keys are not None and the rest are None according to the `col_type` of the column.

        Args:
            attrs (Dict[str, Any]): the attrs to validate
            important_keys (Set[str]): the important keys for the column

        Raises:
            ValidationError: When the important keys are None
            ValidationError: When the non-important keys are not None
        """

        for key, value in attrs.items():
            if key in {"row", "column"}:
                continue

            if key in important_keys:
                if value is None:
                    raise ValidationError(f"{key} cannot be None")
            else:
                if value is not None:
                    raise ValidationError(f"{key} must be set to None")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        The overwritten validate method of `ModelSerializer`.


        Args:
            attrs (Dict[str, Any]):
                The attributes to validate

        Returns:
            attrs (Dict[str, Any]): The validated attributes
        """

        col = attrs["column"]
        self.validate_nones(attrs, IMPORTANT_KEYS_BY_DTYPE[col.col_type])
        return attrs

    def to_representation(
        self, instance: Union[GenericData, List[GenericData]]
    ) -> Union[Dict[str, Any], Dict[str, List[Dict[str, Any]]]]:
        """
        The overwritten `to_representation` method of `ModelSerializer`.
        It accepts either a single instance or a list of instances and returns the representation of the instance(s).
        If it is a single instance, it uses `one_representation` to represent it.
        If it is a list of instances, it uses `represent_with_row_order` if `row_order` is not None, otherwise it uses `represent_without_row_order`.

        Args:
            instance (Union[GenericData, List[GenericData]]): The single or list of instances to represent

        Returns:
            return (Union[Dict[str, Any], List[Dict[str, Any]]]):
                Either the representation of a single instance or a list of instances.
        """

        def one_representation(instance: GenericData) -> Dict[str, Any]:
            """
            Represents a single instance of `GenericData` model as a dictionary.

            Args:
                instance (GenericData): The single instance to represent.

            Raises:
                ValidationError: When dtype stored in the database is not supported by the serializer.

            Returns:
                Dict[str, Any]: The dictionary representation of the instance. It has the following keys:
                    - row_index (int): The row index of the instance
                    - col_name (str): The column name of the instance
                    - value (Any): The transformed value of the file cell according to the `col_type` of the column.
            """

            # Initialize the return data with the row_index and col_name
            data = {
                "row_index": instance.row,
                "col_name": instance.column.col_name,
            }

            # Get the columns dtype
            dtype: str = instance.column.col_type

            # Transform the value according to the dtype
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

            elif dtype.startswith("complex"):
                real = instance.double_value
                imag = instance.double_imag_value
                value = {"real": real, "imag": imag}

            elif dtype == "datetime64[ns]":
                value = instance.datetime_value

            elif dtype == "category":
                value = instance.string_value

            elif dtype == "timedelta64[ns]":
                time_delta_value = instance.uint_value
                timedelta: pd.Timedelta = pd.to_timedelta(time_delta_value, "ns")
                value = precisedelta(timedelta, minimum_unit="milliseconds")

            else:
                raise ValidationError(f"DTYPE '{dtype}' NOT FOUND")

            return {**data, "value": value}

        # If instance is not a list, represent it as a single instance
        if not isinstance(instance, list):
            return one_representation(instance)

        # Represent the list of instances according to row_order
        if self.row_order is None:
            rows = self.represent_without_row_order(instance)
        else:
            rows = self.represent_with_row_order(instance)

        # A dictionary return is used instead of a list because of issues with the ModelSerializer Parent class
        return {"rows": rows}

    def represent_with_row_order(
        self, generic_data_models: List[GenericData]
    ) -> List[Dict[str, Any]]:
        """It uses the `row_order` to represent the list of models.

        Args:
            generic_data_models (List[GenericData]): The list of models to represent

        Returns:
            rows (List[Dict[str, Any]]):
                A list of dictionaries representing each row.
                The list is ordered according to `row_order` that was passed on initialization.

                Each row will be a dictionary with the following keys
                    - row_index (int): The row index of the row
                    - values (Dict[str, Any]): Another dictionary with the column name as key and the value as value.
                    This format is the best to display the data in the frontend.
        """

        # A hash to store lists of serialized data by row_index
        serialized_generic_data_hash: Dict[int, List[Any]] = dict()

        # Traverse the models and hash them by row_index
        for generic_data_model in generic_data_models:

            # Serialize the model. Notice it will use the `one_representation` method
            serialized_generic_data = GenericDataSerializer(generic_data_model).data
            row_index = serialized_generic_data["row_index"]

            if row_index not in serialized_generic_data_hash:
                serialized_generic_data_hash[row_index] = []

            serialized_generic_data_hash[row_index].append(serialized_generic_data)

        # Now, traverse the row_order and get the serialized data for each row_index
        rows: List[Dict[str, Any]] = []
        for row_index in self.row_order:
            serialized_generic_datas = serialized_generic_data_hash[row_index]

            # create the row dictionary
            row = {"row_index": row_index, "values": {}}
            for serialized_generic_data in serialized_generic_datas:
                col_name = serialized_generic_data["col_name"]
                value = serialized_generic_data["value"]
                row["values"][col_name] = value

            rows.append(row)

        return rows

    def represent_without_row_order(
        self, generic_data_models: List[GenericData]
    ) -> List[Dict[str, Any]]:
        """
        It represents the list of models without using the `row_order`,
        Instead it returns the rows in the same order given by the input `generic_data_models`.

        Args:
            generic_data_models (List[GenericData]): The list of models to represent.
            This where previously ordered by a query

        Returns:
            row List[Dict[str, Any]]:
                A list of dictionaries representing each row.
                The list is ordered according to `row_order` that was passed on initialization.

                Each row will be a dictionary with the following keys
                    - row_index (int): The row index of the row
                    - values (Dict[str, Any]): Another dictionary with the column name as key and the value as value.
                    This format is the best to display the data in the frontend.
        """

        # Initialize the rows list with the correct number of rows
        # For this, we use the number of columns passed on initialization
        rows: List[Dict[str, Any]] = [
            {"values": {}}
            for _ in range(int(len(generic_data_models) / self.num_of_cols))
        ]

        # Traverse the models and fill the rows
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
