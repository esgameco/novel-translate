# novel-translate

A python script that will scrape a site for raws, translate using AI, then output to files. 

## Setup

```bash
git clone https://github.com/esgameco/novel-translate.git
python -m venv venv
# DO -> Activate venv
pip install -r requirements.txt

cp .env.template .env
# Change 

python main.py {novel url} {novel name} {claude model} {page start} {page end}
# use either claude-3-haiku-20240307 or claude-3-5-sonnet-20240620
```

## TODO

1. [x] Scrape site for raws
2. [x] Translate raws using API
3. [x] Output to files

### Future

1. [ ] Extract characters with Haiku
2. [ ] Translate with Sonnet / Opus
3. [ ] Verify with Haiku