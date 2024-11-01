from rest_framework import serializers
from .models import GenericData, TableCol


class GenericDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericData
        fields = "__all__"


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
