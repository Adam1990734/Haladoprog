from fastapi import APIRouter, Request

from controller import mainController

router = APIRouter()

@router.get("/")
async def index(request : Request):
    return await mainController.index(request)