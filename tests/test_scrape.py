import pytest

from src import Scraper

@pytest.mark.asyncio
async def test_scrape_get_raw():
    scraper = Scraper()

    res = await scraper.get_raw('https://69shux.com/txt/3554/3004146')

    assert res

@pytest.mark.asyncio
async def test_scrape_get_pages():
    scraper = Scraper()

    res = await scraper.get_pages('https://69shux.com/book/3554/index.html')

    assert res