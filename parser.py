import sys
import io
from re import match, search, IGNORECASE
from os import listdir
from os.path import isfile, join, exists

######################### Функции для получения количества строк в файле, нужны лишь для указания текущего прогресса #########################

def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)

def rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
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


######################### Функция для поиска строк, содержащих требуемое регулярное выражение #########################
def find_errors(files, arg):
    output = open("output.txt", 'w', encoding="utf-8")      ########## Файл для записи вывода. Если отсутствует, создается, если существует, перезаписывается
    for f in files:
        print("-------------------" + "\n")
        output.write("====== START OF FILE ======\n")
        print("Идет чтение файла " + f + "\n")              ########## Вывод в консоль названия текущего файла
        output.write(f + ": \n")                            ########## Запись названия в файл вывода
        print("-------------------" + "\n")
        output.write("-------------------" + "\n")
        counter = 1                                         ########## Номер строки в файле, исследуемой в итерации последующего цикла
        with io.open(f, encoding='utf-8') as file:
            lines = rawpycount(f) + 1                       ########## Количество строк в файле, необходимо для определения текущего прогресса, не более
            for line in file:
                print("Текущий прогресс чтения файла составляет: " + str(
                    round(100 * counter / lines, 2)) + "% Идет чтение " + str(counter) + " строки из " + str(
                    lines) + "\n")                          ########## Вывод текущего прогресса чтения файла в виде строки. Если строка содержит регулярку, она печатается ниже
                tpl = arg
                if search(tpl, line):                      ########## Проверка строки на содержание регулярки
                    print(line, end='')                    ########## Вывод в консоль строки, содержащей регулярное выражение
                    output.write(str(counter) + ": " + line + "\n")   ########## Запись данной строки в файл с ее порядковым номером в исходном файле (нумерация от 1)
                    print()
                counter += 1
        print()
        output.write("====== END OF FILE ======\n\n")

path = sys.argv[1]                                          ########## Получаем путь в виде первого аргумента
arg = sys.argv[2]                                           ########## Получаем регулярку в виде второго аргумента
files = get_files(path)                                     ########## Получаем список адресов файлов по данному пути (список из одного элемента, если в пути указан путь к файлу)
find_errors(files, arg)                                     ########## Производим поиск строк в файлах из списка, соответствующих регулярке

