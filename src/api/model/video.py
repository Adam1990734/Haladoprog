class Video:
    def __init__(self, name = "", file = None):
        self.name = name
        self.file = file

    def getName(self):
        return self.name

    def getFile(self):
        return self.file

    def setName(self, name):
            self.name = name

    def setFile(self, file):
        self.file = file