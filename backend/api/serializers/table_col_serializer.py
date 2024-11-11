from typing import Dict, List, Union

from api.models.table_col_model import TableCol
from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer, ValidationError


class TableColSerializer(ModelSerializer):
    """The serializer for the `TableCol` model."""

    class Meta:
        model = TableCol
        fields = "__all__"

    def validate_col_type(self, value: str) -> str:
        """
        The overridden method to validate the `col_type` field.
        It checks if the `col_type` is one of the valid column types.

        Args:
            value (str): The value of the `col_type` field.

        Raises:
            ValidationError: If the `col_type` is not one of the valid column types.

        Returns:
            value (str): The value of the `col_type` field after validation.
        """

        if value not in TableCol.TYPES.keys():
            raise ValidationError(
                f"Invalid column type. Must be one of {list(TableCol.TYPES.keys())}"
            )

        return value

    def to_representation(
        self, instance: Union[TableCol, List[TableCol]]
    ) -> Union[Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]]]:
        """
        The overwritten `to_representation` method of `ModelSerializer`.
        It accepts either a single instance or a list of instances and returns the representation of the instance(s).
        If it is a single instance, it uses `one_representation` to represent it.
        If it is a list of instances, it uses `one_representation` to represent each instance and returns a dictionary of the representations.

        Args:
            instance (Union[TableCol, List[TableCol]]): The instance or list of instances to represent.

        Returns:
            col | cols (Union[Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]]):
                Either the representation of a single instance or a dictionary of the representations of the instances.
        """

        def one_representation(instance: TableCol) -> Dict[str, Union[int, str]]:
            return {
                "col_index": instance.col_index,
                "col_name": instance.col_name,
                "col_type": instance.col_type,
                "human_col_type": TableCol.TYPES[instance.col_type],
                "id": instance.id,
            }

        if isinstance(instance, list):
            cols: Dict[str, Dict[str, Union[int, str]]] = {}
            for table_col_model in instance:
                table_col: Dict[str, Union[int, str]] = TableColSerializer(
                    table_col_model
                ).data
                cols[table_col["col_name"]] = table_col

            return cols

        return one_representation(instance)
