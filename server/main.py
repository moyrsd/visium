from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import video as video_router
from app.core.config import settings

app = FastAPI(
    title="Visium AI Video Generator",
    description="An API to generate 3b1b-style videos from text prompts, with a clean project structure.",
    version="0.3.0",
)

settings.setup_directories()
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.include_router(video_router.router)


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the server is running."""
    return {"message": "Visium AI Video Generator is running. Go to /docs for the API."}


