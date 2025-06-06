# %%
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Desactiva GPU
os.environ["TF_XLA_FLAGS"] = "--tf_xla_enable_xla_devices=false"  # Desactiva compilación JIT
import tensorflow as tf
from tensorflow import keras
import librosa
import numpy as np
import pyaudio
import wave

# %%
def grabar_audio(nombre_archivo="grabacion.wav", duracion=30, sample_rate=22050):
    formato = pyaudio.paInt16
    canales = 1
    chunk = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(format=formato, channels=canales,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk)

    print("🎙️ Grabando durante", duracion, "segundos...")
    frames = []

    for _ in range(0, int(sample_rate / chunk * duracion)):
        data = stream.read(chunk)
        frames.append(data)

    print("✅ Grabación terminada.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(nombre_archivo, 'wb') as wf:
        wf.setnchannels(canales)
        wf.setsampwidth(audio.get_sample_size(formato))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


# %%
def audio_a_mfcc(archivo_audio, max_pad_len=862):  # ajusta este valor a tu dataset
    y, sr = librosa.load(archivo_audio, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

    if mfcc.shape[1] < max_pad_len:
        pad_width = max_pad_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_pad_len]
        
    return mfcc


# %%
def predecir_genero_desde_audio(audio_path, modelo, etiquetas=None):
    # Paso 1: Cargar audio y extraer MFCC
    audio_series, sample_rate = librosa.load(audio_path, duration=30.0, res_type="soxr_hq")
    mfcc = librosa.feature.mfcc(y=audio_series, sr=sample_rate, n_mfcc=40).T

    # Paso 2: Padding o recorte
    desired_length = 1300
    if mfcc.shape[0] < desired_length:
        pad_width = desired_length - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)), mode='constant')
    elif mfcc.shape[0] > desired_length:
        mfcc = mfcc[:desired_length, :]

    # Paso 3: Expandir dimensión para batch
    entrada = mfcc[np.newaxis, ...]  # (1, 1300, 40)

    # Paso 4: Predecir
    prediccion = modelo.predict(entrada)
    indice = np.argmax(prediccion)
    confianza = prediccion[0][indice]
    genero = etiquetas[indice] if etiquetas else indice
    return genero, confianza


# %%
# Cargar el modelo
modelo = keras.models.load_model("genre_classifier_model.keras")

# Opcional: etiquetas si las tienes
etiquetas = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]  # por ejemplo

# Grabar
grabar_audio("grabacion.wav", duracion=30)

# %%
# Procesar
mfcc = audio_a_mfcc("grabacion.wav")

# %%
# Predecir
genero, confianza = predecir_genero_desde_audio("grabacion.wav", modelo, etiquetas)
print(f"🎵 Género detectado: {genero} (confianza: {confianza:.2f})")



