from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="public/templates")


async def index(request : Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )