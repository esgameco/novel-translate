import pytest
import os

from src import API

@pytest.mark.asyncio
async def test_api_pages():
    api = API()

    pages = await api.get_pages('https://www.uukanshu.com/b/120636/')

    res = await api.translate_pages(pages=pages, r=(167, 169))

    print(res[0])

    assert len(res) == 2

@pytest.mark.asyncio
async def test_api_gen_pages():
    api = API()

    pages = await api.get_pages('https://www.uukanshu.com/b/120636/')

    res = await api.translate_pages(pages=pages, r=(167, 168))

    for r in res:
        api.generate_page('167', r, os.path.join(os.getcwd(), 'output', f'167.html'))

    assert len(res) == 1