from typing import Annotated
from fastapi import Depends

from config import Configs
from services.videoService import VideoService

def vidoeServiceInjection() -> VideoService:
    return VideoService(
        Configs.INPUT,
        Configs.OUTPUT
    )

VideoServiceDependency = Annotated[
    VideoService,
    Depends(vidoeServiceInjection)
]