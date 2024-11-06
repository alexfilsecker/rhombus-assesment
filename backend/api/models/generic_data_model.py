from typing import Any, Dict, List, Set

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    Index,
    Manager,
    Model,
    PositiveBigIntegerField,
    SmallIntegerField,
)

from .table_col_model import TableCol

IMPORTANT_KEYS_BY_DTYPE: Dict[str, Set[str]] = {
    "object": {"string_value"},
    **{f"uint{2 ** i}": {"uint_value"} for i in range(3, 7)},
    **{f"int{2 ** i}": {"uint_value", "int_sign_value"} for i in range(3, 7)},
    **{f"float{2 ** i}": {"double_value"} for i in range(5, 7)},
    "bool": "bool_value",
    "complex128": {"double_value", "double_imag_value"},
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
    double_imag_value = FloatField(null=True)
    datetime_value = DateTimeField(null=True)
    time_zone_info_value = CharField(max_length=30, null=True)
    bool_value = BooleanField(null=True)

    @classmethod
    def get_objects_by_columns(
        cls, cols: Dict[str, Dict[str, Any]]
    ) -> Manager["GenericData"]:
        return GenericData.objects.filter(
            column__in=[col["id"] for col in cols.values()]
        )

    @staticmethod
    def slice_and_sort_by_row(
        data: Manager["GenericData"],
        cols: Dict[str, Dict[str, Any]],
        request_query: Dict[str, Any],
    ):
        ascending: bool = request_query["asc"]
        page_size = request_query["page_size"]
        page = request_query["page"]

        order_by = f"{'-' if not ascending else ''}row"
        sorted_data_models = data.order_by(order_by)[
            page * page_size * len(cols) : (page + 1) * page_size * len(cols)
        ]
        return sorted_data_models

    @staticmethod
    def slice_and_sort_by_col(
        data: Manager["GenericData"],
        cols: Dict[str, Dict[str, Any]],
        request_query: Dict[str, Any],
    ) -> Manager["GenericData"]:
        # Get parameters from request_query
        page_size = request_query["page_size"]
        page = request_query["page"]
        sort_by = request_query["sort_by"]
        ascending: bool = request_query["asc"]

        # Generate the order_by string
        sorting_col = cols[sort_by]
        order_by = SORTING_MAP[sorting_col["col_type"]]

        # Add '-' if it is descending
        order_by = f"{'-' if not ascending else ''}{order_by}"

        # Get data from the sorting column
        only_sorting_col_data = data.filter(column=sorting_col["id"])

        # order and slice
        sorted_col_data_models = only_sorting_col_data.order_by(order_by)[
            page * page_size : (page + 1) * page_size
        ]

        return sorted_col_data_models
