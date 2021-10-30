import sys
from os import listdir
from os.path import isfile, join, exists


######################### Функция для получения файлов по указанному пути #########################
def get_files(route):
    if exists(route):                                       ########## Сначала проверяем существование указанного пути
        files = []
        if (isfile(route)):                                 ########## По указанному пути лежит файл
            files.append(route)
        else:                                               ########## По указанному пути лежит папка, грузим все текстовые файлы из нее
            for f in listdir(route):
                if isfile(join(route, f)):
                    if f.endswith(".txt") or f.endswith(".log"):
                        files.append(join(route, f))
        return files
    else:
        print("Путь некорректен")
        sys.exit(1)


path = sys.argv[1]
files = get_files(path)

