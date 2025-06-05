# # Usa una imagen base ligera de Python
# FROM python:3.11-slim

# # Establece el directorio de trabajo
# WORKDIR /app

# # Copia los archivos al contenedor
# COPY . .

# # Instala las dependencias
# RUN pip install --no-cache-dir -r requirements.txt

# # Expone el puerto 8000 para acceder a la API
# EXPOSE 8000

# # Comando para ejecutar la app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
