import pytest

from src import Scraper, Translate

@pytest.mark.asyncio
async def test_translate_page():
    scraper = Scraper()
    translate = Translate()

    res = await scraper.get_raw('https://www.uukanshu.com/b/120636/28238.html')

    t = ' (-BREAK-) '.join(res)

    texts = await translate.translate_text([t])

    a = texts[0].split(' (-BREAK-) ')

    print(a)

    assert len(a) > 10