from pathlib import Path
from uuid import UUID, uuid4
from fastapi import UploadFile

from models.video import Video
from models.videoRequestDto import VideoRequestDto
from models.videoResponseDto import VideoResponseDto
from models.videoStatus import VideoStatus



class VideoService:
    __INPUT = "../input"
    __OUTPUT = "../output"

    async def upload(self, file: UploadFile) -> VideoResponseDto:
        videoId = str(uuid4())

        target = self.__INPUT / f"{videoId}.mp4"

        with open(target, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return VideoResponseDto(
            VideoStatus.UPLOADED
        )

    async def getStatus(self, id: UUID) -> VideoResponseDto:
        inputFilePath = Path(self.__INPUT / f"{id}.mp4")
        outputFilePath = Path(self.__OUTPUT / f"{id}_censored.mp4")
        resp = VideoResponseDto()
        resp.setResultPath(outputFilePath)

        if not inputFilePath.exists() and not outputFilePath.exists():
            resp.setStatus(
                VideoStatus.FAILED
            )
            resp.errorMessage("Faild to load the pictiure up!")
            return resp
        
        if inputFilePath.exists() and not outputFilePath.exists():
            resp.setStatus(
                VideoStatus.UPLOADED
            )
            return resp

        if inputFilePath.exists() and outputFilePath.exists():
            resp.setStatus(
                VideoStatus.COMPLETED
            )
            return resp

    async def startProcessig(self, id: UUID) -> VideoResponseDto:
        outputFilePath = Path(self.__OUTPUT / f"{id}_censored.mp4")
        resp = VideoResponseDto()
        resp.setResultPath(outputFilePath)
        resp.setStatus(
            VideoStatus.PROCESSING
        )
        return resp

    async def removeFromInput(self, id: UUID) -> None:
        filePath = Path(self.__INPUT / f"{id}_censored.mp4")
        if not filePath.exists():
            raise FileExistsError("The given file is not exists!")
        filePath.unlink()

    async def removeFromOutput(self, id: UUID) -> None:
        filePath = Path(self.__OUTPUT / f"{id}_censored.mp4")
        if not filePath.exists():
            raise FileExistsError("The given file is not exists!")
        filePath.unlink()

    # Jelen esetben nincs semmi szükség rá, de jól jöhet,
    # ha adatbázist is be vezetnénk meta adatok tárolására szerint jól jöhet talán.
    @staticmethod
    def toRespDto(video: Video) -> VideoResponseDto:
        result = VideoResponseDto()
        result.setStatus(video.status)
        result.setErroMessage(video.errorMessage)
        result.setResultPath(video.resultPath)
        return result

    # Middleware-be tervezem mint DI és validálási szempontok szerint
    @staticmethod
    def toReqDto(video: UploadFile) -> VideoRequestDto:
        return VideoRequestDto(
            video
        )