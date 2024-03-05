import os
import cv2
import numpy as np
import shutil

def cut_lines_from_image(image_path, all_coords, folder_to_write):
  
  # Creating path to store the result
  destination_folder_path = os.path.join(folder_to_write, os.path.splitext(os.path.basename(image_path))[0])
  if os.path.exists(destination_folder_path):
    shutil.rmtree(destination_folder_path)
  os.makedirs(destination_folder_path)
  
  # Reading in the image  
  image = cv2.imread(image_path)

  for a_coord in all_coords:
    x_coords, y_coords = [],[]
    size_too_small = False
    for i in range(len(a_coord)):
      if i%2 == 0:
        x_coords.append(a_coord[i])
      else:
        y_coords.append(a_coord[i])
    x_min, y_min, x_max, y_max = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
    
    '''
    Tesseract won't process the image if either its height or width is less than
    3 pixels wide
    '''
    if ((x_max - x_min) <= 3) or ((y_max - y_min) <= 3):
      size_too_small = True
      continue
    
    # The coordinates are relative to the image
    # we are making them relative to a patch
    new_coords = []
    for i in range(len(a_coord)):
      if i%2 == 0:
        new_coords.append(a_coord[i] - x_min)
      else:
        new_coords.append(a_coord[i] - y_min)

    if size_too_small:
      continue
    cropped_image = 255 - image[int(y_min) : int(y_max), int(x_min) : int(x_max)]

    # Creating an empty mask
    mask = np.zeros((cropped_image.shape[:2]), dtype=np.uint8)

    points_array = np.array(new_coords).reshape(-1, 2)
    cv2.drawContours(mask, [points_array], -1, 255 ,-1, cv2.LINE_AA)
    
    # Applying the mask
    dst = cv2.bitwise_and(cropped_image, cropped_image, mask=mask)

    dst = cv2.copyMakeBorder(dst, 5,5,5,5, borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    destination_path = os.path.join(destination_folder_path, "{}_{}_{}_{}.png".format(x_min, y_min, x_max, y_max))
    cv2.imwrite(destination_path,255 - dst)