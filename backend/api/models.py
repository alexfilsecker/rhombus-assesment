from django.db import models


class TableCol(models.Model):
    TYPES = {
        "object": "String",
        # "": "Date",
        # "DT": "DateTime",
        # "DTZ": "DateTime with TimeZone",
        "uint8": "Unsigned 8 bit Integer",
        "uint16": "Unsigned 16 bit Integer",
        "uint32": "Unsigned 32 bit Integer",
        "uint64": "Unsigned 64 bit Integer",
        "int8": "Signed 8 bit Integer",
        "int16": "Signed 16 bit Integer",
        "int32": "Signed 32 bit Integer",
        "int64": "Signed 64 bit Integer",
        "float32": "32 bit Floating Number",
        "float64": "Float64",
        "bool": "Boolean",
    }

    file_id = models.CharField(max_length=50)
    col_name = models.CharField(max_length=30)
    col_type = models.CharField(choices=TYPES, max_length=10)

    class Meta:
        indexes = [models.Index(fields=["file_id", "col_name"])]

    def __str__(self):
        return f"{self.file_id}: {self.col_name} TYPE: {self.TYPES[self.col_type]}"


class GenericData(models.Model):
    column = models.ForeignKey(TableCol, on_delete=models.CASCADE)

    # Big in case rhombus decides to test a masive csv
    row = models.PositiveBigIntegerField()

    string_value = models.CharField(max_length=100)
    int_sign = models.SmallIntegerField()
    uint_value = models.PositiveBigIntegerField()
    double_value = models.FloatField()
    timestamp_value = models.TimeField()
    time_zone_value = models.CharField(max_length=50)

    class Meta:
        indexes = [models.Index(fields=["column", "row"])]
