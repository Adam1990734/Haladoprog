from typing import Annotated
from fastapi import Depends, UploadFile
from models.videoRequestDto import VideoRequestDto
from models.censor_mode import CensorMode

def vidoeServiceInjection(video: UploadFile, mode: str) -> VideoRequestDto:
    if mode == "BEEP":
        return VideoRequestDto(
            video,
            CensorMode.BEEP
        )
    return VideoRequestDto(
        video,
        CensorMode.MUTE
    )

VideoRequestDtoDependency = Annotated[
    VideoRequestDto,
    Depends(vidoeServiceInjection)
]