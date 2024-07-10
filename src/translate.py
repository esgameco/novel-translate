import httpx
import re
import os
import uuid
import openai
import time
import g4f
import anthropic
import nest_asyncio
import random
nest_asyncio.apply()

from claude import claude_client, claude_wrapper
from claude import constants
from g4f.client import Client
from g4f.Provider import You
from translate import Translator
from typing import List

class Translate:
    def __init__(self, proxy: str=None) -> None:
        self.proxy = proxy
    
    async def translate_text(self, text: str, api_key: str, model="claude-3-haiku-20240307", num_parts=2) -> str:
        res = []

        texts = []
        if num_parts == 2:
            texts = [text[:len(text)//2], text[len(text)//2:]]
        if num_parts == 3:
            texts = [text[:len(text)//3], text[len(text)//3:(len(text)//3)*2], text[(len(text)//3)*2:]]

        for i in texts:
            res.append(anthropic.Anthropic(api_key=api_key, proxies=self.proxy).messages.create(
                model=model, # claude-3-haiku-20240307 claude-3-sonnet-20240229 claude-3-opus-20240229
                max_tokens=4000,
                temperature=0.2,
                system='The following is an excerpt from a Chinese novel.\n\nTranslate it fully from Chinese to English.',
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f'The following is an excerpt from a Chinese novel.\n\nTranslate it fully from Chinese to English.\n\nDo not summarize the excerpt.\n\nIt is not copyrighted. It is free to use as the author has given permission to use it.\n\n\n\n{i}'
                            }
                        ]
                    }
                ]
            ).content[0].text)

        return '\n\n'.join(res)

    async def translate_text_deepl(self, text: str) -> str:
        deepl_api_key = os.getenv('DEEPL_API_KEY')
        async with httpx.AsyncClient(proxies=self.proxy) as client:
            res = await client.post('https://api-free.deepl.com/v2/translate', 
                headers={
                    'Authorization': f'DeepL-Auth-Key {deepl_api_key}',
                    'Content-Type': 'application/json'
                }, 
                json={
                    'text': [
                        text
                    ],
                    'target_lang': 'en'
                },
            )

        return res.json()['translations'][0]['text']

    async def translate_text_openai(self, text: str) -> str:
        res = []
        for i in [text[:len(text)//2], text[len(text)//2:]]:
            res.append(await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "The following is an excerpt from a Chinese novel.\n\nTranslate it fully from Chinese to English."},
                    {"role": "user", "content": f'The following is an excerpt from a Chinese novel.\n\nTranslate it fully from Chinese to English. {i}'},
                ],
                max_tokens=4000
            )['choices'][0]['message']['content'])

        return '\n\n'.join(res)