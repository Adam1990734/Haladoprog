from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

UPLOAD_DIR = Path("input")
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="templates")

async def get_status(request: Request, filename: str):
    status = processing_files.get(filename)

    if status is None:
        return {
            "status": "not_found"
        }

    return {
            "status": status,
            "video_name": filename
        }