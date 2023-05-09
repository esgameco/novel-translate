import httpx
import re

from typing import List

class Scraper:
    def __init__(self, proxy: str=None) -> None:
        self.proxy = proxy

    async def get_raw(self, url: str) -> List[str]:
        async with httpx.AsyncClient(proxies=self.proxy) as client:
            res = await client.get(url)

            r = re.findall(r'<br />&nbsp;&nbsp;&nbsp;&nbsp;(.*?)\r<br />', res.text)
            if len(r) < 1:
                r = re.findall(r'<br />(.*?)<br />', res.text)
                if len(r) < 1:
                    r = re.findall(r'<p>(.*?)<p>', res.text)

            return r
        
    async def get_pages(self, url: str) -> List[tuple]:
        async with httpx.AsyncClient(proxies=self.proxy) as client:
            res = await client.get(url)

            r = re.findall(r'<li><a href="(.*?)" title=".*?" target="_blank">.*?</a></li>', res.text)

            return r