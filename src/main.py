from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.db_session_middleware import db_session_middleware
from src.routes.book_routes import book_routers
from src.routes.google_auth_routes import google_routes
from src.routes.history_routes import history_routes
from src.routes.user_routes import user_routes

app = FastAPI(
    title="OZ Books App",
)
templates = Jinja2Templates(directory="src/templates")

app.middleware("http")(db_session_middleware)

app.include_router(google_routes)
app.include_router(user_routes)
app.include_router(book_routers)
app.include_router(history_routes)

origins = [
    "http://localhost:3000",  # Фронт
    "http://localhost:8000",  # Бек
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы 
    allow_headers=["*"],  # Разрешить все заголовки
)