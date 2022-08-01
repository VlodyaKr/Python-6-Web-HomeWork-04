import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from console_bot.command_parser import command_parser
from console_bot.command_parser import RainbowLexer
from console_bot.normalize import normalize
from datetime import datetime
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory

REGISTER_EXTENSIONS = {
    'JPEG': 'IMAGES', 'PNG': 'IMAGES', 'JPG': 'IMAGES', 'SVG': 'IMAGES', 'GIF': 'IMAGES', 'ICO': 'IMAGES',
    'MP3': 'AUDIO', 'OGG': 'AUDIO', 'WAV': 'AUDIO', 'AMR': 'AUDIO', 'FLAC': 'AUDIO', 'WMA': 'AUDIO',
    'AVI': 'VIDEO', 'MP4': 'VIDEO', 'MOV': 'VIDEO', 'MKV': 'VIDEO', 'WMV': 'VIDEO',
    'DOC': 'DOCUMENTS', 'DOCX': 'DOCUMENTS', 'TXT': 'DOCUMENTS', 'PDF': 'DOCUMENTS', 'XLSX': 'DOCUMENTS',
    'PPTX': 'DOCUMENTS', 'RTF': 'DOCUMENTS',
    'BAT': 'PROGRAMS', 'CMD': 'PROGRAMS', 'EXE': 'PROGRAMS', 'C': 'PROGRAMS', 'CPP': 'PROGRAMS', 'JS': 'PROGRAMS',
    'PY': 'PROGRAMS', 'VBS': 'PROGRAMS',
    'ZIP': 'ARCHIVES', 'GZ': 'ARCHIVES', 'TAR': 'ARCHIVES'
}

FOLDERS = []
work_folder = Path('.')

def get_extension(filename: str) -> str:
    # Перетворюємо розширення файлу на назву теки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def sort_files(file: Path, container: str, ext: str):
    if container == 'ARCHIVES':
        handle_archive(file, work_folder / container)
    elif container == 'OTHERS' and not ext:
        new_file = work_folder / container
        handle_file(file, new_file)
    else:
        new_file = work_folder / container / ext
        handle_file(file, new_file)


def scan_item(folder: Path, item: Path) -> None:
    # Якщо це тека, то додаємо її до списку FOLDERS і переходимо до наступного елемента теки
    if item.is_dir():
        # Перевіряємо, щоб тека не була тією, в яку ми вже складаємо файли
        if item.name not in ('ARCHIVES', 'VIDEO', 'AUDIO', 'DOCUMENTS', 'IMAGES', 'PROGRAMS', 'OTHERS'):
            FOLDERS.append(item)
            #  Скануємо цю вкладену теку – рекурсія
            for subitem in item.iterdir():
                scan_item(item, subitem)
        #  Перейти до наступного елемента у сканованій теці
        return

    #  Пішла робота з файлом
    ext = get_extension(item.name)  # взяти розширення файлу
    fullname = folder / item.name  # взяти повний шлях к файлу
    if not ext:  # якщо файл не має розширення, додати до невідомих
        # OTHER.append(fullname)
        container = 'OTHERS'
    else:
        try:
            # Взяти список, куди покласти повний шлях до файлу
            container = REGISTER_EXTENSIONS[ext]
        except KeyError:
            # Якщо ми не реєстрували розширення у REGISTER_EXTENSIONS, то додати до іншого
            container = 'OTHERS'
    sort_files(fullname, container, ext)


def help_me(*args):
    return """\nCommand format:
    help or ? - this help;
    parse folder_name - sorts files in the folder;
    good bye or close or exit or . - exit the program"""


def goodbye(*args):
    return 'You have finished working with file_parser'


def handle_file(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.stem) + filename.suffix))


def handle_archive(filename: Path, target_folder: Path):
    # Створюємо теку для архівів
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо теку, куду розпаковуємо архів
    # Беремо суфікс у файлу та прибираємо replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    # Створюємо теку для архіву з іменем файлу

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не вдалося видалити теку {folder}')


def scan(folder: Path):
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Скануємо задану теку
        futures = [executor.submit(scan_item, folder, item) for item in folder.iterdir()]

        for _ in as_completed(futures):
            pass

    # Виконуємо реверс списку для того, щоб всі теки видалити.
    for folder in FOLDERS[::-1]:
        handle_folder(folder)


def file_parser(*args):
    global FOLDERS
    global work_folder
    if len(args) < 1:
        return 'Please enter a folder name'

    if args[0]:
        FOLDERS = []
        work_folder = Path(args[0])
        print(f'\n\033[033mScanning {work_folder}...\033[0m')
        if not work_folder.exists():
            return 'Folder does not exist'

        scan(work_folder.resolve())
        return f'Done in folder {work_folder.resolve()}'


COMMANDS_F = {file_parser: ['parse'], help_me: ['?', 'help'], goodbye: ['good bye', 'close', 'exit', '.']}


def start_fp():
    print('\n\033[033mWelcome to file parser!\033[0m')
    print(f"\033[032mType command or '?' for help \033[0m\n")
    while True:
        with open("history.txt", "wb"):
            pass
        user_command = prompt('Enter command >>> ',
                              history=FileHistory('history.txt'),
                              auto_suggest=AutoSuggestFromHistory(),
                              completer=Completer,
                              lexer=RainbowLexer()
                              )
        command, data = command_parser(user_command, COMMANDS_F)
        print(command(*data), '\n')
        if command is goodbye:
            break


Completer = NestedCompleter.from_nested_dict({'help': None, '?': None, 'parse': None, 'good bye': None,
                                              'close': None, 'exit': None, '.': None})

if __name__ == '__main__':
    work_folder = Path(input('Enter folder name >>> '))
    start_time = datetime.now()
    file_parser(work_folder)
    print(f'\n\033[032mDone in {datetime.now() - start_time} seconds\033[0m')