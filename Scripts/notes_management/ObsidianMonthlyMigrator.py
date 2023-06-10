import os
import shutil
import re

def get_notes_directory():
    """Возвращает путь к папке 'Daily', находящейся на два уровня выше текущего скрипта."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    two_level_up = os.path.dirname(os.path.dirname(script_dir))
    return os.path.join(two_level_up, "Daily")

def move_file_to_month_folder(filename, notes_dir):
    """Перемещает файл в папку, соответствующую месяцу, указанному в имени файла."""
    year_month = filename[:7]  # YYYY-MM
    new_dir = os.path.join(notes_dir, year_month)
    os.makedirs(new_dir, exist_ok=True)

    old_file_path = os.path.join(notes_dir, filename)
    new_file_path = os.path.join(new_dir, filename)
    shutil.move(old_file_path, new_file_path)

    print(f"Moved file {filename} to {new_dir}")

def main():
    notes_dir = get_notes_directory()
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')

    for filename in os.listdir(notes_dir):
        if filename.endswith(".md") and date_pattern.match(filename):
            move_file_to_month_folder(filename, notes_dir)

if __name__ == "__main__":
    main()
