"""
Offline image preprocessing for crop disease detection.
Uses OpenCV only — resize, normalize, optional leaf extraction.
"""

import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def extract_leaf(img: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_green = np.array([25, 30, 30])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result


def resize_image(img: np.ndarray, target_size: tuple[int, int]) -> np.ndarray:
    return cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)


def normalize_image(img: np.ndarray) -> np.ndarray:
    return img.astype(np.float32) / 255.0


def preprocess(
    image_path: str,
    target_size: tuple[int, int] = (64, 64),
    extract_leaf_region: bool = False,
) -> np.ndarray:
    img = load_image(image_path)
    if extract_leaf_region:
        img = extract_leaf(img)
    img = resize_image(img, target_size)
    img = normalize_image(img)
    return np.expand_dims(img, axis=0)
