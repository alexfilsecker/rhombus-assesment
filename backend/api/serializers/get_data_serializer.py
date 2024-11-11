from typing import Any, Dict

from api.models.table_col_model import TableCol
from api.serializers.table_col_serializer import TableColSerializer
from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    Serializer,
    ValidationError,
)


class GetDataSerializer(Serializer):
    """
    The serializer for the `get-data` endpoint.
    """

    file_id = CharField(required=True)
    page_size = IntegerField(required=True)
    page = IntegerField(default=0)

    sort_by = CharField(default="row_index")
    asc = BooleanField(default=True)

    def validate_file_id(self, value: str) -> str:
        """
        The overridden method to validate the `file_id` field.
        It checks if the `file_id` exists in the database.

        Args:
            value (str): The value of the `file_id` field.

        Raises:
            ValidationError: If the `file_id` does not exist in the database.

        Returns:
            value (str): The value of the `file_id` field.
        """

        if TableCol.objects.filter(file_id=value).count() == 0:
            raise ValidationError(f"file_id '{value}' does not exist on db")

        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        The overridden method to validate the serializer fields.
        It checks if the `sort_by` field is a valid column name or `row_index`.

        Args:
            attrs (Dict[str, Any]): The attributes of the serializer.

        Raises:
            ValidationError: If the `sort_by` field is not a valid column name.

        Returns:
            attrs (Dict[str, Any]): The attributes of the serializer after validation.
        """

        sort_by = attrs["sort_by"]

        # if the sort_by field is "row_index" there is no need to check the columns
        if sort_by == "row_index":
            return attrs

        # Get the columns of the file
        file_id = attrs["file_id"]
        table_col_models = TableCol.objects.filter(file_id=file_id)
        cols = TableColSerializer(list(table_col_models)).data

        # Check if the sort_by field is a valid column name
        if sort_by not in cols.keys():
            raise ValidationError(
                f"cannot sort by {sort_by} because {file_id} does not have that column"
            )

        return attrs
