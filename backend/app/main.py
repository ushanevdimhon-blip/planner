from fastapi import FastAPI

from app.api import api_router
from app.core.exceptions import register_exception_handlers
from app.core.logger import setup_logger

def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI()

    register_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) # http://localhost:8000/docs
