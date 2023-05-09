# novel-translate

A python script that will scrape a site for raws, translate using an Azure api, then output to files. 

## Setup

```bash
git clone https://github.com/esgameco/novel-translate.git
python -m venv venv
# DO -> Activate venv
pip install -r requirements.txt

cp .env.template .env
# Change RSC_KEY and RSC_LOC to azure key and location of resource

python main.py {novel url} {novel name}
```

## TODO

1. [x] Scrape site for raws
2. [x] Translate raws using API
3. [x] Output to files