# predict.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow import keras
from jwt_utils import jwt, SECRET_KEY, ALGORITHM
from datetime import datetime
from database import db

router = APIRouter()
security = HTTPBearer()

# Load model once
# Get the current directory of this file (routes/predict.py)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the model relative to this file
MODEL_PATH = os.path.join(CURRENT_DIR, "..", "1kGenres", "genre_classifier_modelV3.keras")

# Normalize the path
MODEL_PATH = os.path.normpath(MODEL_PATH)

# Load the model
model = keras.models.load_model(MODEL_PATH)
labels = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # user email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/predict")
async def predict_genre(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Only WAV files are supported")

    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Load audio
    y, sr = librosa.load(temp_path, duration=30.0, res_type="soxr_hq")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T

    # Padding/truncating
    desired_length = 1300
    if mfcc.shape[0] < desired_length:
        pad = desired_length - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad), (0, 0)), mode="constant")
    else:
        mfcc = mfcc[:desired_length, :]

    # Predict
    input_tensor = mfcc[np.newaxis, ...]  # shape (1, 1300, 40)
    prediction = model.predict(input_tensor)
    index = np.argmax(prediction)
    confidence = float(prediction[0][index])
    genre = labels[index]

    # Log in DB
    await db["predictions"].insert_one({
        "user": user,
        "genre": genre,
        "confidence": confidence,
        "timestamp": datetime.utcnow(),
        "filename": file.filename
    })

    # Clean up temp file
    os.remove(temp_path)

    return {"genre": genre, "confidence": confidence}

