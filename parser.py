import sys
import io
from re import match, search, IGNORECASE
from os import listdir
from os.path import isfile, join, exists

######################### Функция для подсчета количества строк в файле #########################
def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)

def rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    f.close()
    return sum( buf.count(b'\n') for buf in f_gen )


######################### Функция для получения файлов по указанному пути #########################
def get_files(route):
    if exists(route):                                       ########## Сначала проверяем существование указанного пути
        files = []
        if (isfile(route)):                                 ########## По указанному пути лежит файл, добавляем его в список
            files.append(route)
        else:                                               ########## По указанному пути лежит папка, грузим все текстовые файлы из нее в список
            for f in listdir(route):
                if isfile(join(route, f)):
                    if f.endswith(".txt") or f.endswith(".log"): ########## Добавление текстовых файлов *.txt и *.log
                        files.append(join(route, f))
        return files
    else:
        print("Путь некорректен")
        sys.exit(1)


def find_errors(files, arg):
    for f in files:
        with io.open(f, encoding='utf-8') as file:
            for line in file:
                tpl = arg
                if search(tpl, line):                       ########## Проверка строки на содержание регулярки
                    print("Line found")                     ########## Заглушка на случай нахождения строки с содержанием регулярки ##########

path = sys.argv[1]                                          ########## Получаем путь в виде первого аргумента
arg = sys.argv[2]                                           ########## Получаем регулярку в виде второго аргумента
files = get_files(path)                                     ########## Получаем список файлов по данному пути (список из одного элемента, если в пути указан путь к файлу
find_errors(files, arg)                                     ########## Производим поиск строк в файлах из списка, соответствующих регулярке

