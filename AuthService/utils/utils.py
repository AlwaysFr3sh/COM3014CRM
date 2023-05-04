def get_ssap(path):
  with open(path) as f: text = f.readlines()
  return "".join(text).replace("\n", "")