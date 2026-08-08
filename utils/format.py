from unicodedata import normalize

def normalize_word(word:str)->str:
  """
    Normalize a string into a standardized snake_case format.

    This function converts a word or phrase into a normalized representation
    suitable for use as column names, identifiers, or feature names. The
    normalization process performs the following operations:

    1. Replaces spaces (`" "`) with underscores (`"_"`).
    2. Replaces hyphens (`"-"`) with underscores (`"_"`).
    3. Removes consecutive or leading/trailing underscores generated during
      the replacement process.
    4. Converts all characters to lowercase.
    5. Removes diacritical marks (accents) by converting Unicode characters
      to their closest ASCII representation.
    6. Joins the resulting tokens using a single underscore.

    Parameters
    ----------
    word : str
        Input string to normalize.

    Returns
    -------
    str
        A normalized string in lowercase snake_case with ASCII characters
        only.
  """
  word = word.replace(' ', '_')
  word = word.replace('-', '_')
  find_guion = word.find('_')
  list_word = []
  if find_guion:
    list_word = [w for w in word.split('_') if w != '']
  else:
    list_word = word
  word = list(map(lambda x: x.lower(), list_word))
  word = [normalize('NFKD', c).encode('ASCII', 'ignore').decode() for c in word]
  word = "_".join(word)
  return word
