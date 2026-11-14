from fastapi import UploadFile

class VideoRequestDto:
    __file : UploadFile

    def __init__(
        self,
        file: UploadFile
    ):
        self.__file = file

    def getFilename(self) -> str:
        return self.__file.filename

    def getType(self) -> str:
         return self.__file.content_type

    def getFile(self) -> UploadFile:
        return self.__file
    