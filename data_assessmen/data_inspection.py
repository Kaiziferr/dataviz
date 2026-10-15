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
    meaning_width = max_meaning_width
    table_width = (
        column_width
        + 15
        + 17
        + 13
        + 9
        + (17 + meaning_width + 4 if metadata else 0)
    )

    print("DATASET COLUMNS")
    print("─" * table_width)

    if metadata:
        print(
            f"{'Column':<{column_width}}"
            f"{'Type':<15}"
            f"{'Non-Null Fields':>17}"
            f"{'Null Fields':>13}"
            f"{'Null %':>9}"
            f"{'Understandable':>17}  "
            f"{'Meaning':<{meaning_width}}"
        )

    else:
        print(
            f"{'Column':<{column_width}}"
            f"{'Type':<15}"
            f"{'Non-Null Fields':>17}"
            f"{'Null Fields':>13}"
            f"{'Null %':>9}"
        )

    print("─" * table_width)

    for column in data.columns:

        dtype = type_mapping.get(
            str(data[column].dtype),
            str(data[column].dtype)
        )

        non_nulls = data[column].notna().sum()
        nulls = data[column].isna().sum()
        null_percentage = nulls / len(data) * 100 if len(data) else 0.0

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
                f"{non_nulls:>17,}"
                f"{nulls:>13,}"
                f"{null_percentage:>8.2f}%"
                f"{understandable:>17}  "
                f"{meaning:<{meaning_width}}"
            )

        else:
            print(
                f"{column_name:<{column_width}}"
                f"{dtype:<15}"
                f"{non_nulls:>17,}"
                f"{nulls:>13,}"
                f"{null_percentage:>8.2f}%"
            )

    print("─" * table_width)


