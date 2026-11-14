from uuid import UUID
from pathlib import Path
from models.videoStatus import VideoStatus

class VideoResponseDto:
    id: UUID

    resultPath: Path | None

    status: VideoStatus
    
    errorMessage: str | None

    def __init__(self, id: UUID, status: VideoStatus = VideoStatus.PROCESSING):
        self.id = id
        self.resultPath = None
        self.status = status
        self.errorMessage = None

    def setResultPath(self, result_path: Path) -> Path | None:
        self.resultPath = result_path

    def setStatus(self, status: VideoStatus) -> None:
        self.status = status

    def setErroMessage(self, message: str) -> None:
        self.errorMessage = message

    def getId(self) -> UUID:
        return self.id

    def getResultPath(self) -> Path:
        return self.resultPath

    def getStatus(self) -> VideoStatus:
        return self.status

    def getErrorMessage(self) -> str:
        return self.errorMessage