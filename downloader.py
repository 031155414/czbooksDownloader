import requests


def path():
    path = r"C:\Users\yusun\Documents\novelDownloader"
    return path


def download_url():
    url = r"https://czbooks.net/n/ai164db"
    return url


def get_novel():
    novel_page = requests.get(download_url())
    txt = open(f'{path()}/novel_page.txt', "w+", encoding="utf-8")
    for i in novel_page.text:
        print(i, end="", file=txt)
    txt.close()
    txt = open(f'{path()}/novel_page.txt', "r", encoding="utf-8")
    reader = txt.readlines()
    txt.close()
    return reader


def get_novel_property():
    novel_property = []
    skip = True
    mark = "info"
    title_markup = "《"
    title_markdn = "》"
    author_markup = "a href"
    author_markdn = ">"
    for ln in get_novel():
        if ln.find(mark) > 0:
            skip = False
            continue
        if skip == True:
            continue
        if ln.find(title_markup) > 0:
            novel_property.append(
                (ln[ln.find(title_markup): ln.find(title_markdn) + 1]))
        if ln.find(author_markup) > 0:
            novel_property.append(
                (ln[ln.find(author_markup) + 24: ln.find(author_markdn) - 1]))
            break
    return novel_property


def get_chapter_url():
    chapter_url = []
    skip = True
    up_mark = "nav chapter-list"
    dn_mark = "div"
    chapter_url_markup = "f="
    chapter_url_markdn = ">"
    for ln in get_novel():
        if ln.find(up_mark) > 0:
            skip = False
            continue
        if skip == True:
            continue
        if ln.find(dn_mark) > 0:
            skip = True
            continue
        if ln.find(chapter_url_markup) > 0:
            up_index = ln.find(chapter_url_markup)
            dn_index = ln.find(chapter_url_markdn, up_index)
            chapter_url.append((ln[up_index + 3: dn_index - 1]))
    return chapter_url


def get_chapter(url):
    chapter_page = requests.get(f'https:{url}')
    txt = open(f'{path()}/chapter_page.txt', "w+", encoding="utf-8")
    for i in chapter_page.text:
        print(i, end="", file=txt)
    txt.close()
    txt = open(f'{path()}/chapter_page.txt', "r", encoding="utf-8")
    reader = txt.readlines()
    txt.close()
    return reader


def get_chapter_content(url):
    chapter_content = []
    skip = True
    up_mark = "<div class = \"content\">"
    dn_mark = "div"

    for ln in get_chapter(url):
        if ln.find(up_mark) > 0:
            skip = False
            chapter_content.append(ln)
            continue
        if skip == True:
            continue
        if ln.find(dn_mark) > 0:
            skip = True
            chapter_content.append(ln)
            continue
        chapter_content.append(ln)
    return chapter_content


def layout(content):
    result = []
    for ln in content:
        ln = ln.replace("\n", "")
        ln = ln.replace("<br />", "")
        ln = ln.replace(" <div class = \"content\">", "")
        ln = ln.replace(" ", "")
        if ln != "":
            result.append(ln)
    return result


if __name__ == "__main__":
    novel_property = get_novel_property()
    output = open(f'{path()}/{novel_property[0]}.txt', "w+", encoding="utf-8")

    print(f'{novel_property[0]}\n\n{novel_property[1]}', file=output)

    count = 1
    for url in get_chapter_url():
        print(f"\n\n第{count}章\n", file=output)
        content = layout(get_chapter_content(url))
        for ln in content:
            print(f'{ln}\n', file=output)
        count += 1
    output.close()
    print("finish")
