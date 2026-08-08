def summary(tables:dict, path: Path, read_f = pd.read_csv)-> pd.DataFrame:
    """
        Summarize multiple data files into a single DataFrame.

        Parameters
        ----------
        tables : dict
            Dictionary mapping table names to file paths relative to ``path``.
        path : Path
            Base directory containing the data files.
        read_f : callable, default=pd.read_csv
            Function used to read each data file. It must accept a file path
            as its first argument and return a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame containing one row per table, with the following columns:
            - ``table`` : str
                Name of the table.
            - ``rows`` : int
                Number of rows in the table.
            - ``columns`` : int
                Number of columns in the table.

    """
    rows_list = []
    for name, value in tables.items():
        data = read_f(path/value)
        rows_list.append({
            'table': name,
            'rows': len(data),
            'columns': data.shape[1]
        })
    return pd.DataFrame(rows_list)
  
"""
OLIST_FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv"
}
"""
# summary(OLIST_FILES, Path('../../data'))
