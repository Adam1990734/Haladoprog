from fastapi import UploadFile
from models.censor_mode import CensorMode

class VideoRequestDto:
    __file: UploadFile
    __mode: CensorMode

    def __init__(
        self,
        file: UploadFile,
        mode: CensorMode
    ):
        self.__file = file
        self.__mode = mode

    def getFilename(self) -> str:
        return self.__file.filename

    def getType(self) -> str:
         return self.__file.content_type

    def getFile(self) -> UploadFile:
        return self.__file

    def getMode(self) -> CensorMode:
        return self.__mode
    