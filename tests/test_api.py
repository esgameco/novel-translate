import pytest
import os

from src import API

@pytest.mark.asyncio
async def test_claude_keys():
    api = API()

    res = await api._test_claude_keys()

    print(res)

    assert res

@pytest.mark.asyncio
async def test_api_pages():
    api = API()

    pages = await api.get_pages('https://www.69shu.pro/book/39164/')

    res = await api.translate_pages(pages=pages, r=(167, 168))

    print(res[0])

    assert len(res) == 2

@pytest.mark.asyncio
async def test_api_gen_pages():
    api = API()

    pages = await api.get_pages('https://www.69shu.pro/book/39164/')

    res = await api.translate_pages(pages=pages, r=(524, 525))

    for r in res:
        api.generate_page(r[0]+1, r[1], os.path.join(os.getcwd(), 'output', f'{r[0]+1}.html'))

    assert len(res) == 1