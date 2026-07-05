def plot_box(
    data,
    x=None,
    y=None,
    hue=None,
    title=None,
    whis=1.5,
    ax=None,
    palette="Set1",
    width=0.3,
    linewidth=1):
  """
    Generate a boxplot using Seaborn with a ggplot-inspired style.

    Parameters
    ----------
    data : pandas.DataFrame
        Input DataFrame containing the data to be plotted.

    x : str, optional
        Column name for the categorical variable (x-axis grouping).
        Default: None.

    y : str, optional
        Column name for the numerical variable (y-axis).
        Default: None.

    hue : str, optional
        Column name for subgroup coloring within each x category.
        Default: None.

    title : str, optional
        Title of the plot.
        Default: None.

    whis : float, optional
        Whisker length as a proportion of the IQR beyond the box edges.
        Equivalent to matplotlib's whis parameter.
        Default: 1.5.

    ax : matplotlib.axes.Axes, optional
        Axes object to draw the plot on. If None, a new figure and axes
        are created automatically.
        Default: None.

    palette : str, optional
        Color palette for the boxes. Accepts any valid Seaborn or
        matplotlib palette name (e.g. 'Set1', 'Set2', 'tab10').
        Default: 'Set1'.

    width : float, optional
        Width of the boxes. Values between 0.2 and 0.6 recommended.
        Default: 0.3.

    linewidth : float, optional
        Width of the box borders and whisker lines.
        Default: 1.

    Returns
    -------
    matplotlib.axes.Axes
        Axes object containing the boxplot. Can be passed directly
        to another subplot via the ax parameter.
  """

  if ax is None:
      fig, ax = plt.subplots(figsize=(8, 5))

  sns.boxplot(
      data=data,
      x=x,
      y=y,
      hue=hue,
      whis=whis,
      ax=ax,
      palette=palette,
      width=width,
      linewidth=linewidth,
      flierprops=dict(
          marker="o",
          markerfacecolor="white",
          markeredgecolor="gray",
          markersize=4,
          linewidth=0.8
      )
  )

  ax.set_facecolor("#f5f5f5")
  ax.grid(True, color="white", linewidth=0.8)
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)
  ax.spines["left"].set_visible(False)
  ax.spines["bottom"].set_color("#cccccc")

  if title:
      ax.set_title(title, fontsize=12, pad=10)

  return ax
