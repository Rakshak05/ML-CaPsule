import pathlib
import re
import urllib.parse

ROOT_PATH = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def Extract_file_names():
    temp = []
    ignored = {
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING_GUIDELINES.md",
        "CONTRIBUTING.md",
        "build_readme.py",
        "requirements.txt",
        "README.md",
        "download statistics.jpg",
        "img",
        "ml img.jpg"
    }

    for path in sorted(ROOT_PATH.iterdir()):
        name = path.name
        if name.startswith('.'):
            continue
        if name in ignored:
            continue
        
        temp2 = {
            'fname': name,
            'furl': urllib.parse.quote(name)
        }
        temp.append(temp2)
    return temp

if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    
    with open(readme, "r", encoding="utf-8") as f:
        readme_contents = f.read()

    file_names = Extract_file_names()
    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )
    
    readme_contents = replace_chunk(readme_contents, "Projects", "| Content List | \n | --------------- | \n" + file_md)
    
    with open(readme, "w", encoding="utf-8") as f:
        f.write(readme_contents)

