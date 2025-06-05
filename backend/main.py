from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes import auth

load_dotenv()  # This loads the .env file into environment variables


app = FastAPI()

# manejo de OPTIONS (cors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # frontend local
        "http://127.0.0.1:3000",
        "http://172.20.100.143",  # esta el la red de NGINX 
        # "https://tunetunetune.com",  <-- dominio para producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")