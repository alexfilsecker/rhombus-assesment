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

    file_id = models.CharField(max_length=50, null=False, blank=False)
    col_name = models.CharField(max_length=30, null=False, blank=False)
    col_type = models.CharField(choices=TYPES, max_length=10)

    class Meta:
        db_table = "api_table_col"
        indexes = [models.Index(fields=["file_id", "col_name"])]

    def __str__(self):
        return (
            f"table_col = {self.file_id}: {self.col_name}, {self.TYPES[self.col_type]}"
        )


class GenericData(models.Model):
    column = models.ForeignKey(TableCol, on_delete=models.CASCADE)

    # Big in case rhombus decides to test a masive csv
    row = models.PositiveBigIntegerField()

    string_value = models.CharField(max_length=100, null=True)
    int_sign_value = models.SmallIntegerField(null=True)
    uint_value = models.PositiveBigIntegerField(null=True)
    double_value = models.FloatField(null=True)
    datetime_value = models.DateTimeField(null=True)
    time_zone_info_value = models.CharField(max_length=30, null=True)
    bool_value = models.BooleanField(null=True)

    class Meta:
        db_table = "api_generic_data"
        indexes = [models.Index(fields=["column", "row"])]
