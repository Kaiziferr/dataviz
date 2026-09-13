from typing import Optional
import pandas as pd


def evaluate_completeness(
    table: pd.DataFrame,
    combination: Optional[list[str]] = None,
    acceptance_percentage: float = 0.0,
) -> pd.DataFrame:
    """
    Evaluate the completeness of a data table.

    The function operates in two modes:

    1. Individual column evaluation:
       When ``combination`` is ``None`` or an empty list, each column
       is evaluated independently. Only columns whose completeness
       percentage is greater than or equal to the acceptance percentage
       are included in the result.

    2. Combination evaluation:
       When ``combination`` contains columns, their completeness is
       evaluated jointly at the record level. A record is considered
       complete only when all columns in the combination contain
       non-null values. In this mode, the acceptance percentage is
       not applied.

    Parameters
    ----------
    table : pandas.DataFrame
        Data table to be evaluated.

    combination : list of str, optional
        List of columns to evaluate jointly.
        If ``None`` or empty, each column is evaluated independently.

    acceptance_percentage : float, default=0.0
        Minimum completeness percentage required for a column to be
        included in the result when ``combination`` is empty.
        Must be between 0 and 100.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the completeness profiling results with
        the following columns:

        - ``Dimension`` : Evaluated data quality dimension.
        - ``Column`` : Evaluated column or column combination.
        - ``Record Count`` : Total number of records evaluated.
        - ``Value Count`` : Number of complete records.
        - ``Null Count`` : Number of records containing at least one
          null value.
        - ``Completeness %`` : Percentage of complete records.

    Raises
    ------
    ValueError
        If ``acceptance_percentage`` is outside the range from 0 to 100,
        or if a column specified in ``combination`` does not exist in
        the table.

    Examples
    --------
    Evaluate each column independently:

    >>> evaluate_completeness(
    ...     table=df,
    ...     acceptance_percentage=80
    ... )

    Evaluate a combination of columns:

    >>> evaluate_completeness(
    ...     table=df,
    ...     combination=["A", "B", "C"]
    ... )
    """

    if combination is not None and not isinstance(combination, list):
        raise TypeError(
            "combination must be a list of column names or None."
        )

    if not isinstance(acceptance_percentage, (int, float)):
        raise TypeError(
            "acceptance_percentage must be numeric."
        )

    if not 0 <= acceptance_percentage <= 100:
        raise ValueError(
            "acceptance_percentage must be between 0 and 100."
        )

    combination = combination or []

    missing_columns = [
        column for column in combination
        if column not in table.columns
    ]

    if missing_columns:
        raise ValueError(
            f"The following columns do not exist in the table: "
            f"{missing_columns}"
        )

    record_count = len(table)
    results = []

    if not combination:
        for column in table.columns:
            value_count = table[column].notna().sum()
            null_count = record_count - value_count

            completeness_percentage = (
                (value_count / record_count) * 100
                if record_count > 0
                else 0.0
            )

            if completeness_percentage >= acceptance_percentage:
                results.append(
                    {
                        "Dimension": "Completeness",
                        "Column": column,
                        "Record Count": record_count,
                        "Value Count": int(value_count),
                        "Null Count": int(null_count),
                        "Completeness %": round(
                            completeness_percentage,
                            2,
                        ),
                    }
                )

    else:
        complete_records = table[combination].notna().all(axis=1)

        value_count = complete_records.sum()
        null_count = record_count - value_count

        completeness_percentage = (
            (value_count / record_count) * 100
            if record_count > 0
            else 0.0
        )

        results.append(
            {
                "Dimension": "Completeness",
                "Column": " + ".join(combination),
                "Record Count": record_count,
                "Value Count": int(value_count),
                "Null Count": int(null_count),
                "Completeness %": round(
                    completeness_percentage,
                    2,
                ),
            }
        )

    return pd.DataFrame(
        results,
        columns=[
            "Dimension",
            "Column",
            "Record Count",
            "Value Count",
            "Null Count",
            "Completeness %",
        ],
    )



def evaluate_uniqueness(
    table: pd.DataFrame,
    combination: Optional[list[str]] = None,
    acceptance_percentage: float = 0.0,
) -> pd.DataFrame:
    """
    Evaluate the uniqueness dimension of a dataset.

    The function supports two evaluation modes:

    1. Individual evaluation
       Each column is evaluated independently. Only columns whose
       uniqueness percentage is greater than or equal to the acceptance
       threshold are returned.

    2. Combination evaluation
       A group of columns is evaluated as a composite key. Each unique
       row combination is treated as a unique record. In this mode, the
       acceptance threshold is ignored.

    Parameters
    ----------
    table : pandas.DataFrame
        Input dataset.

    combination : list of str, optional
        Columns to evaluate as a composite key. If ``None`` or empty,
        every column is evaluated independently.

    acceptance_percentage : float, default=0.0
        Minimum uniqueness percentage required to include a column in
        the output. Valid range is [0, 100].

    Returns
    -------
    pandas.DataFrame
        Profiling results with the following columns:

        - Dimension
        - Column
        - Record Count
        - Unique Count
        - Duplicate Count
        - Uniqueness %

    Raises
    ------
    ValueError
        If the acceptance percentage is outside [0, 100], if duplicated
        column names are provided in the combination, or if any column
        does not exist in the dataset.

    Notes
    -----
    Null values are considered valid values during uniqueness analysis.
    Therefore, repeated nulls are counted as duplicates.

    Examples
    --------
    >>> evaluate_uniqueness(df)

    >>> evaluate_uniqueness(
    ...     df,
    ...     acceptance_percentage=95
    ... )

    >>> evaluate_uniqueness(
    ...     df,
    ...     combination=["customer_id", "country"]
    ... )
    """

    if not 0 <= acceptance_percentage <= 100:
        raise ValueError(
            "acceptance_percentage must be between 0 and 100."
        )

    combination = combination or []

    if combination:
        duplicated_columns = pd.Index(combination).duplicated()

        if duplicated_columns.any():
            repeated = pd.Index(combination)[duplicated_columns].unique().tolist()
            raise ValueError(
                f"Duplicate column names in combination: {repeated}"
            )

        missing = sorted(set(combination) - set(table.columns))
        if missing:
            raise ValueError(
                f"Columns not found: {missing}"
            )

    record_count = len(table)
    results = []

    if not combination:

        for column in table.columns:

            unique_count = table[column].nunique(dropna=False)
            duplicate_count = record_count - unique_count

            uniqueness = (
                unique_count / record_count * 100
                if record_count
                else 0.0
            )

            if uniqueness >= acceptance_percentage:
                results.append(
                    {
                        "Dimension": "Uniqueness",
                        "Column": column,
                        "Record Count": record_count,
                        "Unique Count": int(unique_count),
                        "Duplicate Count": int(duplicate_count),
                        "Uniqueness %": round(uniqueness, 2),
                    }
                )

    else:

        unique_count = (
            table[combination]
            .drop_duplicates()
            .shape[0]
        )

        duplicate_count = record_count - unique_count

        uniqueness = (
            unique_count / record_count * 100
            if record_count
            else 0.0
        )

        results.append(
            {
                "Dimension": "Uniqueness",
                "Column": " + ".join(combination),
                "Record Count": record_count,
                "Unique Count": int(unique_count),
                "Duplicate Count": int(duplicate_count),
                "Uniqueness %": round(uniqueness, 2),
            }
        )

    return pd.DataFrame(
        results,
        columns=[
            "Dimension",
            "Column",
            "Record Count",
            "Unique Count",
            "Duplicate Count",
            "Uniqueness %",
        ],
    )
