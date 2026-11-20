from fastapi import Request
from fastapi.templating import Jinja2Templates

from config import Configs as cf

templates = Jinja2Templates(directory=str(cf.TEMPLATES))


async def index(request : Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )