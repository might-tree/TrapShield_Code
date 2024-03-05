def get_coordinates(file_path):
  all_content = []
  with open(file_path, "r") as f:
    all_content = f.readlines()
  
  for i in range(len(all_content)):
    all_content[i] = [int(coord) for coord in all_content[i].replace("\r", "").replace("\n", "").split(",")]

  return all_content
  