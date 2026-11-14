from fastapi import APIRouter, Request
from uuid import UUID

from controllers import homeController, statusController, uploadController
from providers.serviceInjector import VideoServiceDependency
from providers.dtoInjector import VideoRequestDtoDependency

router = APIRouter()

@router.get("/")
async def index(req : Request):
    return await homeController.index(req)

# Feltöltéshez:
@router.get("/upload")
async def uploadGet(req: Request):
    return await uploadController.get_upload(req)

@router.post("/upload")
async def uploadPost(
    req: Request,
    dto: VideoRequestDtoDependency,
    service: VideoServiceDependency
):
    return await uploadController.post_upload(req, dto, service)

# Státusz lekérdezés API:
@router.get("/api/status/{id}")
async def statusApiGET(
    req: Request,
    id: UUID,
    service: VideoServiceDependency
):
    return await statusController.get_statusAPI(req, id, service)

# Státsz igazából statikus oldal, nembiztos hogy kéne rendereltetni, de mindegy
@router.get("/status/{id}")
async def statusGET(req: Request, id: UUID):
    return await statusController.get_status(req, id)