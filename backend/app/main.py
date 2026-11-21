from fastapi import FastAPI

from app.api import api_router
from app.core.exceptions import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI()

    register_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) # http://localhost:8000/docs
