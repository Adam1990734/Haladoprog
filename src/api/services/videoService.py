from model.video import Video
from model.videoRequestDto import VideoRequestDto
from model.videoResponseDto import VideoResponseDto

import shutil
from fastapi import File

class VideoService:
    __INPUT = "../input"
    __OUTPUT = "../output"

    def upload(self, file : File) -> VideoResponseDto:
        file_path = self.__INPUT / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file, buffer)

    def remove(self, file : str) -> None:
        file_path = self.__OUTPUT / file
        if not file_path.exists():
            raise FileExistsError("The given file is not exists!")
        file_path.unlink()

    def exist(self, file : str) -> bool:
        file_path = self.__OUTPUT / file
        return file_path.exists()

    @staticmethod
    def toRespDto(video: Video) -> VideoResponseDto:
        return VideoResponseDto(
            video.name,
            video.file
        )

    @staticmethod
    def toReqDto(video: Video) -> VideoRequestDto:
        return VideoRequestDto(
            video.file
        )