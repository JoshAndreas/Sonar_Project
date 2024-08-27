import json


class JsonFileHandler:
  def read_from_file(file_name: str):
    with open(file_name, "r") as json_file:
      data = json.loads(json_file.read())
    return data

  def dump_to_file(file_name: str, data, sort_keys: bool = True, indent: int = 2):
    with open(file_name, "w") as json_file:
      json_file.write("%s\n" % json.dumps(data, sort_keys=sort_keys, indent=indent))
      print(f">> Writing in {file_name} completed.")
    return data
