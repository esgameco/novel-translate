import asyncio
import os
import json
import random

from .scrape import Scraper
from .translate import Translate
from .generator import Generator

from typing import List

class API:
    def __init__(self, proxy: str=None, base_url: str=None) -> None:
        self.scraper = Scraper(proxy=proxy)
        self.translate = Translate(proxy=proxy)
        self.generator = Generator()

        self._claude_keys = self._get_claude_keys()

        self.base_url = base_url if base_url else os.getenv('BASE_URL')
    
    def _get_claude_keys(self) -> List[str]:
        with open(os.path.join(os.getcwd(), 'secrets', 'anthropic_5.json'), 'r') as file:
            data = json.load(file)

            return data['keys']
        
    async def _test_claude_keys(self) -> str:
        working_keys = []
        for key in self._claude_keys:
            try:
                res = await self.translate.translate_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non tincidunt nulla, in consequat ante. Nulla rhoncus, justo ac ullamcorper iaculis, erat orci gravida nisl, eu facilisis lorem nunc sed dolor. Phasellus egestas ornare bibendum. Maecenas at dapibus urna, quis posuere leo. Vestibulum quis velit ultricies, tristique erat quis, finibus purus. Aliquam quis dictum mauris. Quisque id cursus eros. Nulla eget rhoncus lectus. Duis molestie, metus et laoreet tristique, nunc tellus consectetur neque, eu dapibus arcu dui in erat. Suspendisse scelerisque quis diam eu congue. Sed iaculis hendrerit tellus vel congue. Maecenas non nisi vitae eros sollicitudin aliquam. Aliquam porta libero eu iaculis pellentesque. Nunc vitae metus vel velit commodo ultricies. Proin ut congue felis, sit amet mollis lacus. Donec eget libero venenatis, luctus ex ac, ultrices velit. Quisque ac lectus eu magna facilisis blandit. Praesent eget mattis dui. Phasellus auctor lectus in elit faucibus sollicitudin. In pulvinar turpis in neque ultricies placerat. Morbi gravida felis vel feugiat facilisis. Nullam id ultricies nulla, in mollis nibh. Pellentesque lobortis orci nisi, sit amet convallis tellus lobortis non. Fusce nec arcu metus. Phasellus mauris elit, iaculis eu lorem ac, aliquam laoreet turpis. Aenean dapibus sapien massa, eu tincidunt risus scelerisque dictum. Aliquam. ", key, model='claude-3-haiku-20240307')
                working_keys.append(key)
            except Exception:
                pass
        
        return json.dumps({'keys': working_keys}, indent=4)

    async def translate_page(self, url: str, model: str) -> str:
        res = await self.scraper.get_raw(url)
        try:
            if len(res) > 5:
                texts = ''
                # if not provider:
                texts = await self.translate.translate_text(res, random.choice(self._claude_keys), model=model)
                for i in range(8):
                    if len(texts) < len(res)/3:
                        print("Trying again...")
                        texts = await self.translate.translate_text(res, random.choice(self._claude_keys), model=model)
                # elif provider == 'openai':
                #     texts = await self.translate.translate_text_openai(res)
                #     if len(texts) < len(res)/3:
                #         texts = await self.translate.translate_text_deepl(res)
                # elif provider == 'deepl':
                #     texts = await self.translate.translate_text_deepl(res)
                return texts
        except Exception:
            await asyncio.sleep(5)
            pass
        return ''
    
    async def translate_pages(self, pages: List[str], r: tuple=None, model='claude-3-5-sonnet-20240620') -> List[str]:
        res = []
        if not r:
            r = (0, len(pages))
        if len(r) == 2:
            for i in range(r[0], r[1]):
                res.append((i, await self.translate_page(pages[i], model=model)))
                print(f'Finished translating chapter {i+1} with Claude.')
        else:
            for i in r:
                res.append((i, await self.translate_page(pages[i], model=model))) # 
                print(f'Finished translating chapter {i+1} with Claude.')
        return res
    
    async def get_pages(self, url: str) -> List[str]:
        res = await self.scraper.get_pages(url)
        res.sort(key=lambda n: int(n.split('/')[-1].replace('.html', '')))

        return res
    
    def generate_page(self, title: str, text: str, out_file: str):
        self.generator.generate_html({'title': title, 'content': text}, out_file=out_file)
    
    async def gen_book(self, url: str, output_loc: str, r: tuple=None, model=None):
        pages = await self.get_pages(url=url)
        print('Finished scraping pages from the website.')

        translated = {}
        if model:
            translated = await self.translate_pages(pages=pages, r=r, model=model)
        else:
            translated = await self.translate_pages(pages=pages, r=r)
        print('Finished translating.')

        for t in translated:
            self.generate_page(t[0]+1, t[1], os.path.join(os.getcwd(), 'output', output_loc, f'{t[0]+1}.html'))
        print('Finished generating pages.')