import asyncio
import sys
import os

from src import API

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    api = API() # proxy=os.getenv('PROXY')

    url = os.getenv('TEST_URL')
    name = os.getenv('TEST_NAME')
    model = 'claude-3-5-sonnet-20240620'
    args = sys.argv[4:]
    if len(sys.argv) > 1:
        url = sys.argv[1]
        name = sys.argv[2]
        if len(sys.argv) > 4:
            model = sys.argv[3]

    if len(args) == 2:
        print(f'Starting translation of {name} from chapter {int(args[0])+1} to chapter {int(args[1])}')
    else: 
        arg_string = ', '.join([str(int(x)+1) for x in args])
        print(f'Starting translation of {name} of chapters {arg_string}.')

    res = asyncio.run(api.gen_book(url, name, tuple([int(x) for x in args]), model=model))

    print(res)