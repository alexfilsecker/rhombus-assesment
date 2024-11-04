from typing import List, Union

from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer, ValidationError

from api.models.table_col_model import TableCol


class TableColSerializer(ModelSerializer):
    class Meta:
        model = TableCol
        fields = "__all__"

    def validate_col_type(self, value: str):
        if value not in TableCol.TYPES.keys():
            raise ValidationError(
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
