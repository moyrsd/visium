# app/services/manim_service.py
import os
import shutil
import subprocess

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings
from app.utils import task_manager


genai.configure(api_key=settings.GOOGLE_API_KEY)

def generate_manim_code(prompt: str) -> str:
    """Uses the Gemini LLM to generate Manim code from a natural language prompt."""
    meta_prompt = f"""
    You are an expert Manim programmer. Your task is to write a Python script that fulfills the user's request.

    **INSTRUCTIONS:**
    - The script must be a single, complete piece of Python code.
    - It must import from the `manim` library (`from manim import *`).
    - It must contain exactly one class that inherits from `manim.Scene`.
    - The name of that class **MUST** be `GeneratedScene`.
    - Do not include any explanation, comments, or markdown formatting; provide only the raw Python code.
    - Only provide the code that generates the animation as specified in the user's request.

    **USER REQUEST:**
    "{prompt}"

    **PYTHON SCRIPT:**
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(meta_prompt)
        generated_code = response.text.strip()
        fixing_prompt = f"""Please ensure the generated code meets the following requirements:
        - It must be a complete, runnable Python script.
        - It must import from the `manim` library (`from manim import *`).
        - It must contain exactly one class that inherits from `manim.Scene`.
        - The name of that class **MUST** be `GeneratedScene`.
        - Do not include any explanation, comments, or markdown formatting; provide only the raw Python code.
        - Only provide the code that generates the animation as specified in the user's request.

        **USER REQUEST:**
        "{prompt}"
        **PYTHON SCRIPT:**  
        {generated_code}
        **Instructions:**
        Please ensure the code is valid and meets the requirements above.
        If it does not, rewrite it to ensure it meets these requirements.
        """
        response = model.generate_content(fixing_prompt)
        generated_code = response.text.strip()
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        return generated_code.strip()

    except Exception as e:
        print(f"Error during AI generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate animation code from the AI model.")


def render_video_background(task_id: str, code: str):
    """
    Saves Manim code to a file and renders it. This is run in the background.
    It updates the task status via the task_manager.
    """
    task_manager.set_task_status(task_id, "rendering", "Video rendering in progress.")
    
    script_path = settings.TEMP_SCRIPT_DIR / f"{task_id}.py"
    temp_media_dir = settings.TEMP_SCRIPT_DIR / task_id
    
    try:
        with open(script_path, "w") as f:
            f.write(code)

        command = [
            "manim",
            str(script_path),
            "GeneratedScene",
            "-ql",  # Low quality for speed
            "--media_dir", str(temp_media_dir)
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Manim STDOUT for {task_id}:", result.stdout)
        
        manim_output_file = temp_media_dir / "videos" / script_path.stem / "480p15" / "GeneratedScene.mp4"
        
        if not manim_output_file.exists():
            raise FileNotFoundError("Manim did not produce the expected output file.")

        final_video_path = settings.VIDEO_DIR / f"{task_id}.mp4"
        shutil.move(str(manim_output_file), str(final_video_path))

        task_manager.set_task_status(
            task_id,
            "completed",
            "Video rendering finished successfully.",
            video_url=f"/static/videos/{task_id}.mp4"
        )

    except subprocess.CalledProcessError as e:
        print(f"Manim rendering failed for task {task_id}. STDERR: {e.stderr}")
        task_manager.set_task_status(task_id, "failed", f"Manim rendering failed: {e.stderr[:200]}...")
    except Exception as e:
        print(f"An unexpected error occurred during rendering for task {task_id}: {e}")
        task_manager.set_task_status(task_id, "failed", f"An unexpected error occurred: {str(e)}")
    finally:
        if script_path.exists():
            os.remove(script_path)
        if temp_media_dir.exists():
            shutil.rmtree(temp_media_dir)
