def dataset_summary(data):
    """
    Display a compact visual summary of a pandas DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Input DataFrame to summarize.

    Returns
    -------
    None
        Prints the dataset dimensions and the distribution of variable types.
    """
    rows, columns = data.shape

    print("DATASET OVERVIEW")
    print("─" * 40)
    print()
    print(f"Rows{' ' * 25}{rows:,}")
    print(f"Columns{' ' * 22}{columns:,}")
    print()
    print("VARIABLE TYPES")
    print("─" * 40)
    print()

    type_mapping = {
        "int64": "Integer",
        "int32": "Integer",
        "float64": "Numeric",
        "float32": "Numeric",
        "object": "Categorical",
        "category": "Categorical",
        "bool": "Boolean",
        "datetime64[ns]": "Datetime"
    }

    type_counts = data.dtypes.astype(str).map(
        lambda dtype: type_mapping.get(dtype, dtype)
    ).value_counts()

    for variable_type, count in type_counts.items():
        percentage = count / columns * 100
        bar_length = round(percentage / 2)
        bar = "█" * bar_length

        print(
            f"{variable_type:<20}"
            f"{count:>3}   "
            f"{bar:<20}  "
            f"{percentage:>5.1f}%"
        )

    print()
    print("─" * 40)

def dataset_columns(data, metadata=None, max_column_width=20, max_meaning_width=40):
    """
    Display a formatted summary of the columns in a pandas DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Input DataFrame to summarize.

    metadata : dict, optional
        Dictionary containing additional information for selected columns.
        Each value must be a tuple with:
        (understandable, meaning).

        Example
        -------
        {
            "age": ("Yes", "Customer age in years"),
            "income": ("Yes", "Annual customer income")
        }

    max_column_width : int, default=20
        Maximum width allowed for column names.

    max_meaning_width : int, default=40
        Maximum width allowed for the meaning description.

    Returns
    -------
    None
        Prints a formatted summary of the dataset columns.
    """

    metadata = metadata or {}

    def truncate(text, width):
        text = str(text)

        if len(text) <= width:
            return text

        return text[:width - 3] + "..."

    type_mapping = {
        "int64": "Integer",
        "int32": "Integer",
        "float64": "Numeric",
        "float32": "Numeric",
        "object": "Categorical",
        "category": "Categorical",
        "bool": "Boolean",
        "datetime64[ns]": "Datetime"
    }

    column_width = max_column_width

    if metadata:
        meaning_width = max_meaning_width

        print("DATASET COLUMNS")
        print("─" * (column_width + 15 + 10 + 10 + 17 + meaning_width + 4))

        print(
            f"{'Column':<{column_width}}"
            f"{'Type':<15}"
            f"{'Records':>10}"
            f"{'Nulls':>10}"
            f"{'Understandable':>17}  "
            f"{'Meaning':<{meaning_width}}"
        )

        print("─" * (column_width + 15 + 10 + 10 + 17 + meaning_width + 4))

    else:
        print("DATASET COLUMNS")
        print("─" * (column_width + 15 + 10 + 10))

        print(
            f"{'Column':<{column_width}}"
            f"{'Type':<15}"
            f"{'Records':>10}"
            f"{'Nulls':>10}"
        )

        print("─" * (column_width + 15 + 10 + 10))

    for column in data.columns:

        dtype = type_mapping.get(
            str(data[column].dtype),
            str(data[column].dtype)
        )

        records = data[column].notna().sum()
        nulls = data[column].isna().sum()

        column_name = truncate(column, column_width)

        if metadata:
            understandable, meaning = metadata.get(
                column,
                ("—", "—")
            )

            meaning = truncate(meaning, meaning_width)

            print(
                f"{column_name:<{column_width}}"
                f"{dtype:<15}"
                f"{records:>10,}"
                f"{nulls:>10,}"
                f"{understandable:>17}  "
                f"{meaning:<{meaning_width}}"
            )

        else:
            print(
                f"{column_name:<{column_width}}"
                f"{dtype:<15}"
                f"{records:>10,}"
                f"{nulls:>10,}"
            )

    print("─" * (
        column_width
        + 15
        + 10
        + 10
        + (17 + meaning_width + 4 if metadata else 0)
    ))


