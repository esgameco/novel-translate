import os

template = """<!DOCTYPE html>

<html>
    <head>
        <title>REPLACE_TITLE</title>
        <style>
            h1 {font-size:60px;}
            p {font-size:30px; font-family: "Merriweather"; color: lightgrey;}
            body {margin:50px 300px;}
        </style>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Merriweather&display=swap" rel="stylesheet"> 
    </head>
    <body>
        <h1>Chapter REPLACE_TITLE</h1>
        <div class="content">
            REPLACE_CONTENT
        </div>
        <a href="REPLACE_PREVIOUS.html"><p>Previous: Chapter REPLACE_PREVIOUS</p></a>
        <a href="REPLACE_NEXT.html"><p>Next: Chapter REPLACE_NEXT</p></a>
    </body>
</html>
"""

class Generator:
    def __init__(self) -> None:
        pass

    def generate_html(self, input: dict, out_file: str):
        content = ''.join([f'<p>{x}</p>' for x in input['content'].split('\n')])
        h = template.replace('REPLACE_TITLE', str(input['title'])).replace('REPLACE_CONTENT', content).replace('REPLACE_PREVIOUS', str(int(input['title'])-1)).replace('REPLACE_NEXT', str(int(input['title'])+1))
        with open(out_file, 'w', encoding="utf-8") as f:
            f.write(h)