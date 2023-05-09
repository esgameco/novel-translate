import pytest

from src import Scraper

@pytest.mark.asyncio
async def test_scrape_get_raw():
    scraper = Scraper()

    res = await scraper.get_raw('https://www.uukanshu.com/b/120636/28238.html')

    assert res

@pytest.mark.asyncio
async def test_scrape_get_pages():
    scraper = Scraper()

    res = await scraper.get_pages('https://www.uukanshu.com/b/120636/')

    assert res