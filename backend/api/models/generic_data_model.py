from typing import Any, Dict, Set
from django.db.models import (
    Model,
    Index,
    ForeignKey,
    PositiveBigIntegerField,
    CharField,
    SmallIntegerField,
    FloatField,
    DateTimeField,
    BooleanField,
    Manager,
    CASCADE,
)
from .table_col_model import TableCol

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


class GenericData(Model):
    class Meta:
        db_table = "api_generic_data"
        indexes = [Index(fields=["column", "row"])]

    column = ForeignKey(TableCol, on_delete=CASCADE)

    # Big in case rhombus decides to test a masive csv
    row = PositiveBigIntegerField()

    string_value = CharField(max_length=100, null=True)
    int_sign_value = SmallIntegerField(null=True)
    uint_value = PositiveBigIntegerField(null=True)
    double_value = FloatField(null=True)
    datetime_value = DateTimeField(null=True)
    time_zone_info_value = CharField(max_length=30, null=True)
    bool_value = BooleanField(null=True)

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
