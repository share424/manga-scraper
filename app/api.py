from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from mangaintegration import GetAllMangasite, CreateMangasite
from pydantic import BaseModel
from pymongo import MongoClient
from hashlib import sha256

class MangaRequest(BaseModel):
    uuid: str
    key: str

app = FastAPI()

mongo_client = MongoClient(
    host="172.18.97.1:27017",
    username="root",
    password="123456"
)

@app.get("/")
def index():
    return {"Hello": "Worlds"}

@app.get('/mangasites')
def get_all_mangasite():
    return GetAllMangasite()

@app.post('/mangas')
async def create_manga(req: MangaRequest):
    ms = CreateMangasite(req.uuid)
    manga = ms.fetchManga(req.key)
    if manga is not None:
        db = mongo_client.mangas
        manga_data = manga.getData()
        manga_data["integration"] = req.uuid
        manga_data['id'] = sha256(f"{req.uuid}:{req.key}".encode('utf-8')).hexdigest()
        payload = {
            "key": req.key,
            "integration": req.uuid
        }
        collection = db.mangas.find(payload)
        if(collection.count() >= 1):
            db.mangas.replace_one(payload, manga_data)
        else:
            db.mangas.insert(manga_data)
    return {
        "status": True
    }

@app.get('/mangas')
async def get_all_manga():
    db = mongo_client.mangas
    collection = db.mangas.find()
    mangas = []
    for manga in collection:
        mangas.append({
            'id': manga['id'],
            'title': manga['title'],
            'synopsis': manga['synopsis'],
            'total_chapter': len(manga['chapters'])
        })
    return mangas

@app.get('/mangas/{id}')
async def get_manga(id):
    db = mongo_client.mangas
    manga = db.mangas.find_one({'id': id})
    if manga is not None:
        print(type(manga))
        return {
            "id": manga["id"],
            "title": manga["title"],
            "synopsis": manga["synopsis"],
            "chapters": manga["chapters"]
        }
    raise HTTPException(status_code=404, detail="Manga not found")

