class Manga:
    _title = None
    _key = None
    _chapters = []
    _synopsis = None

    def __init__(self):
        pass

    def getTitle(self):
        return self._title

    def getKey(self):
        return self._key

    def getAllChapters(self):
        return self._chapters

    def getSynopsis(self):
        return self._synopsis

    def getData(self):
        return {
            "title": self._title,
            "key": self._key,
            "chapters": [ch.getData() for ch in self._chapters],
            "synopsis": self._synopsis
        }

class Chapter:
    _chapter = None
    _images = []

    def __init__(self):
        pass

    def getChapter(self):
        return self._chapter

    def getAllImages(self):
        return self._images

    def getData(self):
        return {
            "chapter": self._chapter,
            "images": self._images
        }
    