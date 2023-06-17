import os
import time
from bs4 import BeautifulSoup
import feedparser
import re
from pathlib import Path

# Константы
SECONDS_IN_DAY = 86400
TITLE_CHAR_LIMIT = 200
DAYS_OLD = 7


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


# Функция для создания директории категории и возврата пути к ней
def create_directory_path(save_path, entry):
    tags = entry.get('tags', [])
    category = None

    # Если в записи есть теги, выбираем категорию, которая не начинается с '.'
    for tag in tags[1:]:
        if not tag.term.startswith('.'):
            category = tag.term
            break

    # Если категория не найдена, проверяем первую категорию
    if not category and tags and not tags[0].term.startswith('.'):
        category = tags[0].term

    # Создаем директорию для категории, если она была найдена
    if category:
        category_path = Path(save_path) / category
        category_path.mkdir(parents=True, exist_ok=True)
        return category_path
    else:
        return Path(save_path)


# Функция для сохранения статьи в формате Markdown
def save_article_as_md(entry, save_path):
    title = re.sub(r'[^\w\s]', '', entry['title'])[:TITLE_CHAR_LIMIT]
    date = entry['published']
    content = process_article_content(entry['summary'])
    category_path = create_directory_path(save_path, entry)

    # Извлекаем теги из записи
    tags = [tag.term for tag in entry.get('tags', [])]

    # Если теги существуют, преобразуем их в строку, разделенную запятыми
    tags_line = f"Теги: {', '.join(tags)}\n\n" if tags else ""

    # Создаем файл Markdown с тегами перед контентом
    file_path = category_path / f"{title}.md"
    with file_path.open('w', encoding='utf-8') as f:
        f.write(f"# {title}\n")
        f.write(f"> Published on {date}\n")
        f.write(f"\n{tags_line}---\n")
        f.write(f"{content}\n")


# Функция для получения RSS-ленты и сохранения каждой записи файла Markdown
def get_rss_feed(url, save_path):
    NewsFeed = feedparser.parse(url)
    for entry in NewsFeed.entries:
        save_article_as_md(entry, save_path)


# Функция для удаления файлов, старше DAYS_OLD дней, и пустых директорий
def delete_old_files_and_empty_folders(path, days_old=DAYS_OLD):
    cutoff_time = time.time() - days_old * SECONDS_IN_DAY
    for root, dirs, files in os.walk(path, topdown=False):
        for file_name in files:
            file_path = Path(root) / file_name
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if not list(dir_path.iterdir()):
                dir_path.rmdir()


if __name__ == "__main__":
    url = "https://tproger.ru/feed/"  # URL RSS-ленты
    base_dir = Path(__file__).resolve().parents[2]
    save_path = base_dir / 'RSS'
    delete_old_files_and_empty_folders(save_path)
    get_rss_feed(url, save_path)
