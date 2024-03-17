
import cv2
#import dlib
import numpy as np

from deepface import DeepFace
import time

import tensorflow as tf
import numpy as np
import itertools


import main

def calculate_avg_color_of_slices(image: np.ndarray, rows: int, cols: int) -> list:
    """
        Calculates the average color of the slices of the image.

        Args:
            image (np.ndarray): Image to be processed
            rows (int): Number of rows
            cols (int): Number of columns

        Returns:
            list: List of the average colors
    """
    
    avg_color_list = []
    
    for i in range(rows):
        for j in range(cols):
            x1 = int(i * image.shape[0] / rows)
            x2 = int((i+1) * image.shape[0] / rows)
            y1 = int(j * image.shape[1] / cols)
            y2 = int((j+1) * image.shape[1] / cols)

            slice = image[x1:x2, y1:y2]
            avg_color = np.mean(slice, axis=(0,1))
            avg_color_list.append(avg_color)
            if False:
                cv2.rectangle(image, (y1, x1), (y2, x2), (0, 255, 0), 2)
                cv2.imshow("Image", image)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

    return avg_color_list

def get_difference_of_avg_colors(image_objects: list) -> list:
    """
        Calculates the difference of the average colors.

        Args:
            avg_color_list (list): List of the average colors

        Returns:
            list: List of the differences
    """
    diff_list = []
    processed_pairs = set()  # Set to store processed pairs
    all_pairs = generate_all_pairs(image_objects, random_flag=False)

    for i, j in all_pairs:
        # Check if the pair (i, j) or (j, i) has been processed already
        if (i, j) not in processed_pairs and (j, i) not in processed_pairs:
            
            diff = np.linalg.norm(np.array(image_objects[i].avg_image_colors) - np.array(image_objects[j].avg_image_colors))

            dict_diff = { "Result": diff, "Obj1": image_objects[i], "Obj2": image_objects[j] }
            diff_list.append(dict_diff)

            # Add the pair to the set of processed pairs
            processed_pairs.add((i, j))
    return diff_list

import random
def get_similarity(image_objet_list:list) -> None:
    """
        Calculates the similarity of the images.

        Args:
            image_list (list): List of the images
        Returns:
            None
    """
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

    result_list = []
    processed_pairs = set()  # Set to store processed pairs
    time_start = time.time()
    # randomly choose
    all_pairs = generate_all_pairs(image_objet_list, random_flag=True)

    count = 0
    
    for i, j in all_pairs:
        if (i, j) not in processed_pairs and (j, i) not in processed_pairs:
            if i==j:
                print(f"Same image: {image_objet_list[i].path}")
            f1 = image_objet_list[i].path
            f2 = image_objet_list[j].path
            try:
                result = DeepFace.verify(img1_path=f1, img2_path=f2, detector_backend=backends[0])
                result_list.append({"Result": result["distance"], "Obj1": image_objet_list[i], "Obj2": image_objet_list[j]})
            except ValueError as e:
                result = "Face_error"
                count += 1
            processed_pairs.add((i, j))

            if time.time() - time_start > 120:
                print(f"Time Out: {time.time() - time_start}")
                print(f"Face_error count: {count}")
                return result_list
    print(f"Face_error count: {count}")

    return result_list

def generate_all_pairs(image_objet_list:list, random_flag:bool) -> list:
    """
        Generates all possible pairs from the image list.

        Args:
            image_list (list): List of the images
        Returns:
            list: List of the pairs
    """
    all_pairs = list(itertools.combinations(range(len(image_objet_list)), 2))
    if random_flag:
        random.shuffle(all_pairs)
    return all_pairs
