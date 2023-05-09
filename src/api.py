import os

from .scrape import Scraper
from .translate import Translate
from .generator import Generator

from typing import List

class API:
    def __init__(self, proxy: str=None, base_url: str=None) -> None:
        self.scraper = Scraper(proxy=proxy)
        self.translate = Translate(proxy=proxy)
        self.generator = Generator()
        self.base_url = base_url if base_url else os.getenv('BASE_URL')
    
    async def translate_page(self, url: str) -> str:
        res = await self.scraper.get_raw(url)
        texts = await self.translate.translate_text([' (-BREAK-) '.join(res)])
        raw = texts[0].split(' (-BREAK-) ')
        return '\n'.join([x.replace('\u3000', '') for x in raw])
    
    async def translate_pages(self, pages: List[str], r: tuple=None) -> List[str]:
        res = []
        if not r:
            r = (0, len(pages))
        for i in range(r[0], r[1]):
            res.append((i, await self.translate_page(pages[i])))
        return res
    
    async def get_pages(self, url: str) -> List[str]:
        res = await self.scraper.get_pages(url)
        res.sort(key=lambda n: int(n.split('/')[-1].replace('.html', '')))

        return [self.base_url + x for x in res]
    
    def generate_page(self, title: str, text: str, out_file: str):
        self.generator.generate_html({'title': title, 'content': text}, out_file=out_file)
    
    async def gen_book(self, url: str, output_loc: str, r: tuple=None):
        pages = await self.get_pages(url=url)

        translated = await self.translate_pages(pages=pages, r=r)

        for t in translated:
            self.generate_page(t[0]+1, t[1], os.path.join(os.getcwd(), 'output', output_loc, f'{t[0]+1}.html'))