from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join("model", "emotion_model.h5")
model = load_model(MODEL_PATH)

emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("L").resize((48, 48))
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_array = image_array.reshape(1, 48, 48, 1)
    return image_array


@app.get("/")
def root():
    return {"status": "ok", "message": "Emotion detection backend is running."}


@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    contents = await image.read()
    input_tensor = preprocess_image(contents)
    predictions = model.predict(input_tensor)
    scores = predictions[0].tolist()
    best_index = int(np.argmax(scores))
    return {
        "emotion": emotions[best_index],
        "confidence": scores[best_index],
        "scores": scores,
    }
