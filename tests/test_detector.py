import numpy as np
from src.detector import detect

def test_detect_empty_image():
    """Test that a None image returns Neutral with 0 confidence."""
    mood, confidence, img = detect(None)
    assert mood == "Neutral"
    assert confidence == 0.0
    assert img is None

def test_detect_no_face():
    """Test that a blank image (no face) returns Neutral with 0 confidence."""
    # Create a blank black image (100x100 pixels, 3 color channels)
    blank_image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    mood, confidence, img = detect(blank_image)
    
    assert mood == "Neutral"
    assert confidence == 0.0
    assert img is not None  # Should return the original image array