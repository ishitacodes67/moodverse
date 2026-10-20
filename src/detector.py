"""Face + lightweight emotion detection (Day 1: Haar cascades).

This is a HEURISTIC detector, good enough for a demo:
  Happy   -> smile found in lower half of face
  Tired   -> face found but no open eyes found in upper half
  Neutral -> everything else
Day 2/3 upgrade: swap `analyze_face` for an ONNX model (HSEmotion).
Keep the same return type so the UI does not change.
"""
from dataclasses import dataclass
import cv2
import numpy as np

_FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
_SMILE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
_EYES = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


@dataclass
class FaceResult:
    box: tuple          # (x, y, w, h)
    emotion: str        # Happy | Neutral | Tired
    confidence: float   # 0..1 (heuristic, not a calibrated probability)


def analyze_face(gray_face: np.ndarray) -> tuple[str, float]:
    h, w = gray_face.shape
    lower = gray_face[h // 2:, :]
    upper = gray_face[: h // 2, :]
    smiles = _SMILE.detectMultiScale(lower, scaleFactor=1.7, minNeighbors=22, minSize=(w // 4, h // 12))
    if len(smiles) > 0:
        return "Happy", min(0.6 + 0.1 * len(smiles), 0.95)
    eyes = _EYES.detectMultiScale(upper, scaleFactor=1.1, minNeighbors=8, minSize=(w // 8, h // 8))
    if len(eyes) == 0:
        return "Tired", 0.55
    return "Neutral", 0.65


def detect(image_bgr: np.ndarray) -> list[FaceResult]:
    gray = cv2.equalizeHist(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY))
    faces = _FACE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    results = []
    for (x, y, w, h) in faces:
        emotion, conf = analyze_face(gray[y:y + h, x:x + w])
        results.append(FaceResult((int(x), int(y), int(w), int(h)), emotion, conf))
    return results


def annotate(image_bgr: np.ndarray, results: list[FaceResult], blur: bool = False) -> np.ndarray:
    """Draw boxes + labels. If blur=True the face is blurred (privacy mode)."""
    out = image_bgr.copy()
    for r in results:
        x, y, w, h = r.box
        if blur:
            out[y:y + h, x:x + w] = cv2.GaussianBlur(out[y:y + h, x:x + w], (51, 51), 30)
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 200, 120), 2)
        cv2.putText(out, f"{r.emotion} {r.confidence:.0%}", (x, max(y - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 120), 2)
    return out
