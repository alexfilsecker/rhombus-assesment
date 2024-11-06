from django.db.models import CharField, Index, Model, PositiveIntegerField


class TableCol(Model):
    TYPES = {
        "object": "String",
        "datetime64[ns]": "datetime",
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

    file_id = CharField(max_length=50, null=False, blank=False)
    col_index = PositiveIntegerField(null=False)
    col_name = CharField(max_length=30, null=False, blank=False)
    col_type = CharField(choices=TYPES, max_length=20)

    class Meta:
        db_table = "api_table_col"
        indexes = [Index(fields=["file_id", "col_index"])]

    def __str__(self):
        return (
            f"table_col = {self.file_id}: {self.col_name}, {self.TYPES[self.col_type]}"
        )
