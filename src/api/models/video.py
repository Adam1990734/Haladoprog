from pathlib import Path
from uuid import UUID
from models.videoStatus import VideoStatus

class Video:
    id: UUID
    
    originalFilename: str

    uploadPath: Path

    resultPath: Path | None = None

    status: VideoStatus = VideoStatus.UPLOADED

    errorMessage: str | None = None