def null_percentage_per_feature(data:pd.DataFrame, **kwargs)->None:
    """Calculate the percentage of null values per feature"""
    try:
        ticklabels = data.isnull().melt().pipe(
            lambda df: (
                sns.displot(
                    data=df,
                    y='variable',
                    hue='value',
                    multiple='fill',
                    aspect=5
                    ).set(**kwargs)
                )
            )
        p = (data.isnull().sum()/data.shape[0])
        for n, i in zip(p.index, range(p.shape[0])):
            if p[i] > 0:
                ticklabels.ax.text(p[n]+0.015, i+0.2, f'{round(p[n]*100, 2)}%', ha="center", color='w', fontweight='bold')
    except Exception as e:
        print(e)

# null_percentage_per_feature(data_train, title="Percentage of missing values", xlabel='Percentage of missing values', ylabel='Features')