import numpy as np
from src.detector import detect, annotate


def test_blank_image_has_no_faces():
    img = np.zeros((240, 320, 3), dtype=np.uint8)
    assert detect(img) == []


def test_annotate_keeps_shape():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    assert annotate(img, []).shape == img.shape
