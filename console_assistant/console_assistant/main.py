from collections import UserDict
from datetime import datetime
from pickle import dump
from pickle import load
from os import path
from os import makedirs

from rich.console import Console
from rich.table import Table

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from re import fullmatch
from re import IGNORECASE


# Спробуємо імпортувати модуль sorter з пакету file_sorter.
# Якщо модуль не знайдено (ModuleNotFoundError), то спробуємо
# імпортувати його з іншого шляху.     
try:
    from console_assistant.file_sorter import sorter
except ModuleNotFoundError: 
    from file_sorter import sorter

# Регулярний вираз для перевірки email
EMAIL_REGULAR = r"[a-z][a-z0-9_.]+[@][a-z.]+[.][a-z]{2,}"

# Отримуємо повний шлях до поточного робочого каталогу,
# де розташований цей скрипт
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Побудуємо абсолютний шлях до файлу address_book.pkl у підкаталозі 'data'
FILENAME = path.join(CURRENT_DIRECTORY, 'data', 'address_book.pkl')

# Побудуємо абсолютний шлях до файлу notes.pkl у підкаталозі 'data'
FILENAME2 = path.join(CURRENT_DIRECTORY, 'data', 'notes.pkl')

def main() -> None:
    # Створення папки 'data'
    data_folder_path = path.join(CURRENT_DIRECTORY, 'data')
    makedirs(data_folder_path, exist_ok=True)

    # Завантаження адресної книги або створення нової
    book = load_book()

    print("Hi! I am Mr.Corgi's Personal Assistant. How can I help you?")

    # Список доступних команд
    commands = ['help', 'add-contact', 'show-contacts', 'edit-contact',
                'delete-contact', 'delete-phone', 'upcoming-birthdays', 
                'add-note', 'show-notes', 'search-contact', 'search-notes',
                'edit-note', 'delete-note', 'sort-files', 'exit']

    # Створення об'єкту WordCompleter, який використовується
    # для автодоповнення команд
    completer = WordCompleter(commands, ignore_case=True)

    # Запит на введення команди від користувача з можливістю автодоповнення
    command = prompt('Write a command (help - all commands): ',
                      completer=completer)

    # Цикл для команд в консолі 
    while command != 'exit':

        if command == 'help':
            # Вивід меню команд
            print_menu_commmands()

        elif command[:11] == 'add-contact':
            words_commands = command.split() # розділення рядка на масив слів
            # Додавання контакту
            if len(words_commands) < 2:
                name_contact = input('Enter name of contact: ')
            else:
                name_contact = ' '.join(words_commands[1:])
            fun_add_contact(book, name_contact)

        elif command == 'show-contacts':
            # Виведення всіх записів у книзі
            print_table(book, "Book of gift recipients")
        
        elif command[:12] == 'edit-contact':
            words_commands = command.split() # розділення рядка на масив слів
            # Редактування контакту
            if len(words_commands) < 2:
                fun_edit_contact(book)
            else:
                name_contact = ' '.join(words_commands[1:])
                fun_edit_contact(book, name_contact)

        elif command == 'delete-contact':
            # Видалення контакту
            fun_delete_contact(book)
        
        elif command == 'delete-phone':
            # Видалення контакту
            fun_delete_phone(book)

        elif command == 'upcoming-birthdays':
            # Вивід контакту у якого через n днів день народження
            fun_upcoming_birthdays(book)
        
        elif command == 'add-note':
            # Додавання нотатки
            fun_add_note(book)

        elif command == 'show-notes':
            # Вивід нотаток
            fun_show_notes(book, FILENAME2)

        elif command == 'search-contact':
            # Пошук контактів серед контактів книги
            book.search_contact()

        elif command == 'search-notes':
            # Пошук нотатки серед нотаток книги
            fun_search_notes(book, FILENAME2)

        elif command == 'edit-note':
            # Редагування нотатки
            fun_edit_note(book)

        elif command == 'delete-note':
            # Відалення нотатки
            fun_delete_note(book)

        elif command == 'sort-files':
            # Сортування файлів по папкам 
            fun_sort_files()

        else: 
            print("The command was not found. Please enter another command.")

        # Запит на введення команди від користувача з можливістю автодоповнення
        command = prompt('Write a command (help - all commands): ',
                          completer=completer)

        # Збереження книги
        save_book(book)


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    # реалізація класу
    def __init__(self, value: str):
        self.value = value

    # getter
    @property
    def value(self) -> str:
        return self._value

    # setter
    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value


class Phone(Field):
    def __init__(self, value: str):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value: str) -> bool:
        return len(value) == 10 and value.isdigit()
    
    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)


class Email(Field):
    def __init__(self, value: str):
        if not self.is_valid_email(value):
            raise ValueError('Invalid email format')
        super().__init__(value)

    @staticmethod
    def is_valid_email(value: str) -> bool:
        return fullmatch(EMAIL_REGULAR, value, flags = IGNORECASE) is not None
    
    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        if not self.is_valid_email(new_value):
            raise ValueError('Invalid email format')
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)

    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value)

    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

class Notes:
    def __init__(self, text: str, author: str, tags: list = None):
        self.text = text
        self.author = author
        self.tags = tags if tags is not None else []

    def __str__(self) -> str:
        tags_str = ', '.join(self.tags) if hasattr(self, 'tags') else ''
        return f"{self.text} (by {self.author}, Tags: {tags_str})"
    
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note_with_tags(self, author: str, text: str, tags: list) -> None:
        note = Notes(text, author, tags)
        self.notes.append(note)

    def print_notes(self) -> None:
        if self.notes:
            console = Console()
            table = Table(title="Wish list", show_header=True,
                          header_style="bold magenta")
            table.title_align = "center"
            table.title_style = "bold yellow"
            table.add_column("Index", style="cyan", width=5, justify="center")
            table.add_column("Note", style="green")
            table.add_column("Author", style="blue")
            table.add_column("Tags", style="magenta")  # Додавання стовпця для тегів

            for i, note in enumerate(self.notes, start=1):
                # Перевірка, чи note має атрибут tags перед його використанням
                tags_str = ', '.join(note.tags) if hasattr(note, 'tags') else ''
                table.add_row(str(i), note.text, note.author, tags_str)

            console.print(table)
        else:
            print("No notes available.")

    def save_notes(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            dump(self.notes, file)

    def load_notes(self, filename: str) -> list:
        try:
            with open(filename, 'rb') as file:
                self.notes = load(file)
        except FileNotFoundError:
            self.notes = []

    def edit_note(self, index: int, new_text: str = None,
                        new_tags: list = None) -> None:
        # Редагує нотатку з вказаним індексом.
        # index: Індекс нотатки для редагування
        # new_text: Новий текст нотатки
        # new_tags: Нові теги нотатки
        
        if 1 <= index <= len(self.notes):
            note = self.notes[index - 1]
            note.text = new_text
            note.tags = new_tags
            print(f"Note {index} edited successfully.")
        else:
            print("Invalid note index.")

    def delete_note(self, index: int) -> None:
        if 1 <= index <= len(self.notes):
            deleted_note = self.notes.pop(index - 1)
            print(f"Note {index} deleted: {deleted_note}")
        else:
            print("Invalid note index.")

    def update_notes_author(self, old_author: str, new_author: str,
                                  filename: str):
        for note in self.notes:
            if note.author == old_author:
                note.author = new_author

        # Збереження оновленного нотатка у файл
        self.save_notes(filename)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None
        self.notes = []

    def add_phone(self, phone: str) -> None:
        phone = Phone(phone)
        self.phones.append(phone)
        
    def add_email(self, email: str) -> None:
        email = Email(email)
        self.email = email
            
    def edit_phone(self, old_phone: str = None, new_phone: str = None) -> None:
        # Редагування телефону
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        
        if not found:
            raise ValueError(f"Phone {old_phone} not found in the record")
    
    def edit_email(self, new_email: str) -> None:
        if not Email.is_valid_email(new_email):
            raise ValueError('Invalid email format')
        self.email.value = new_email

    def remove_phone(self, number: str) -> None:
        # Видалення телефону
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)

    def find_phone(self, number: str) -> str:
        # Знаходження телефону
        for phone in self.phones:
            if phone.value.lower() == number:
                return phone
        return None

    def set_birthday(self, birthday: str) -> None:
        # Перевірка коректності формату дати та збереження в атрибут birthday
        try:
            self.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid birthday date format. Use YYYY-MM-DD.")

    def set_address(self, address: str) -> None:
        self.address = Birthday(address)

    def days_to_birthday(self) -> int:
        # Знаходження кількості днів до дня народження
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
            delta = next_birthday - today
            return f'There are {delta.days} days left before the birthday.'
        else:
            return None

    def __str__(self) -> str:
        # Виведення даних у вигляді рядка при виклику print(), str()
        contact_info = f"Contact name: {self.name.value}"
        if self.phones:
            contact_info += f", phones: {'; '.join(p.value for p in self.phones)}"
        if self.email is not None:
            contact_info += f", email: {self.email.value}"
        if self.birthday:
            contact_info += f", birthday: {self.birthday.strftime('%Y-%m-%d')}"
        if self.address:
            contact_info += f", address: {self.address.value}"
        if self.notes:
            contact_info += f" \nNotes: \n "
            for i, note in enumerate(self.notes, start = 1):
                contact_info += f"{i}.{note}\n"
        return contact_info


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notes_manager = NoteManager()

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def add_note(self, text: str) -> None:
        self.notes_manager.add_note(text)

    def print_notes(self) -> None:
        self.notes_manager.print_notes()

    def find(self, name: str) -> str:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def update_contact_name(self, old_name: str, new_name: str,
                                  notes_manager: NoteManager) -> None:
        # Оновлення імені контакту

        # Перевірка, чи ім'я контакту існує в адресній книзі
        if old_name in self.data:
            # Вилучення запису за старим ім'ям
            record = self.data.pop(old_name)
            # Оновлення імені в самому об'єкті запису
            record.name.value = new_name
            # Додавання оновленого запису з новим іменем до адресної книги
            self.data[new_name] = record

            # Оновлення імені в нотатках
            notes_manager.update_notes_author(old_name, new_name, FILENAME2)
            
    def __iter__(self):
        return AddressBookIterator(self, items_per_page = 5)
    # items_per_page - кількість записів на сторінці

    def search_contact(self) -> None:
        # пошук контактів серед контактів книги
        search_query = input("Enter search term: ")
        results, suggestions = self.search(search_query)

        if results:
            new_book = AddressBook()
            for record in set(results):
                new_book.add_record(record)
            print_table(new_book, "Search results")
        elif suggestions:
            print(f"Possible suggestions: {', '.join(suggestions)}")
        else:
            print(f"Contact '{search_query}' not found. Phone number, address, and email were also not found.")

    def search(self, query: str) -> (list, list):
        results = []
        suggestions = []

        try:
            int(query[0])
        except ValueError:
            query_lower = query.lower()
            for name, record in self.data.items():
                # Пошук за ім'ям, адресою та електронною поштою
                if (
                    query_lower in name.lower()
                    or (record.email and query_lower in record.email.value.lower())
                    or (record.address and query_lower in record.address.value.lower())
                ):
                    results.append(record)
                elif name.lower().startswith(query_lower):
                    # Додавання рекомендації, якщо збігається початок імені
                    suggestions.append(name)
            # Пошук за номером телефону
            for record in self.data.values():
                for phone in record.phones:
                    if query_lower in phone.value.lower():
                        results.append(record)

        else:
            # Пошук за номером телефону
            for name, record in self.data.items():
                for phone in record.phones:
                    if query.lower() in phone.value.lower():
                        results.append(record)

        return results, suggestions


class AddressBookIterator:
    def __init__(self, address_book: AddressBook, items_per_page: int):
        self.address_book = address_book
        self.items_per_page = items_per_page
        # Визначається поточна сторінка, починаючи з нуля (перша сторінка)
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self) -> list[Record]:
        # Метод обчислює індекс початку (start) і кінця (end) діапазону
        # записів, які повинні бути виведені на поточній сторінці. 
        # Наприклад, якщо items_per_page дорівнює 5, то на першій сторінці
        # будуть виводитися записи з індексами 0 до 4, 
        # на другій сторінці - з 5 до 9, і так далі.
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        records = list(self.address_book.data.values())[start:end]

        if not records:
            raise StopIteration

        self.current_page += 1
        return records


def load_book() -> AddressBook:
    # Завантаження адресної книги з файлу
    try:
        with open(FILENAME, 'rb') as file: 
            return load(file)
    except FileNotFoundError:
        return AddressBook()

def save_book(address_book: AddressBook) -> None:
    # Збереження адресної книги у файл
    with open(FILENAME, 'wb') as file:
        dump(address_book, file)


def print_menu_commmands() -> None:
    # Друк команд
    print('''All commands:
    - add-contact [name]  - add contact with it's name
    - edit-contact [name] - edit contact information
    - delete-contact      - delete contact
    - delete-phone        - delete phone from some contact
    - show-contacts       - display all contacts in the book
    - search-contact      - search for contacts in the book 
    - upcoming-birthdays  - display a list of contacts whose birthday is a specified number of days from the current date
    - add-note            - add note with author if he/she is in the book
    - show-notes          - show all notes with authors and tags
    - search-notes        - search for a note by word or author
    - edit-note           - editing a note
    - delete-note         - delete note
    - sort-files          - sort files in a directory
    - exit                - exit the Assistant
    ''')


def fun_add_contact(address_book, name: str) -> None:
    # Функція для додавання контакту в адресну книгу

    if name in address_book.data:
        print('Such a contact already exists.')
        return
    elif name == "":
        print('Name cannot be empty.')
        return

    # Створюється новий запис (контакт) з ім'ям name
    record = Record(name)

    # Додається створений запис в адресну книгу
    address_book.add_record(record)

    # Користувачу пропонується ввести телефон для контакту
    phone = input(f'Enter the phone of contact {name} (10 digits) (c - close): ')

    # Ввод телефонів для контакту, можливо введення 'c' для закриття
    phones = []
    while phone != 'c':
        try:
            # Додає телефон до запису контакту
            if not phone in phones:
                record.add_phone(phone)
                phones.append(phone)
            else:
                print('The phone is already in the phone list.')
            phone = input(f'Enter the phone of contact {name} (10 digits) (c - close): ')
        except ValueError:
            # Обробка виключення, якщо введено некоректний телефон
            phone = input(f'Enter the phone (10 digits) (c - close): ')

    # Користувачу пропонується ввести день народження для контакту
    birthday = input(f'Enter the birthday of contact {name} (Year-month-day) (c - close): ')

    # Ввод дня народження для контакту, можливо введення 'c' для закриття
    while birthday != 'c':
        try:
            # Встановлює день народження для запису контакту
            record.set_birthday(birthday)
            break
        except ValueError:
            # Обробка виключення, якщо введено некоректний формат дня народження
            birthday = input(f'Enter the birthday (Year-month-day) (c - close): ')

    # Користувачу пропонується ввести електронну пошту для контакту
    email = input(f'Enter the email adress (c - close): ')

     # Ввод електронної пошти для контакту, можливо введення 'c' для закриття
    while email != 'c':
        try:
             # Додає електронну пошту до запису контакту
            record.add_email(email)
            break
        except ValueError:
            # Обробка виключення, якщо введено некоректний формат електронної пошти
            email = input('Enter a valid email (c - close): ')

    # Користувачу пропонується ввести адресу для контакту
    address = input(f'Enter the address of contact {name} (c - close): ')

    # Якщо адреса не 'c', встановлює адресу для запису контакту
    if address != 'c':
        record.set_address(address)


def fun_edit_contact(address_book: AddressBook, contact_name: str = "") -> None:
    if not contact_name:
        contact_name = input('Write the name of contact in which you want to'\
                             ' change something: ')

    if contact_name in address_book.data:
        contact_edit = address_book.data[contact_name]
        print(f'Contact found')

        while True:
            edit = input('Enter what you want to edit(n - name, p - phone, ' \
                         'b - birthday, a - address, e - email) (c - close): ')

            if edit.lower() == 'c':
                break 

            elif edit == 'n':
                new_name = input('Enter the new name (c - close): ')
                if new_name.lower() != 'c':
                    # Перевіряємо, чи нове ім’я вже існує в адресній книзі
                    if new_name in address_book.data:
                        print('A contact with that name already exists.')
                    elif new_name == "":
                        print('New name cannot be empty. Contact name not updated.')
                    else:
                        # Оновлюємо ім’я контакту в адресній книзі
                        address_book.update_contact_name(contact_name, new_name,
                                                    address_book.notes_manager)
                        print(f'Contact name update to {new_name}.')
                        contact_name = new_name
                else:
                    print('Name not changed')

            elif edit == 'p':
                new_phone = input("Enter new phone number (10 digits) (c - close): ")
                while new_phone != 'c':
                    try:
                        if not (len(new_phone) == 10 and new_phone.isdigit()):
                            raise ValueError
                        len_phones = len(contact_edit.phones)
                        if  len_phones == 0:
                            contact_edit.add_phone(new_phone)
                        elif len_phones == 1:
                            while True:
                                choice = input('Enter what you want (c - correct phone ' \
                                               f'{contact_edit.phones[0].value}, a - add a new phone): ')
                                if choice == 'c':
                                    contact_edit.edit_phone(contact_edit.phones[0].value,
                                                             new_phone)
                                    break
                                elif choice == 'a':
                                    contact_edit.add_phone(new_phone)
                                    break
                        else:
                            question_text = 'What phone number will we correct: '
                            for i in range(len_phones):
                                question_text += str(i + 1) + ' - ' + contact_edit.phones[i].value + ', '
                            question_text += str(len_phones + 1) + ' - add a new phone: '
                            while True:
                                number = input(question_text)
                                if number.isdigit():
                                    number = int(number)
                                    if number > 0 and number < len_phones + 2:
                                        break
                                    else:
                                        print('Incorrect number.')
                                else:
                                    print('Only numbers are required.')
                            if number > 0 and number <= len_phones:
                                contact_edit.edit_phone(contact_edit.phones[number - 1].value, new_phone)
                            else:
                                contact_edit.add_phone(new_phone)
                        new_phone = input("Enter new phone number (c - close): ")
                    except ValueError:
                        new_phone = input('Enter the valid phone (10 digits) (c - close): ')
            elif edit == 'b':
                new_birthday = input('Enter new birthday (Year-month-day) (c - close): ')
                while new_birthday != 'c':
                    try:
                        contact_edit.set_birthday(new_birthday)
                        break
                    except ValueError:
                        new_birthday = input('Enter the birthday (Year-month-day) (c - close): ')
            elif edit == 'a':
                new_address = input('Enter new address (c - close): ')
                if new_address != 'c':
                    contact_edit.set_address(new_address)
            elif edit == 'e':
                new_email = input('Enter new email (c - close): ')
                while new_email != 'c':
                    try:
                        if contact_edit.email:
                            contact_edit.edit_email(new_email)
                        else:
                            contact_edit.add_email(new_email)
                        break
                    except ValueError:
                        new_email = input('Enter a valid email (c - close): ')
            else:
                print('Invalid comand.')
    else:
        print(f'Contact {contact_name} not found.')


def fun_delete_contact(address_book: AddressBook) -> None:
    # Видалення контакту з книги контактів
    contact_name = input('Enter the name of contact you want to delete: ')
    if contact_name in address_book.data:
        question = input('Are you sure you want to delete this contact' \
                         f' {contact_name}? (yes or no): ')
        if question == 'yes':
            del address_book.data[contact_name]
            print('Contact deleted')
        else:
            print('Deletion canceled')
    else:
        print(f'Contact with the name {contact_name} not found.')


def fun_delete_phone(address_book: AddressBook) ->None:
    # Видалення телефону якогось контакту
    contact_name = input('Enter the name of contact: ')
    if contact_name in address_book.data:
        contact_edit = address_book.data[contact_name]
        if len(contact_edit.phones) > 0:
            while len(contact_edit.phones) > 0:
                phones = []
                for i in range(len(contact_edit.phones)):
                    phones.append(contact_edit.phones[i].value)
                del_phone = input('Enter phone number to delete (c - close): ')
                if del_phone == 'c':
                    break
                if del_phone in phones:
                    contact_edit.remove_phone(del_phone)
                    print('Phone number deleted.')
                else:
                    print('Phone number not found.')
        else:
            print('There are no phone numbers to delete.')            
    else:
        print(f'Contact with the name {contact_name} not found.')


def print_table(AddressBook, text_title: str) -> None:
    # Виведення у вигляді таблиці

    # Перевірка на порожню книгу
    if not AddressBook.data:
        print("The book of gift recipients is empty.")
        return 

    # Створення об'єкту Console
    console = Console()

    # Створення таблиці
    table = Table(title = text_title, show_header=True, header_style="bold magenta")
    table.title_align = "center"
    table.title_style = "bold yellow"

    # Додавання стовпців до таблиці
    table.add_column("Contact name", style="magenta", width=20, justify="center")
    table.add_column("Phones", style="cyan", width=40, justify="center")
    table.add_column("Birthday", style="green", width=20, justify="center")
    table.add_column("Address", style="yellow", width=40, justify="center")
    table.add_column("Email", style="red", width=40, justify="center")

    # Додавання даних до таблиці
    for name, record in AddressBook.data.items():
        table.add_row(
            str(record.name.value),
            "; ".join(str(phone) for phone in record.phones),
            record.birthday.strftime('%Y-%m-%d') if record.birthday else "",
            str(record.address.value) if record.address else "",
            str(record.email.value) if record.email else "",
        )

    # Виведення таблиці
    console.print(table)
    print()


def fun_upcoming_birthdays(address_book: AddressBook) -> None:
    # Команда для виводу наближених днів народження
    days_count = input('Enter the number of days to check upcoming birthdays: ')
    try:
        days_count = int(days_count)
        if days_count < 0:
            raise ValueError("Please enter a non-negative number of days.")
    except ValueError:
        print("Invalid input. Please enter a non-negative integer.")

    upcoming_birthdays = get_upcoming_birthdays(address_book, days_count)
    if upcoming_birthdays:
        new_book = AddressBook()
        for contact in upcoming_birthdays:
            new_book.add_record(contact)
        print_table(new_book, f'Upcoming birthdays within the next {days_count} days')
    else:
        print(f'No upcoming birthdays within the next {days_count} days.')


def get_upcoming_birthdays(address_book: AddressBook, days_count: int) -> list:
    # Список для зберігання записів з найближчими днями народженнями
    upcoming_birthdays = []    

    # Отримання поточної дати та часу                
    today = datetime.today()          

    # Перебір записів у адресній книзі       
    for record in address_book.data.values():
        # Перевірка, чи є в запису вказана дата народження

        if record.birthday:                    
            # Формування дати наступного дня народження
            next_birthday = datetime(today.year, record.birthday.month, record.birthday.day+1)  

            # Якщо день народження вже минув у поточному році, обчислити для наступного року        
            if next_birthday < today:                                                                  
                next_birthday = datetime(today.year + 1, record.birthday.month, record.birthday.day)  

            # Обчислення різниці в часі між сьогоднішньою датою і наступним днем народження
            delta = next_birthday - today       

            # Перевірка, чи день народження відбудеться в межах визначеної кількості днів                                                   
            if 0 <= delta.days <= days_count:                                              
                upcoming_birthdays.append(record)

    # Повернення списку з записами, у яких найближчий день народження наступає впродовж зазначеної кількості днів
    return upcoming_birthdays                                                                          


def fun_add_note(address_book: AddressBook) -> None:
    # Додавання нотатки
    author = input('Enter an author of note (c - close): ')

    # Перевірка, чи користувач вибрав опцію закриття
    if author.lower() == 'c':
        return

    # Перевірка, чи автор існує в телефонній книзі
    if author not in address_book.data:
        print('The author is not found in the book of gift recipients.')
        return

    # Введення тексту нотатки та тегів
    while True:
        note_text = input('Enter your note (c - close): ')
        if note_text.lower() == 'c':
            break

        tags_input = input('Enter tags (comma-separated): ')
        tags = [tag.strip() for tag in tags_input.split(',')]
        
        # Додавання нотатки та тегів до менеджера нотаток
        address_book.notes_manager.add_note_with_tags(author, note_text, tags)
        print('Note added successfully!')

    # Збереження нотаток у файл
    address_book.notes_manager.save_notes(FILENAME2)


def fun_show_notes(address_book: AddressBook, filename: str) -> None:
    # Функція для відображення нотаток з файла

    # Завантажує нотатки з файлу в об'єкт notes_manager
    address_book.notes_manager.load_notes(filename)

    # Виводить всі нотатки за допомогою методу print_notes
    address_book.notes_manager.print_notes()

def fun_search_notes(address_book: AddressBook, filename: str) -> None:
    # Пошук нотатки за словами або автором
    search_term = input(
        'Enter search term (leave blank to show all notes): ').lower()

    # Завантаження нотатки з файлу в об'єкт notes_manager
    address_book.notes_manager.load_notes(filename)

    # Фільтрування нотаток за словом або автором
    filtered_notes = [note for note in address_book.notes_manager.notes if search_term in note.text.lower() 
                      or search_term in note.author.lower()]

    # Виведення знайдених нотаток
    if filtered_notes:
        console = Console()
        table = Table(title='Search results', show_header=True,
                      header_style='bold magenta')
        table.title_align = 'center'
        table.title_style = 'bold yellow'
        table.add_column('Index', style='cyan', width=5, justify='center')
        table.add_column('Note', style='green')
        table.add_column('Author', style='blue')

        for i, note in enumerate(filtered_notes, start=1):
            table.add_row(str(i), note.text, note.author)

        console.print(table)
    else:
        print(f"No notes found for the search term '{search_term}'.")

def fun_edit_note(address_book: AddressBook) -> None:
    if isinstance(address_book, AddressBook):
        address_book.notes_manager.load_notes(FILENAME2)
        address_book.notes_manager.print_notes()
        
        try:
            index_to_edit = int(input('Enter the index of the note to edit (0 - cancel): '))
            if index_to_edit == 0:
                return  # Редагування скасовано
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return
        
        if 1 <= index_to_edit <= len(address_book.notes_manager.notes):
            new_text = input('Enter the new text for the note: ')
            new_tags_input = input("Enter new tags (comma-separated): ")
            new_tags = [tag.strip() for tag in new_tags_input.split(',')]
            address_book.notes_manager.edit_note(index_to_edit, new_text, new_tags)
            address_book.notes_manager.save_notes(FILENAME2)
            
        else:
            print("Invalid note index.")
    
def fun_delete_note(address_book:AddressBook) -> None:
    address_book.notes_manager.load_notes(FILENAME2)
    address_book.notes_manager.print_notes()
    index_to_delete = int(input('Enter the index of the note to delete (0 - cancel): '))

    if index_to_delete == 0:
        return  # Скасувати видалення
    
    address_book.notes_manager.delete_note(index_to_delete)
    address_book.notes_manager.save_notes(FILENAME2)
    print('Note deleted successfully!')


def fun_sort_files() -> None:
    # за замовчування папка - example ,
    # щоб не сортувавало поточну папку при пустому параметрі
    folder = ''
    while folder != 'c':
        folder = input('Enter the directory to sort (c - cancel): ').strip()
        if folder and folder != 'c':
            sorter(folder)


if __name__ == "__main__":
    main()
