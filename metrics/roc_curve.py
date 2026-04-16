def roc_curve_plot(
    y_true:np.array,
    y_pred:list,
    labels:list,
    color:list=None,
    size:tuple=(10,5),
    threshold_prede:list=[0, 1],
    **Kwargs)-> None:
    """
      Plot ROC curves for one or multiple prediction sets.

      Parameters
      ----------
      y_true : numpy.array
          Array of true binary labels.

      y_pred : list
          List of arrays containing predicted scores or probabilities
          for each model.

      labels : list
          List of labels for each ROC curve.

      color : list, default=None
          List of colors for each curve.
          If None, default matplotlib colors are used.

      size : tuple, default=(10, 5)
          Figure size as (width, height).

      threshold_prede : list, default=[0, 1]
          Values used to plot the diagonal reference line
          representing random guessing.

      **Kwargs : dict
          Additional keyword arguments passed to sklearn.metrics.roc_curve.

      Returns
      -------
      None
          Displays the ROC curve plot.
    """
    try:
      fig, ax = plt.subplots(figsize = size)

      data = []

      for i in range(len(y_pred)):
        fpr, tpr, thresholds = roc_curve(y_true, y_pred[i], **Kwargs)
        if color:
          plt.plot(fpr, tpr, "--", label=labels[i], color=color[i])
        else:
          plt.plot(fpr, tpr, label=labels[i])

      plt.plot(threshold_prede, threshold_prede   , 'k:', label='Random guess')
      plt.xlabel('False Positive Rate')
      plt.ylabel('True Positive Rate')
      plt.title('ROC Curve')
      plt.legend()
      plt.show()

    except Exception as e:
      raise e
    
prd = [y_pred_forest, y_pred_log, y_pred_tree, y_dummy]
labes = ["Random Forest", "Logistic Regression", "Decision Tree", "Dummy"]
color=["red", "blue", "green", "black"]
roc_curve_plot(y_test, prd, labes, color, **{'pos_label': 1})