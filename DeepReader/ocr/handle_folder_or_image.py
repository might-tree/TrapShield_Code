import os
import shutil
import cv2

def get_test_folder(folder_or_image_path, temp_folder_path):
  test_folder = folder_or_image_path

  # This is where we find whether the path is a file or a folder
  if not os.path.isdir(folder_or_image_path):

    # A temporary folder will be generated with image name as a folder 
    # under temporary folder
    image_name = os.path.splitext(os.path.basename(folder_or_image_path))[0]
    test_folder = os.path.join(temp_folder_path, image_name)
    #print (test_folder, folder_or_image_path) 
    # Remove if the folder exists
    if os.path.exists(test_folder):
      shutil.rmtree(test_folder)
    
    # Create the folder again
    os.makedirs(test_folder)

    test_image_path = os.path.join(test_folder, image_name + ".png")
    image = cv2.imread(folder_or_image_path)
    cv2.imwrite(test_image_path, image)

  return test_folder
