import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.video import VideoRequest, TaskCreationResponse, TaskStatusResponse
from app.services import manim_service
from app.utils import task_manager

router = APIRouter(
    prefix="/video",
    tags=["Video Generation"],
)

@router.post("/create", response_model=TaskCreationResponse, status_code=202)
async def create_video_task(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Accepts a prompt, generates Manim code, and starts the rendering
    process in the background. Returns a task ID to check for status.
    """
    try:
        manim_code = manim_service.generate_manim_code(request.prompt)
    except HTTPException as e:
        raise e

    task_id = str(uuid.uuid4())
    task_manager.create_task(task_id)

    background_tasks.add_task(manim_service.render_video_background, task_id, manim_code)

    return {
        "message": "Video generation task started.",
        "task_id": task_id,
        "status_url": f"/video/status/{task_id}",
    }

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_video_task_status(task_id: str):
    """Checks the status of a video rendering task."""
    status_info = task_manager.get_task_status(task_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Task ID not found.")
    return status_info
