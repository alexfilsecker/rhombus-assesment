from typing import Any, Dict

from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    Serializer,
    ValidationError,
)

from api.models.table_col_model import TableCol
from api.serializers.table_col_serializer import TableColSerializer


class GetDataSerializer(Serializer):
    file_id = CharField(required=True)
    page_size = IntegerField(required=True)
    page = IntegerField(default=0)

    sort_by = CharField(default="row_index")
    asc = BooleanField(default=True)

    def validate_file_id(self, value: str):
        if TableCol.objects.filter(file_id=value).count() == 0:
            raise ValidationError(f"file_id '{value}' does not exist on db")

        return value

    def validate(self, attrs: Dict[str, Any]):
        sort_by = attrs["sort_by"]
        if sort_by == "row_index":
            return attrs

        file_id = attrs["file_id"]
        cols = TableColSerializer(TableCol.objects.filter(file_id=file_id)).data
        if sort_by not in cols.keys():
            raise ValidationError(
                f"cannot sort by {sort_by} because {file_id} does not have that column"
            )

        return attrs
