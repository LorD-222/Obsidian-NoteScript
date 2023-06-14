import feedparser
import os
import time
from bs4 import BeautifulSoup
import re


# Функция для сохранения статьи в формате Markdown
def save_article_as_md(entry, save_path):
    # Получение заголовка статьи, удаление всех небуквенно-цифровых символов
    title = re.sub(r'[^\w\s]', '', entry.title)[:200]
    date = entry.published
    content = entry.summary
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    filename = f"{title}.md"

    # Проверка категории в записи и создание директории с именем категории
    if 'tags' in entry.keys():
        if len(entry.tags) > 1:
            category = entry.tags[1].term
        else:
            category = entry.tags[0].term
        category_path = os.path.join(save_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
    else:
        category_path = save_path

    # Запись файла
    with open(os.path.join(category_path, filename), 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n")
        f.write(f"> Published on {date}\n")
        f.write("\n---\n")
        f.write(f"{text}\n")


# Функция для получения RSS-ленты и вызова функции сохранения
def get_rss_feed(url, save_path):
    NewsFeed = feedparser.parse(url)
    for entry in NewsFeed.entries:
        save_article_as_md(entry, save_path)


# Функция дляудаления старых файлов и пустых папок старше недели
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
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    save_path = os.path.join(base_dir, 'RSS')
    delete_old_files_and_empty_folders(save_path)
    get_rss_feed(url, save_path)
