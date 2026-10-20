import cv2
import numpy as np

# Load the pre-trained Haar Cascades from OpenCV's built-in data
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
SMILE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_smile.xml"

face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
smile_cascade = cv2.CascadeClassifier(SMILE_CASCADE_PATH)

def detect(image: np.ndarray):
    """
    Takes an image (RGB from Streamlit), detects a face, and guesses the mood.
    Returns: mood (str), confidence (float), annotated_image (np.ndarray)
    """
    if image is None:
        return "Neutral", 0.0, None

    # Convert RGB (Streamlit) to BGR (OpenCV) then to Grayscale for detection
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return "Neutral", 0.0, image

    # We only take the first face for simplicity
    (x, y, w, h) = faces[0]
    
    # Focus on the lower half of the face for smiles
    roi_gray = gray[y + h//2 : y + h, x : x + w]

    # Detect smiles in the lower half of the face
    # Tuned threshold: minNeighbors=20 prevents false positives
    smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

    mood = "Neutral"
    confidence = 0.5
    
    if len(smiles) > 0:
        # Added 5th Mood logic: Check the shape of the detected mouth
        (sx, sy, sw, sh) = smiles[0]
        
        # If the mouth is very tall/round, it's likely a surprised "O" shape
        if sh > sw * 0.8: 
            mood = "Surprised"
            confidence = 0.75
        else:
            mood = "Happy"
            confidence = 0.85
    else:
        # Simple heuristic: If face is small or low in frame, assume Tired
        if h < 100 or y > 300:
            mood = "Tired"
            confidence = 0.6
            
    # Annotate the image to show the detection
    annotated_img = annotate(img_bgr, faces[0], mood)

    # Convert back to RGB for Streamlit
    annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

    return mood, confidence, annotated_img_rgb


def annotate(img, face_rect, mood):
    """
    Draws a rectangle around the face and puts the mood text on the image.
    """
    (x, y, w, h) = face_rect
    
    # Draw rectangle around face
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Add mood text above the face
    cv2.putText(img, mood, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return img