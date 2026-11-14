from typing import Annotated
from fastapi import Depends, UploadFile
from models.videoRequestDto import VideoRequestDto

def vidoeServiceInjection(video: UploadFile) -> VideoRequestDto:
    return VideoRequestDto(
        video
    )

VideoRequestDtoDependency = Annotated[
    VideoRequestDto,
    Depends(vidoeServiceInjection)
]