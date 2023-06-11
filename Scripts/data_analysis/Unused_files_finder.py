import os
import glob

# Функция для получения всех файлов с указанным расширением в заданной директории
def get_all_files(directory, extension):
    return glob.glob(f"{directory}/**/*{extension}", recursive=True)

# Функция для получения всех ссылок из всех markdown-файлов в заданной директории
def get_all_links(directory):
    files = get_all_files(directory, '.md')
    links = set()

    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            # Добавление всех ссылок из текущего файла в общий список ссылок
            links.update(extract_links_from_content(content))

    return links

# Функция для извлечения всех внутренних ссылок (в формате [[Link]]) из заданного содержимого
def extract_links_from_content(content):
    links = set()
    start_idx = content.find('[[')

    # Пока в содержимом есть ссылки
    while start_idx != -1:
        end_idx = content.find(']]', start_idx)
        if end_idx != -1:
            link = content[start_idx+2:end_idx]
            links.add(link)
        start_idx = content.find('[[', end_idx)
    
    return links

# Функция для поиска всех файлов, которые не используются в качестве ссылок в других файлах
def find_unused_files(directory):
    all_files = set(os.path.relpath(f, directory).replace('.md', '') for f in get_all_files(directory, '.md'))
    all_links = get_all_links(directory)

    unused_files = all_files - all_links
    return unused_files

# Функция для создания отчета о неиспользуемых файлах
def create_report(directory, unused_files):
    # Добавляем поддиректорию 'Reports' к нашему пути директории
    report_dir = os.path.join(directory, 'Reports')
    print(report_dir)
    
    # Проверяем, существует ли директория 'Reports'. Если нет, создаем ее
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    report_file = os.path.join(report_dir, 'unused_files_report.md')
    with open(report_file, 'w') as f:
        f.write('# Unused Files Report\n\n')
        for file in sorted(unused_files):
            f.write(f'- [[{file}]]\n')

# Основная функция, которая вызывает все остальные функции
def main():
    # Получите текущий рабочий каталог
    current_dir = os.path.dirname(os.path.realpath(__file__))

    directory = os.path.dirname(os.path.dirname(current_dir))
    unused_files = find_unused_files(directory)
    create_report(directory, unused_files)

if __name__ == "__main__":
    main()
