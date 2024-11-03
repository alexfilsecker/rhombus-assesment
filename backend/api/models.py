from typing import Any, Dict, List, Set
from django.db import models
from django.db.models import Manager

IMPORTANT_KEYS_BY_DTYPE: Dict[str, Set[str]] = {
    "object": {"string_value"},
    **{f"uint{2 ** i}": {"uint_value"} for i in range(3, 7)},
    **{f"int{2 ** i}": {"int_value", "int_sign_value"} for i in range(3, 7)},
    **{f"float{2 ** i}": {"double_value"} for i in range(5, 7)},
    "bool": "bool_value",
}


SORTING_MAP: Dict[str, str] = {
    **{k: list(val)[0] for k, val in IMPORTANT_KEYS_BY_DTYPE.items()},
    "row_index": "row",
}


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
    col_index = models.PositiveIntegerField(null=False)
    col_name = models.CharField(max_length=30, null=False, blank=False)
    col_type = models.CharField(choices=TYPES, max_length=10)

    class Meta:
        db_table = "api_table_col"
        indexes = [models.Index(fields=["file_id", "col_index"])]

    def __str__(self):
        return (
            f"table_col = {self.file_id}: {self.col_name}, {self.TYPES[self.col_type]}"
        )


class GenericData(models.Model):
    class Meta:
        db_table = "api_generic_data"
        indexes = [models.Index(fields=["column", "row"])]

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

    @classmethod
    def get_objects_by_columns(cls, cols: Dict[str, Dict[str, Any]]):
        return GenericData.objects.filter(
            column__in=[col["id"] for col in cols.values()]
        )

    @classmethod
    def get_sliced_sorted_cols(
        cls,
        data: Manager,
        cols: Dict[str, Dict[str, Any]],
        request_query: Dict[str, Any],
    ):
        page_size = request_query["page_size"]
        page = request_query["page"]
        sort_by = request_query["sort_by"]
        ascending: bool = request_query["asc"]

        num_of_cols = len(cols)

        sorting_col = cols[sort_by]

        only_sorting_col = data.filter(column=sorting_col["id"])

        order_by = SORTING_MAP[sorting_col["col_type"]]
        if not ascending:
            order_by = "-" + order_by

        sorted_col_models = only_sorting_col.order_by(order_by)[
            page * page_size * num_of_cols : (page + 1) * page_size * num_of_cols
        ]

        return sorted_col_models

        # return data.order_by(order_by)[
        #     page * page_size * num_of_cols : (page + 1) * page_size * num_of_cols
        # ]
