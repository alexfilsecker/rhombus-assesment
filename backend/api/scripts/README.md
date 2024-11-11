# Rhombus AI Assessment: Data Type Inference

This directory contains the scripts used to infer types and convert data from a `DataFrame` object. It mainly uses the `pandas` library to handle conversions.

## Conversion Flow

The following steps are involved in the inference and conversion process:

1. It all begins in [`infer_data_types.py`](infer_data_types.py) with the function `infer_and_convert_data_types`. This function takes the already read `DataFrame` from the file and a dictionary `force_casting`.

2. For each column, we first check if the user has requested a specific data type for a column in the `force_casting` option. If it does, we attempt the casting using the `force_cast` function from [`force_cast.py`](force_cast.py). In case it fails, we add an error to the `errors` dictionary and attempt default conversion. If it succeeds, we go to the other columns.

3. As `pandas.read_csv` and `pandas.read_excel` already does some inference and conversion, we check if it has converted to a number (`int64` or `float64`) and attempt to downcast it to it's smallest possible representation.

4. As `pandas` converts to `bool`, we do not need to check that type.

5. When `pandas` can not infer the type, we try to do it in the following order: `numbers`, `complex`, `categories`, `timedelta` and `datetime`.
