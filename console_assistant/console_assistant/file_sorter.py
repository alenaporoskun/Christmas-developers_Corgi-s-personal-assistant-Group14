from pathlib import Path

from shutil import unpack_archive


HELP_STRING = "\nThe program launch must contain one argument,"\
              " this is the name of the folder to sort the files.\n"

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
CIRILLIC_TO_LATIN = ("a", "b", "v", "g", "d", "e", "jo", "j", "z", "i", "j",
                     "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                     "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e",
                     "yu", "ya", "je", "i", "ji", "g")

TRANSLATION_MAP = {}
for number in range(len(CIRILLIC_TO_LATIN)):
    TRANSLATION_MAP[ord(CYRILLIC_SYMBOLS[number])] = CIRILLIC_TO_LATIN[number]
    TRANSLATION_MAP[ord(CYRILLIC_SYMBOLS[number].upper())
                    ] = CIRILLIC_TO_LATIN[number].title()

FOLDERS = ["images", "video", "documents", "audio", "archives", "others"]
path_to_folders = []
number_of_files = [0, 0, 0, 0, 0, 0]

ID_FOLDER_ARHIVES = 4


FILE_GROUPS = {'JPEG': 0, 'PNG': 0, 'JPG': 0, 'SVG': 0,
               'AVI': 1, 'MP4': 1, 'MOV': 1, 'MKV': 1,
               'DOC': 2, 'DOCX': 2, 'TXT': 2, 'PDF': 2,
               'XLSX': 2, 'XLS': 2, 'PPTX': 2,
               'MP3': 3, 'OGG': 3, 'WAV': 3, 'AMR': 3,
               'ZIP': 4, 'GZ': 4, 'TAR': 4}

VALUE_FOR_OTHERS = 5

NAME_FILE_EXTENSIONS = 'extensions.txt'

NAME_FILE_FILES = 'files.txt'


def normalize_string(string: str) -> str:
    """
    Returns a normalized string in which Cyrillic characters are replaced
    by Latin characters, also all unknown characters are replaced by '_'
    Args:
        string(str): initial string
    Return:
        str: The normalized string
    """

    transliterated_string = string.translate(TRANSLATION_MAP)

    result = "".join([symbol if symbol.isalnum()
                      else "_" for symbol in transliterated_string])

    return result


def find_all_files(path_to_folder: Path, list_files: list[Path], IGNORED_FOLDERS) -> list[Path]:
    
    for new_path in path_to_folder.iterdir():
        if not new_path in IGNORED_FOLDERS:
            if new_path.is_dir():
                list_files = find_all_files(new_path, list_files, IGNORED_FOLDERS)
            else:
                list_files.append(new_path)

    return list_files


def create_folders(MAIN_FOLDER) -> None:
    for folder in FOLDERS:
        path_to_folder = MAIN_FOLDER / folder
        path_to_folders.append(path_to_folder)
        path_to_folder.mkdir(exist_ok = True)


def create_report_on_extensions(MAIN_FOLDER, list_of_all_files) -> None:
    found_known_extensions = set()
    found_unknown_extensions = set()
    for file_path in list_of_all_files:
        extensions_file = file_path.suffix.lstrip('.').upper()
        if extensions_file in FILE_GROUPS:
            found_known_extensions.add(extensions_file)
        else:
            found_unknown_extensions.add(extensions_file)
    found_known_extensions = sorted(list(found_known_extensions))
    found_unknown_extensions = sorted(list(found_unknown_extensions))
    if len(found_known_extensions) + len(found_known_extensions) > 0:
        with open(MAIN_FOLDER / NAME_FILE_EXTENSIONS, 'w') as fw:
            fw.write("Found known extensions: "+", ".join(found_known_extensions)+'.\n')
            fw.write("Found unknown extensions: "+", ".join(found_unknown_extensions)+'.')


def rename_files(MAIN_FOLDER, list_of_all_files) -> None:
    old_new_name_files = {}
    for old_name_file in list_of_all_files:
        id_folder = FILE_GROUPS.get(old_name_file.suffix.lstrip('.').upper(), VALUE_FOR_OTHERS)
        number_of_files[id_folder] += 1
        new_name_file = normalize_string(old_name_file.stem) + old_name_file.suffix
        new_path_file = Path(MAIN_FOLDER / FOLDERS[id_folder] / new_name_file)
        if new_path_file.is_file():

            # Finding a new file name because such a file already exists
            while True:
                number_of_digits = 0
                name_without_extension = new_path_file.stem
                list_symbols_name_file = list(name_without_extension)
                list_symbols_name_file.reverse()
                for symbol in list_symbols_name_file:
                    if symbol.isdigit():
                        number_of_digits += 1
                    else:
                        break
                if number_of_digits == 0:
                    new_name_file = name_without_extension + "1" + old_name_file.suffix
                else:
                    number_file = str(int(name_without_extension[-number_of_digits:])+1)
                    if number_of_digits == len(name_without_extension):
                        new_name_file = number_file + old_name_file.suffix
                    else:
                        new_name_file = name_without_extension[
                                    :len(name_without_extension)-number_of_digits
                                        ] + number_file + old_name_file.suffix
                new_path_file = Path(MAIN_FOLDER / FOLDERS[id_folder] / new_name_file)
                if not new_path_file.is_file():
                    break
        
        old_new_name_files[str(old_name_file)] = [id_folder, new_name_file, new_path_file.stem]
        old_name_file.rename(new_path_file)
    
    if len(old_new_name_files) == 0:
        return
    
    # Create report on files
    with open(MAIN_FOLDER / NAME_FILE_FILES, 'w') as fw:
        for id_folder in range(VALUE_FOR_OTHERS+1):
            if number_of_files[id_folder] == 0:
                continue
            if id_folder == ID_FOLDER_ARHIVES:
                fw.write(f"Archives in folder {FOLDERS[id_folder]}:\n")
            else:
                fw.write(f"Files in folder {FOLDERS[id_folder]}:\n")
            for old_name_file in old_new_name_files:
                old_new_name_file_id = old_new_name_files[old_name_file][0]
                new_name_file = old_new_name_files[old_name_file][1]
                if id_folder == old_new_name_file_id:
                    if id_folder == ID_FOLDER_ARHIVES:
                        fw.write(f"{old_name_file} -> {old_new_name_files[old_name_file][2]}\n")
                    else:
                        fw.write(f"{old_name_file} -> {new_name_file}\n")
            fw.write("\n\n")


def unpack_the_archives(MAIN_FOLDER) -> None:
    path_to_arhives = Path(MAIN_FOLDER / FOLDERS[ID_FOLDER_ARHIVES])
    list_arhives = []
    for path_arhive in path_to_arhives.iterdir():
        if path_arhive.is_file():
            list_arhives.append(path_arhive)
    for path_arhive in list_arhives:
        folder_for_file = path_to_arhives / path_arhive.stem
        folder_for_file.mkdir(exist_ok = True)
        try:
            unpack_archive(str(path_arhive.absolute()), str(folder_for_file.absolute()))    
        except:
            folder_for_file.rmdir()
            return
        path_arhive.unlink()


list_all_folders = []

def find_all_folders(path_to_folder: Path):
    for new_folder in path_to_folder.iterdir():
        if new_folder.is_dir():
            list_all_folders.append(new_folder)
            find_all_folders(new_folder)

def delete_empty_folders(MAIN_FOLDER):
    find_all_folders(MAIN_FOLDER)
    list_all_folders.reverse()
    list_del = []
    for folder in list_all_folders:
        new_path = ""
        for new_path in folder.iterdir():
            break
        if not new_path:
            folder.rmdir()


def sorter(new_folder = "example"):
        # за замовчування папка - example ,
        # щоб не сортувавало поточну папку при пустому параметрі
        MAIN_FOLDER = Path(new_folder)
        if not MAIN_FOLDER.is_dir():
            print(f"\nFolder {MAIN_FOLDER} not found.")
        else:
            IGNORED_FOLDERS = [MAIN_FOLDER / folder for folder in FOLDERS]
            list_of_all_files = find_all_files(MAIN_FOLDER, [], IGNORED_FOLDERS)
            create_folders(MAIN_FOLDER)
            create_report_on_extensions(MAIN_FOLDER, list_of_all_files)
            rename_files(MAIN_FOLDER, list_of_all_files)
            unpack_the_archives(MAIN_FOLDER)
            delete_empty_folders(MAIN_FOLDER)
            print(f"Folder {MAIN_FOLDER} is sorted.")


if __name__ == "__main__":
    sorter()
