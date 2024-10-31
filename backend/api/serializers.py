from rest_framework.serializers import ModelSerializer
from .models import GenericData


class GenericDataSerializer(ModelSerializer):
    class Meta:
        model = GenericData
        fields = "__all__"
