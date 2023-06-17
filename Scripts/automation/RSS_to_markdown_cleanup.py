import feedparser
import os
import time
from bs4 import BeautifulSoup
import re


# Функция для обработки текста статьи и извлечения ссылок
def process_article_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    text_with_links = ''
    for tag in soup.find_all(True):
        if tag.name == 'p':
            if tag.find('a'):
                link = tag.a
                text = tag.get_text()
                text = text.replace(link.text, f"[{link.text}]({link.get('href')})")
                text_with_links += text + '\n\n'
            else:
                text_with_links += tag.text + '\n\n'
    return text_with_links


# Функция для сохранения статьи в формате Markdown
def save_article_as_md(entry, save_path):
    title = re.sub(r'[^\w\s]', '', entry.title)[:200]
    date = entry.published
    content = process_article_content(entry.summary)

    filename = f"{title}.md"
    category = None
    if 'tags' in entry.keys() and len(entry.tags) >= 1:
        for tag in entry.tags[1:]:
            if not tag.term.startswith('.'):
                category = tag.term
                break
        if not category and not entry.tags[0].term.startswith('.'):
            category = entry.tags[0].term
        if category:
            category_path = os.path.join(save_path, category)
            os.makedirs(category_path, exist_ok=True)
        else:
            category_path = save_path
    else:
        category_path = save_path

    # Запись файла
    with open(os.path.join(category_path, filename), 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n")
        f.write(f"> Published on {date}\n")
        f.write("\n---\n")
        f.write(f"{content}\n")


# Функция для получения RSS-ленты и вызова функции сохранения
def get_rss_feed(url, save_path):
    NewsFeed = feedparser.parse(url)
    for entry in NewsFeed.entries:
        save_article_as_md(entry, save_path)


# Функция для удаления старых файлов и пустых папок старше недели
def delete_old_files_and_empty_folders(path, days_old=7):
    now = time.time()
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            if os.stat(file_path).st_mtime < now - days_old*86400:
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


if __name__ == "__main__":
    url = "https://tproger.ru/feed/"  # URL RSS-ленты
    file_path = os.path.realpath(__file__)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    save_path = os.path.join(base_dir, 'RSS')
    delete_old_files_and_empty_folders(save_path)
    get_rss_feed(url, save_path)
