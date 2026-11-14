from pathlib import Path
from model.videoStatus import VideoStatus

class VideoResponseDto:
    resultPath: Path

    status: VideoStatus
    
    errorMessage: str | None

    def __init__(self, status: VideoStatus):
        self.status = status
        self.errorMessage = None

    def setResultPath(self, result_path: Path):
        self.resultPath = result_path

    def setStatus(self, status: VideoStatus):
        self.status = status

    def setErroMessage(self, message: str):
        self.errorMessage = message

    def getResultPath(self):
        return self.resultPath

    def getStatus(self):
        return self.status

    def getErrorMessage(self):
        return self.errorMessage