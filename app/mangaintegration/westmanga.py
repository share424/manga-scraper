from mangaintegration.mangasite import MangaSite
from mangaintegration.manga import Manga, Chapter
from bs4 import BeautifulSoup
import requests

class WestManga(MangaSite):

    def __init__(self):
        self._base_url = "https://westmanga.info/manga/"
        self._name = "WestManga"

    def fetchManga(self, url):
        print('[INFO] fetch manga:', url)
        new_url = f'{self.getBaseUrl()}{url}'
        response = requests.get(new_url)
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        content = parsed_html.body.find('div', attrs={'class': 'mangainfo'})
        if content is None:
            raise ValueError('Manga Info not found!')

        manga = Manga()

        title = self.fetchTitle(content)
        synopsis = self.fetchSynopsis(content)
        
        manga._title = title
        manga._synopsis = synopsis
        manga._key = url
        manga._chapters = self.fetchAllChapter(content)
        return manga

    def fetchTitle(self, parsed_html):
        print('[INFO] fetch title')
        title = parsed_html.find('h1')
        if title:
            return title.decode_contents().strip()
        return None

    def fetchSynopsis(self, parsed_html):
        print('[INFO] fetch synopsis')
        # #post-52634 > div > div.area > div > div > div > div.sin
        main_content = parsed_html.find('div', attrs={'itemprop': 'mainContentOfPage'})
        synopsis = main_content.find('p')
        if synopsis:
            synopsis = synopsis.decode_contents().strip()
        return synopsis

    def fetchAllChapter(self, content):
        print('[INFO] fetch all chapter')
        table = content.find('div', attrs={'class': 'cl'})
        chapter_list = table.find_all('li')
        chapters = []
        for ch in chapter_list:
            ch_info = ch.find('span').find('a')
            chapter = Chapter()
            chapter._chapter = ch_info.decode_contents().strip()
            print('[INFO] fetch chapter:', chapter.getChapter())
            chapter._images = self.fetchChapter(ch_info['href'])
            chapters.append(chapter)
        return chapters
    
    def fetchChapter(self, url):
        response = requests.get(url)
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        contents = parsed_html.body.find('div', attrs={'id': 'readerarea'}).find_all('p')
        images = []
        for content in contents:
            img = content.find('img')
            images.append(img['src'])
        return images