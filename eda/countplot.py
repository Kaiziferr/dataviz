def plot_bar(data:pd.DataFrame, paleta:list=None, figsize_x:int=8, figsize_y:int=5,
             fontsize:int=15, **kwards)->None:
  """Plot a bar chart with multiple features."""
  try:

      v = kwards
      ejeX = v['ejeX']

      fig, ax = plt.subplots(figsize = (figsize_x, figsize_y))
      fig.suptitle(f'Bar Chart {v["title"]}', fontsize=fontsize)
      

      if type(ejeX) == str:
          sns.countplot(x=ejeX, data=data, ax = ax, palette=paleta)
      else:
          ejeX = v['ejeX'][0]
          sns.countplot(x=ejeX, hue=v['ejeX'][1], data=data, ax=ax, palette=paleta)

      ax.set_ylabel(v['ejey'], size = 12)
      ax.set_xlabel(ejeX, size=fontsize-3)
      ax.set_xticklabels(ax.get_xticklabels(), fontsize = fontsize-3)
      for p in ax.patches:
          try:
              height = int(p.get_height())
              height_text = height
              if kwards['p'] == True:
                  percentage = round(height/data.shape[0], 5)
                  height_text = f'{height} ({percentage})'
                  ax.text(p.get_x()+p.get_width()/2., height + 1, height_text, ha="center") 
          except Exception as e:
              print(e)
  except Exception as e:
    print(e)

# plot_bar(data_train, paleta=paleta, ejeX='Survived',ejey='count Survived',title='Count Survived', p=True)
"""
paleta = {
    "No": "#E41A1C",
    "Yes": "#4DAF4A"
}
"""