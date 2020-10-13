from mangaintegration.westmanga import WestManga
from fastapi import HTTPException

mangasites = [
    WestManga()
]

def GetAllMangasite():
    return [ms.info() for ms in mangasites]

def CreateMangasite(uuid):
    for ms in mangasites:
        if ms.getUUID() == uuid:
            return ms
    raise HTTPException(
            status_code=404,
            detail="Mangasite Integration not found"
            )