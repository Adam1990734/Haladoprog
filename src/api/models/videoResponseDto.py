from uuid import UUID
from pathlib import Path
from models.videoStatus import VideoStatus

class VideoResponseDto:
    id: UUID

    status: VideoStatus
    
    errorMessage: str | None

    def __init__(self, id: UUID, status: VideoStatus = VideoStatus.PROCESSING):
        self.id = id
        self.status = status
        self.errorMessage = None

    def setStatus(self, status: VideoStatus) -> None:
        self.status = status

    def setErroMessage(self, message: str) -> None:
        self.errorMessage = message

    def getId(self) -> UUID:
        return self.id

    def getStatus(self) -> VideoStatus:
        return self.status

    def getErrorMessage(self) -> str:
        return self.errorMessage