import pytest
import os

from src import Scraper, Translate, API

@pytest.mark.asyncio
async def test_translate_page():
    api = API(proxy=os.getenv('PROXY'))

    texts = await api.translate_page('https://69shux.com/txt/3554/3006152')

    print(texts)

    assert texts

@pytest.mark.asyncio
async def test_translate_page_deepl():
    scraper = Scraper(proxy=os.getenv('PROXY'))
    translate = Translate(proxy=os.getenv('PROXY'))

    res = await scraper.get_raw('https://www.69shu.pro/txt/39164/28554428')

    print(res)

    texts = await translate.translate_text_deepl(res)

    print(texts)

    assert texts

@pytest.mark.asyncio
async def test_translate_page_openai():
    scraper = Scraper(proxy=os.getenv('PROXY'))
    translate = Translate(proxy=os.getenv('PROXY'))

    res = await scraper.get_raw('https://69shux.com/txt/3554/3005034')

    print(res)

    texts = await translate.translate_text_openai(res)

    print(texts)

    assert texts