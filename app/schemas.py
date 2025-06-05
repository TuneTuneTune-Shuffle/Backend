# app/schemas.py

from pydantic import BaseModel
from typing import List

class EntradaModelo(BaseModel):
    caracteristicas: List[float]

class SalidaModelo(BaseModel):
    resultado: float
