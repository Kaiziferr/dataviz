def null_percentage_per_feature(data: pd.DataFrame, **kwargs) -> None:
    """
    Generate a horizontal distribution plot showing the percentage of null
    values per feature in a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Input DataFrame used to compute null value percentages.

    **kwargs :
        Additional keyword arguments passed to seaborn.displot().set()
        for plot customization (e.g., title, labels).

    Returns
    -------
    None
        Does not return a value. Displays the null percentage distribution plot.
    """
    try:
        ticklabels = (
            data.isnull()
            .melt()
            .pipe(
                lambda df: sns.displot(
                    data=df,
                    y='variable',
                    hue='value',
                    multiple='fill',
                    aspect=5
                ).set(**kwargs)
            )
        )

        p = data.isnull().sum() / data.shape[0]

        for i, (feature, value) in enumerate(p.items()):
            if value > 0:
                ticklabels.ax.text(
                    value + 0.015,
                    i + 0.2,
                    f'{round(value * 100, 2)}%',
                    ha="center",
                    color='w',
                    fontweight='bold'
                )
    except Exception as e:
        print(e)
        
# null_percentage_per_feature(data, title="Percentage of missing values", xlabel='Percentage of missing values', ylabel='Features')