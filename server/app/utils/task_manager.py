from typing import Dict, Any

# A simple in-memory dictionary to track the status of background tasks.
# In a production system, this would be replaced with redis or a database for persistence.
task_statuses: Dict[str, Dict[str, Any]] = {}

def get_task_status(task_id: str) -> Dict[str, Any] | None:
    """Retrieves the status of a task."""
    return task_statuses.get(task_id)

def set_task_status(task_id: str, status: str, message: str, video_url: str | None = None):
    """Sets or updates the status of a task."""
    task_statuses[task_id] = {
        "status": status,
        "message": message,
        "video_url": video_url,
    }

def create_task(task_id: str):
    """Initializes a task in the 'pending' state."""
    set_task_status(task_id, "pending", "Task received and is waiting to be processed.")
