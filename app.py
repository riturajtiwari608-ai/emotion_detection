
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import cv2
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "emotion_model.h5")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

model = load_model(MODEL_PATH, compile=False)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


@app.get("/")
def root():
    return {"status": "ok", "message": "Emotion detection backend is running."}


@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    contents = await image.read()

    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
    frame = np.array(pil_image)

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(faces) == 0:
        return {
            "faces": [],
            "message": "No face detected"
        }

    results = []

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=(0, -1))

        predictions = model.predict(face, verbose=0)
        scores = predictions[0].tolist()
        best_index = int(np.argmax(scores))

        results.append({
            "emotion": emotions[best_index],
            "confidence": float(scores[best_index]),
            "scores": scores,
            "box": {
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }
        })

    return {
        "faces": results,
        "count": len(results)
    }