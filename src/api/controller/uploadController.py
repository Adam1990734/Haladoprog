from pathlib import Path
import shutil

from fastapi import File, UploadFile, Request
from fastapi.templating import Jinja2Templates

UPLOAD_DIR = Path("input")
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="templates")

async def get_upload_page(request: Request):
    return templates.TemplateResponse(
        request,
        "upload.html"
    )

async def post_upload_video(
    request: Request,
    video: UploadFile = File(...)
):
    allowed_extensions = { ".mp4", ".avi" }

    extension = Path(video.filename).suffix.lower()

    if extension not in allowed_extensions:
        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "error": "Not supported format (mp4, avi).",
                "filename": ""
            }
        )

    

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "error": "",
            "filename": video.filename
        }
    )