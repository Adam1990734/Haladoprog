from typing import Annotated
from fastapi import Depends, UploadFile, Form
from models.videoRequestDto import VideoRequestDto
from models.censor_mode import CensorMode

def vidoeDtoInjection(
        video: UploadFile = Form(...),
        mode: str = Form(...)
) -> VideoRequestDto:
    if mode == "beep":
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
    Depends(vidoeDtoInjection)
]