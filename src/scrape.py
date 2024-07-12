import httpx
import re
import asyncio

from typing import List

class Scraper:
    def __init__(self, proxy: str=None) -> None:
        self.proxy = proxy
        # self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
        self.headers = {}

    async def get_raw(self, url: str, offline=True) -> str:
        async with httpx.AsyncClient(proxies=self.proxy, headers=self.headers) as client:
            try:
                res = await client.get(url, timeout=60.0)
            except Exception as e:
                try:
                    await asyncio.sleep(5)
                    res = await client.get(url)
                except Exception as e2:
                    print(f'{e}\n{e2}')
                    if not offline:
                        return ''

            if 'feibzw' in url:
                try: 
                    r = re.findall(r'<p>(.*?)</p>', res.content.decode('gb18030'))
                except Exception: 
                    return ''
            if 'xsbiquge' in url:
                try: 
                    r = re.findall(r'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<p class="content_detail">\r\n                        (.*?)\r\n                        \r\n                    </p>', res.content.decode('utf-8'))
                except Exception: 
                    return ''
            elif 'biqu' in url:
                try:
                    r = re.findall(r'<p>(.*?)</p>', res.content.decode('utf-8'))
                except Exception:
                    return ''
            elif 'shuba' in url:
                try:
                    r = re.findall(r'<p>(.*?)</p>', res.content.decode('gb18030'))
                except Exception:
                    return ''
            elif 'twkan' in url:
                try:
                    with open('./input/' + url.split('/')[4] + '/' + url.split('/')[5] + '.html', 'r', encoding='utf-8') as f:
                        inp = f.read()
                        r = re.findall(r'&emsp;(.*?)<', inp)
                    # r = re.findall(r'&emsp;(.*?)<', res.content.decode('utf-8'))
                except Exception:
                    try:
                        r = re.findall(r'<br>\n      &emsp;&emsp;(.*?)\n     <br>', res.content.decode('gb2312')) # 69shu.pro
                    except Exception:
                        try:
                            r = re.findall(r'<br>\n      &emsp;&emsp;(.*?)\n     <br>', res.content.decode('gb18030'))
                        except Exception:
                            try:
                                r = re.findall(r'<br/>\n&emsp;&emsp;(.*?)<br/>', res.content.decode('utf-8')) # 69shux.com
                            except Exception:
                                return ''
            elif 'faloo' in url:
                try:
                    r = re.findall(r'<p>(.*?)</p>', res.content.decode('utf-8'))
                except Exception:
                    return ''
            elif 'mayiwsk' in url:
                try:
                    r = re.findall(r'<br />\n&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />', res.content.decode('utf-8'))
                except Exception:
                    return ''

            return '\n\n'.join([x.replace('&emsp;', '').replace('<br />', '').replace('<br>', '').replace('\r', '') for x in r])
        
    async def get_pages(self, url: str, offline=True) -> str:
        async with httpx.AsyncClient(proxies=self.proxy, headers=self.headers) as client:
            try:
                res = await client.get(url)
            except Exception as e:
                try:
                    res = await client.get(url)
                except Exception as e2:
                    print(f'{e}\n{e2}')
                    if not offline:
                        return []

            if 'feibzw' in url:
                r = re.findall(r'<li><a href="(.*?)"', res.content.decode('gb18030'))
                r = [url.replace('index.html', '') + x for x in r if '.html' in x]
                r = list(set(r))
            if 'xsbiquge' in url:
                r = re.findall(r'<dd>\r\n                    <a href="(.*?)">', res.content.decode('utf-8'))
                r = ['http://www.xsbiquge.la' + x for x in r if 'book' in x]
                r = list(set(r))
            elif 'biqu' in url:
                r = re.findall(r'<li><a href="(.*?)">.*?</a></li>', res.content.decode('utf-8'))
                r = ['https://www.22biqu.com' + x for x in r if 'biqu' in x]
                r = list(set(r))
            elif 'shuba' in url:
                # with open('./input/' + url.split('/')[4] + '.html', 'r', encoding='utf-8') as f:
                #     inp = f.read()
                #     r = re.findall(r'<li data-num=".*?"><a href="(.*?)">.*?</a>', inp)
                r = re.findall(r'<li data-num=".*?"><a href="(.*?)">.*?</a>', res.content.decode('gb18030'))
                if len(r) <= 1:
                    r = re.findall(r'<li data-num=".*?"><a href="(.*?)">.*?</a>', res.content.decode('utf-8'))
            elif 'twkan' in url:
                with open('./input/' + url.split('/')[4] + '.html', 'r', encoding='utf-8') as f:
                    inp = f.read()
                    r = re.findall(r'href="(.*?)"', inp)
                # r = re.findall(r'href="(.*?)"', res.content.decode('utf-8'))
            elif 'shu' in url:
                r = re.findall(r'href="(.*?)"', res.content.decode('utf-8')) # <li data-num=".*?"><a href="(.*?)">.*?</a></li>
                if len(r) <= 1:
                    r = re.findall(r'<li data-num=".*?"><a href="(.*?)">.*?</a>', res.content.decode('utf-8'))  
                # r'<li><a href="(.*?)" title=".*?" target="_blank">.*?</a></li>' 
            elif 'faloo' in url:
                r = re.findall(r'<div class="tt"><a href="(.*?)"', res.content.decode('gb18030'))
                r = ['https:' + x for x in r]
            elif 'mayiwsk' in url:
                r = re.findall(r'<dd><a href="(.*?)">', res.content.decode('utf-8'))
                r = ['https://www.mayiwsk.com' + x for x in r]
            return r
        