# utilities.py :)
def get_text(path):
  with open(path) as f: text = f.readlines()
  return "".join(text).replace("\n", "")

