# app/routes.py

from fastapi import APIRouter
from app.schemas import EntradaModelo, SalidaModelo

router = APIRouter()

@router.post("/predecir", response_model=SalidaModelo)
def predecir_datos(entrada: EntradaModelo):
    # Aquí es donde luego se llamará al modelo real
    suma = sum(entrada.caracteristicas)  # simulación
    return {"resultado": suma}
