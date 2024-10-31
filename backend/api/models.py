from django.db import models


# Create your models here.
class GenericData(models.Model):
    TYPES = {
        "STR": "string",
        "D": "date",
        "DT": "datetime",
        "DTZ": "datetimezone",
        "U8": "uint8",
        "U16": "uint16",
        "U32": "uint32",
        "U64": "uint64",
        "I8": "int8",
        "I16": "int16",
        "I32": "int32",
        "I64": "int64",
        "F32": "float32",
        "F64": "float64",
        "BOOL": "bool",
    }

    file_id = models.CharField(max_length=50)
    col_name = models.CharField(max_length=30)
    col_type = models.CharField(choices=TYPES, max_length=20)
    value = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=["file_id", "col_name"])]
