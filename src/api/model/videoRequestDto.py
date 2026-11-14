from fastapi import File

class VideoRequestDto:
    file : File

    def __init__(
        self,
        file: File
    ):
        self.file = file

    def getFilename(self) -> File:
        return self.file
    