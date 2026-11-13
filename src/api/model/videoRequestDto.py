class VideoRequestDto:
    def __init__(self, file = None):
        self.file = file
    
    def getFile(self):
        return self.file

    def setFile(self, file):
        self.file = file