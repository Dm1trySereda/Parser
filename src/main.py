from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from src.middleware.middleware import db_session_middleware
from src.routes.book_routes import book_router
from src.routes.history_routes import history_routes
from src.routes.user_routes import user_routes
from src.routes.google_auth_routes import google_routes

app = FastAPI(
    title="OZ Books App",
)
templates = Jinja2Templates(directory="src/templates")

app.middleware("http")(db_session_middleware)
app.include_router(google_routes)
app.include_router(user_routes)
app.include_router(book_router)
app.include_router(history_routes)

