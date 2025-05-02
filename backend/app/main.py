from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, users, chatbot
from .utils.database import engine, Base
from .config import settings

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Sistema web de guía y gestión en trámites legales civiles con machine learning"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Bienvenido al Sistema de Asistencia Legal"}