from typing import Any, Dict, List, Set

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    F,
    FloatField,
    ForeignKey,
    Func,
    Index,
    Manager,
    Model,
    PositiveBigIntegerField,
    SmallIntegerField,
)

from .table_col_model import TableCol


class AbsoluteValue(Func):
    function = "ABS"
    output_field = FloatField()


# The keys that must be not None for each dtype
IMPORTANT_KEYS_BY_DTYPE: Dict[str, Set[str]] = {
    "object": {"string_value"},
    **{f"uint{2 ** i}": {"uint_value"} for i in range(3, 7)},
    **{f"int{2 ** i}": {"uint_value", "int_sign_value"} for i in range(3, 7)},
    **{f"float{2 ** i}": {"double_value"} for i in range(5, 7)},
    "bool": {"bool_value"},
    "complex128": {"double_value", "double_imag_value"},
    "category": {"string_value"},
    "datetime64[ns]": {"datetime_value"},
    "timedelta64[ns]": {"uint_value"},
}


# The keys to sort by for each dtype
SORTING_MAP: Dict[str, List[str]] = {
    **{k: list(val) for k, val in IMPORTANT_KEYS_BY_DTYPE.items()},
    "row_index": {"row"},
}


class GenericData(Model):
    """
    The model for the `api_generic_data` table.
    It stores all cells from the files in the most generic way possible.
    """

    class Meta:
        db_table = "api_generic_data"
        indexes = [Index(fields=["column", "row"])]

    # The column that this data belongs to
    # Notice the normalization, where a GenericData belongs to a column and a column belongs to a file
    column = ForeignKey(TableCol, on_delete=CASCADE)

    # Big in case rhombus decides to test a massive csv
    row = PositiveBigIntegerField()

    # The columns we use to store any type of data
    # Notice that all of them can be null
    # That is because we will be using some of them and not others depending on the dtype of the column
    string_value = CharField(max_length=100, null=True)
    int_sign_value = SmallIntegerField(null=True)
    uint_value = PositiveBigIntegerField(null=True)
    double_value = FloatField(null=True)
    double_imag_value = FloatField(null=True)
    datetime_value = DateTimeField(null=True)
    time_zone_info_value = CharField(max_length=30, null=True)
    bool_value = BooleanField(null=True)

    @staticmethod
    def get_objects_by_columns(
        cols: Dict[str, Dict[str, Any]]
    ) -> Manager["GenericData"]:
        """
        A method to query the `GenericData` objects by the columns they belong to.

        Args:
            cols (Dict[str, Dict[str, Any]]):
                A dictionary of column names to serialized TableCol objects.

        Returns:
            generic_data: Manager[GenericData]: A query with `GenericData` filtered by objects that belong to the given columns.
        """

        # Get the ids of the columns we want to query
        col_ids = [col["id"] for col in cols.values()]
        return GenericData.objects.filter(column__in=col_ids)

    @staticmethod
    def slice_and_sort_by_row(
        data: Manager["GenericData"],
        num_of_cols: Dict[str, Dict[str, Any]],
        request_query: Dict[str, Any],
    ) -> Manager["GenericData"]:
        """
        A static method to first sort the data by row and then slice it generating
        the correct pagination.

        Args:
            data (Manager["GenericData"]):
                The data to sort and slice.
            num_of_cols (int):
                The number of columns in the data. This is used to calculate the pagination.
            request_query (Dict[str, Any]):
                The query parameters from the request.

        Returns:
            sorted_data_models (Manager["GenericData"]):
                An ongoing query of the sorted and sliced data models.
        """

        # Get parameters from request_query
        ascending: bool = request_query["asc"]
        page_size: int = request_query["page_size"]
        page: int = request_query["page"]

        # Generate the order_by string adding '-' if it is descending
        order_by = f"{'-' if not ascending else ''}row"

        # Sort and slice
        sorted_data_models = data.order_by(order_by)[
            page * page_size * num_of_cols : (page + 1) * page_size * num_of_cols
        ]

        return sorted_data_models

    @staticmethod
    def slice_and_sort_by_col(
        data: Manager["GenericData"],
        cols: Dict[str, Dict[str, Any]],
        request_query: Dict[str, Any],
    ) -> Manager["GenericData"]:
        """
        A static method to first sort the data by the requested sort_by
        and then slice. This method is different from `slice_and_sort_by_row` because
        It returns the sorted data of just the sorting column, not all the columns.

        Args:
            data (Manager["GenericData"]):
                The data to sort and slice.
            cols (Dict[str, Dict[str, Any]]):
                The columns in the data. This is used to get the column to sort by.
            request_query (Dict[str, Any]):
                The query parameters from the request.

        Returns:
            sorted_col_data_models (Manager[GenericData]):
                An ongoing query of the sorted and sliced data models that belong to the sorting column.
        """

        # Get parameters from request_query
        page_size = request_query["page_size"]
        page = request_query["page"]
        sort_by = request_query["sort_by"]
        ascending: bool = request_query["asc"]

        # Generate the order_by string
        sorting_col = cols[sort_by]
        col_type: str = sorting_col["col_type"]
        order_by_list = SORTING_MAP[col_type]

        # Get data from the sorting column
        only_sorting_col_data = data.filter(column=sorting_col["id"])

        if len(order_by_list) == 1:
            order_by = order_by_list[0]

            # Add '-' if it is descending
            order_by = f"{'-' if not ascending else ''}{order_by}"

            # order and slice the data from the column
            sorted_col_data_models = only_sorting_col_data.order_by(order_by)[
                page * page_size : (page + 1) * page_size
            ]
        else:
            if col_type.startswith("int"):
                signed_value = F(order_by_list[0]) * F(order_by_list[1])
                order_by = "signed_value"
                order_by = f"{'-' if not ascending else ''}{order_by}"
                sorted_col_data_models = only_sorting_col_data.annotate(
                    signed_value=signed_value
                ).order_by(order_by)[page * page_size : (page + 1) * page_size]
            elif col_type.startswith("complex"):
                abs_value = AbsoluteValue(
                    F(order_by_list[0]) ** 2 + F(order_by_list[1]) ** 2
                )
                order_by = "abs_value"
                order_by = f"{'-' if not ascending else ''}{order_by}"
                sorted_col_data_models = only_sorting_col_data.annotate(
                    abs_value=abs_value
                ).order_by(order_by)[page * page_size : (page + 1) * page_size]

        return sorted_col_data_models
