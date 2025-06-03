# app/main.py
# Es el corazón de la aplicación, crea la instancia principal de la app (punto de dentrada de backend)
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="API de Predicción IA")

# Incluir las rutas definidas en otro archivo
# Se inportan las rutas 
app.include_router(router)

@app.get("/") # se define una raíz para verificar que esta funcionando adecuadamente.
def home():
    return {"mensaje": "Bienvenido a la API de IA"}
