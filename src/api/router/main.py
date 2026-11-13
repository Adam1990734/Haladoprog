from fastapi import APIRouter, Request

from api.controller import homeController

router = APIRouter()

@router.get("/")
async def index(request : Request):
    return await homeController.index(request)