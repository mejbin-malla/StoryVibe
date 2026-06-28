"""
model.py
--------
Defines and loads the FER (Facial Expression Recognition) CNN.

Architecture confirmed from model.h5 weight inspection:
  Input  : (48, 48, 1)  — grayscale face / full image
  Conv1  : 32 filters, 3×3, relu   → 46×46×32
  Conv2  : 64 filters, 3×3, relu   → 44×44×64
  Pool1  : MaxPool 2×2              → 22×22×64
  Drop1  : 0.25
  Conv3  : 128 filters, 3×3, relu  → 20×20×128
  Pool2  : MaxPool 2×2             → 10×10×128
  Conv4  : 128 filters, 3×3, relu  →  8× 8×128
  Pool3  : MaxPool 2×2             →  4× 4×128
  Drop2  : 0.25
  Flatten:                          → 2 048
  Dense1 : 1 024, relu
  Drop3  : 0.5
  Dense2 : 7, softmax               → emotion probabilities
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dropout, Flatten, Dense
)

# ── Emotion labels (index matches model output) ──────────────────────────────
EMOTION_LABELS = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised",
}

# ── Map 7-class model output → 5 mood buckets used for recommendations ───────
EMOTION_TO_MOOD = {
    "Angry":     "Angry",
    "Disgusted": "Angry",      # closest bucket
    "Fearful":   "Fear",
    "Happy":     "Happy",
    "Neutral":   "Neutral",
    "Sad":       "Sad",
    "Surprised": "Happy",      # closest bucket
}

IMG_SIZE = 48  # model input side length (pixels)


def build_model() -> Sequential:
    """Return the CNN with the exact architecture used during training."""
    m = Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),

        # Block 2
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),

        # Block 3
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),

        # Classifier head
        Flatten(),
        Dense(1024, activation="relu"),
        Dropout(0.5),
        Dense(7, activation="softmax"),
    ])
    return m


def load_model(weights_path: str = "./model.h5") -> Sequential:
    """Build architecture and load pre-trained weights."""
    m = build_model()
    m.load_weights(weights_path)
    return m


def preprocess_image(bgr_image: np.ndarray) -> np.ndarray:
    """
    Convert a BGR OpenCV image to the tensor expected by the model.
    Returns shape (1, 48, 48, 1) float32 with raw uint8 values (0-255).
    The model was trained without normalisation so we keep pixel range as-is.
    """
    import cv2
    gray    = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
    tensor  = np.expand_dims(np.expand_dims(resized, -1), 0).astype("float32")
    return tensor


def predict_emotions(model: Sequential, bgr_image: np.ndarray,
                     top_n: int = 3, min_confidence: float = 0.10):
    """
    Run inference on a full BGR image.

    Returns
    -------
    emotions : list[str]
        Up to `top_n` raw emotion labels (e.g. ["Happy", "Neutral"]).
    moods : list[str]
        Same list mapped to the 5 recommendation buckets (deduplicated).
    confidences : dict[str, float]
        Raw softmax scores for all 7 classes.
    """
    tensor      = preprocess_image(bgr_image)
    probs       = model.predict(tensor, verbose=0)[0]
    confidences = {EMOTION_LABELS[i]: float(probs[i]) for i in range(7)}

    # Top-N emotions above the confidence threshold
    top_indices = np.argsort(probs)[::-1]
    emotions    = [
        EMOTION_LABELS[i]
        for i in top_indices[:top_n]
        if probs[i] >= min_confidence
    ]
    if not emotions:                          # fallback: always return at least 1
        emotions = [EMOTION_LABELS[int(np.argmax(probs))]]

    # Map to mood buckets, deduplicate while preserving order
    seen, moods = set(), []
    for e in emotions:
        m = EMOTION_TO_MOOD[e]
        if m not in seen:
            seen.add(m)
            moods.append(m)

    return emotions, moods, confidences
