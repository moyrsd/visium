from pydantic import BaseModel, Field

class VideoRequest(BaseModel):
    """The request model for creating a new video."""
    prompt: str = Field(
        ...,
        min_length=10,
        max_length=600,
        description="A natural language prompt describing the animation.",
        example="Show a blue circle transforming into a red square.",
    )

class TaskCreationResponse(BaseModel):
    """The response model after submitting a video generation request."""
    message: str
    task_id: str
    status_url: str

class TaskStatusResponse(BaseModel):
    """The model for checking the status of a rendering task."""
    status: str
    message: str
    video_url: str | None = None
