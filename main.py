import asyncio
import sys
import os

from src import API

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    api = API()

    url = os.getenv('TEST_URL')
    name = os.getenv('TEST_NAME')
    if len(sys.argv) > 1:
        url = sys.argv[1]
        name = sys.argv[2]

    res = asyncio.run(api.gen_book(url, name, (0, 10)))

    print(res)