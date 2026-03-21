def plot_numeric_distributions(data: pd.DataFrame,
                               nrows: int = 3,
                               ncols: int = 3,
                               figsize: tuple = (9, 6),
                               fontsize_title: int = 12,
                               palette=None,
                               show_stats=None) -> None:

    """
    Plot histograms with KDE for all numeric features in a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Input DataFrame containing numeric features to visualize.

    nrows : int, default=3
        Number of subplot rows.

    ncols : int, default=3
        Number of subplot columns.

    figsize : tuple, default=(9, 6)
        Figure size as (width, height).

    fontsize_title : int, default=12
        Font size for the main figure title.

    palette : None, str, list or dict
        - None → usa colores por defecto
        - str → nombre de paleta seaborn
        - list → lista de colores
        - dict → {"columna": "color"}

    show_stats : None, str or list, default=None
        - None → no muestra estadísticas
        - "all" → muestra mean, median y mode
        - list → ["mean", "median", "mode"]

    Returns
    -------
    None
        Does not return a value. Displays the distribution plots.
    """

    try:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.flat

        numeric_columns = data.select_dtypes(include=np.number).columns

        # Manejo de estadísticas
        if show_stats == "all":
            show_stats = ["mean", "median", "mode"]

        # Preparar colores base
        if palette is None:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        elif isinstance(palette, str):
            colors = sns.color_palette(palette, len(numeric_columns))
        elif isinstance(palette, list):
            colors = palette
        elif isinstance(palette, dict):
            colors = None
        else:
            raise ValueError("palette must be None, str, list or dict")

        for i, column in enumerate(numeric_columns):

            # Selección de color
            if isinstance(palette, dict):
                color = palette.get(
                    column,
                    plt.rcParams['axes.prop_cycle'].by_key()['color'][i % 10]
                )
            else:
                color = colors[i % len(colors)]

            ax = axes[i]

            sns.histplot(
                data=data,
                x=column,
                stat="count",
                kde=True,
                color=color,
                ax=ax
            )

            if show_stats:
                series = data[column].dropna()

                if "mean" in show_stats:
                    ax.axvline(series.mean(), color="black", linestyle="--", label="Mean")

                if "median" in show_stats:
                    ax.axvline(series.median(), color="blue", linestyle=":", label="Median")

                if "mode" in show_stats and not series.mode().empty:
                    ax.axvline(series.mode().iloc[0], color="red", linestyle="-.", label="Mode")

                ax.legend(fontsize=7)

            ax.set_title(column, fontsize=10)
            ax.tick_params(labelsize=8)
            ax.set_xlabel("")

        fig.tight_layout()
        plt.subplots_adjust(top=0.9)
        fig.suptitle('Numeric Feature Distributions', fontsize=fontsize_title)

    except Exception as e:
        print(e)

# plot_numeric_distributions(data, 2, 2, palette=p, show_stats=['mean', 'median'])


def plot_categorical_donut_charts(data: pd.DataFrame,
                                   nrows: int = 1,
                                   ncols: int = 3,
                                   figsize: tuple = (9, 6),
                                   fontsize_title: int = 12,
                                   donut_width: float = 0.7,
                                   autopct_format: str = '%1.1f%%',
                                   c: dict=None) -> None:
  """
  Plot donut charts for all categorical (object) features in a DataFrame.

  Parameters
  ----------
  data : pandas.DataFrame
      Input DataFrame containing categorical features.

  nrows : int, default=1
      Number of subplot rows.

  ncols : int, default=3
      Number of subplot columns.

  figsize : tuple, default=(9, 6)
      Figure size as (width, height).

  fontsize_title : int, default=12
      Font size for the main figure title.

  donut_width : float, default=0.7
      Radius of the white circle to create donut effect.

  autopct_format : str, default='%1.1f%%'
      Format string for percentage labels.

  color_dict : dict, default=None
        Dictionary of colors per column

  Returns
  -------
  None
      Displays the donut charts.
  """

  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
  ax = ax.flat

  category_columns = data.select_dtypes(include='object').columns

  for i, column in enumerate(category_columns):

      if i >= len(ax):
          break

      value_counts = data[column].value_counts()
      color_cycle = list(plt.rcParams['axes.prop_cycle'])
      if c and column in c:
        colors = [
            c[column].get(cat, 'gray')
            for cat in value_counts.index
            ]
      else:
        colors = [color_cycle[j % len(color_cycle)]["color"]
                  for j in range(len(data[column].value_counts()))]


      ax[i].pie(
          value_counts,
          labels=value_counts.index,
          autopct=lambda pct: f"{int(round(pct * sum(value_counts) / 100.0))} ({pct:1.1f}%)",
          colors=colors,
          textprops={'fontsize': 8}
      )

      # Donut effect
      centre_circle = plt.Circle((0, 0), donut_width, color='white')
      ax[i].add_artist(centre_circle)

      ax[i].set_title(column, fontsize=10)

  fig.tight_layout()
  plt.subplots_adjust(top=0.8)
  fig.suptitle('Categorical Feature Distribution', fontsize=fontsize_title)

  # plot_categorical_donut_charts(data, 1, 3, figsize=(15, 5), c=paleta)