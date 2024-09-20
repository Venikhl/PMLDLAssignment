import os

# Относительный путь к директории
relative_path = "../../../models"

# Получаем абсолютный путь из относительного
directory_path = os.path.abspath(relative_path)

# Проверка, что путь существует и является директорией
if os.path.exists(directory_path) and os.path.isdir(directory_path):
    # Перебираем все файлы в директории
    files = os.listdir(directory_path)
    
    print("Файлы в директории:", directory_path)
    for file in files:
        print(file)
else:
    print("Указанный путь не существует или не является директорией.")
