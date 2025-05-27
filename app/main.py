from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_routes import router as auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.history import router as history_router
app = FastAPI(title="Weather Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки разрешаем все (в проде - ограничить)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/auth")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", include_in_schema=False)
def serve_root():
    return FileResponse("frontend/login.html")

@app.get("/index.html", include_in_schema=False)
def index_page():
    return FileResponse("frontend/index.html")

@app.get("/register.html", include_in_schema=False)
def register_page():
    return FileResponse("frontend/register.html")



app.include_router(history_router, prefix="/api/v1")

