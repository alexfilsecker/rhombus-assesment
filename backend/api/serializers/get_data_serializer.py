from rest_framework.serializers import (
    Serializer,
    CharField,
    IntegerField,
    BooleanField,
    ValidationError,
)
from ..models.table_col_model import TableCol


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
