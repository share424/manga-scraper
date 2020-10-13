from hashlib import sha256

class MangaSite:
    _base_url = None
    _name = None

    def __init__(self):
        pass

    def getBaseUrl(self):
        return self._base_url

    def getName(self):
        return self._name

    def fetchManga(self, url):
        pass

    def info(self):
        return {
            "name": self.getName(),
            "base_url": self.getBaseUrl(),
            "uuid": self.getUUID()
        }

    def getUUID(self):
        name = type(self).__name__
        return sha256(name.encode('utf-8')).hexdigest()
    