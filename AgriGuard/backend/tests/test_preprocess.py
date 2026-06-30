"""Unit tests for image preprocessing pipeline."""

import os

import numpy as np
import pytest

from preprocess import extract_leaf, load_image, normalize_image, preprocess, resize_image


def _create_synthetic_image(height: int = 128, width: int = 128) -> np.ndarray:
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)


def _save_temp_image(tmp_path, img: np.ndarray, name: str = "test.jpg") -> str:
    import cv2

    path = os.path.join(tmp_path, name)
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, bgr)
    return path


class TestLoadImage:
    def test_load_valid_image(self, tmp_path):
        img = _create_synthetic_image()
        path = _save_temp_image(tmp_path, img)
        result = load_image(path)
        assert result.shape == (128, 128, 3)
        assert result.dtype == np.uint8

    def test_load_invalid_path(self):
        with pytest.raises(ValueError, match="Could not read image"):
            load_image("nonexistent_file.jpg")


class TestExtractLeaf:
    def test_extract_leaf_output_shape(self):
        img = _create_synthetic_image()
        result = extract_leaf(img)
        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_extract_leaf_green_image(self):
        img = np.zeros((128, 128, 3), dtype=np.uint8)
        img[:, :] = [50, 150, 50]
        result = extract_leaf(img)
        assert np.any(result > 0)


class TestResizeImage:
    def test_resize_to_smaller(self):
        img = _create_synthetic_image(256, 256)
        result = resize_image(img, (64, 64))
        assert result.shape == (64, 64, 3)

    def test_resize_to_larger(self):
        img = _create_synthetic_image(32, 32)
        result = resize_image(img, (128, 128))
        assert result.shape == (128, 128, 3)

    def test_resize_preserves_channels(self):
        img = _create_synthetic_image(100, 200)
        result = resize_image(img, (50, 50))
        assert result.shape[2] == 3


class TestNormalizeImage:
    def test_normalize_dtype(self):
        img = _create_synthetic_image()
        result = normalize_image(img)
        assert result.dtype == np.float32

    def test_normalize_range(self):
        img = np.full((64, 64, 3), 128, dtype=np.uint8)
        result = normalize_image(img)
        assert np.allclose(result, 128.0)


class TestPreprocess:
    def test_preprocess_default(self, tmp_path):
        img = _create_synthetic_image(256, 256)
        path = _save_temp_image(tmp_path, img)
        result = preprocess(path)
        assert result.shape == (1, 64, 64, 3)
        assert result.dtype == np.float32

    def test_preprocess_custom_size(self, tmp_path):
        img = _create_synthetic_image(256, 256)
        path = _save_temp_image(tmp_path, img)
        result = preprocess(path, target_size=(128, 128))
        assert result.shape == (1, 128, 128, 3)

    def test_preprocess_with_leaf_extraction(self, tmp_path):
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:, :] = [50, 180, 50]
        path = _save_temp_image(tmp_path, img)
        result = preprocess(path, extract_leaf_region=True)
        assert result.shape == (1, 64, 64, 3)

    def test_preprocess_invalid_path(self):
        with pytest.raises(ValueError):
            preprocess("nonexistent.jpg")

    def test_preprocess_batch_independence(self, tmp_path):
        img1 = _create_synthetic_image(100, 100)
        img2 = _create_synthetic_image(100, 100)
        path1 = _save_temp_image(tmp_path, img1, "test1.jpg")
        path2 = _save_temp_image(tmp_path, img2, "test2.jpg")
        r1 = preprocess(path1)
        r2 = preprocess(path2)
        assert r1.shape == r2.shape
        assert r1.dtype == r2.dtype
