import httpx
import re
import os
import uuid

from typing import List

class Translate:
    def __init__(self, proxy: str=None, rsc_key: str=None, rsc_loc: str=None) -> None:
        self.proxy = proxy
        self.rsc_key = rsc_key if rsc_key else os.getenv('RSC_KEY')
        self.rsc_loc = rsc_loc if rsc_loc else os.getenv('RSC_LOC')

    async def translate_text(self, texts: List[str]) -> List[str]:
        res = httpx.post(f'https://api.cognitive.microsofttranslator.com/translate', params={
            'api-version': '3.0',
            'from': 'zh-Hans',
            'to': ['en']
        }, headers={
            'Ocp-Apim-Subscription-Key': self.rsc_key,
            'Ocp-Apim-Subscription-Region': self.rsc_loc,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }, json=[{
            'text': x
        } for x in texts], proxies=self.proxy)

        j = res.json()

        return [x['translations'][0]['text'] for x in j]