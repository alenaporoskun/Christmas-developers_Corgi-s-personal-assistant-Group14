from collections import UserDict
from datetime import datetime
from pickle import dump, load
from os import path

from rich.console import Console
from rich.table import Table

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from re import fullmatch
from re import IGNORECASE

# Регулярний вираз для перевірки email
EMAIL_REGULAR = r"[a-z][a-z0-9_.]+[@][a-z.]+[.][a-z]{2,}"

# Отримання поточного каталогу, в якому знаходиться виконуваний файл
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Створення повного шляху до файлу "address_book.pkl" в поточному каталозі
FILENAME = path.join(CURRENT_DIRECTORY, 'address_book.pkl')

FILENAME2 = path.join(CURRENT_DIRECTORY, 'notes.pkl')
            
def main():
    # Завантаження адресної книги або створення нової
    book = load_book()

    print("Hi! I am Santa's Personal Assistant - Mr.Corgi. How can I help you?")

    # Список доступних команд
    commands = ['add-contact', 'show-contacts', 'edit-contact', 'delete-contact', 'upcoming-birthdays', 
                'add-note', 'show-notes', 'search-contact', 'search-notes', 'exit']

    # Створення об'єкту WordCompleter, який використовується для автодоповнення команд
    completer = WordCompleter(commands, ignore_case=True)

    # Запит на введення команди від користувача з можливістю автодоповнення
    command = prompt('Write a command (help - all commands): ', completer=completer)

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
            print_table(book, "Contact book")
        
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


        else: 
            print("The command was not found. Please enter another command.")

        # Запит на введення команди від користувача з можливістю автодоповнення
        command = prompt('Write a command (help - all commands): ', completer=completer)

        # Збереження книги
        save_book(book)


def load_book():
    # Завантаження адресної книги з файлу
    try:
        with open(FILENAME, 'rb') as file: 
            return load(file)
    except FileNotFoundError:
        return AddressBook()


def save_book(address_book):
    # Збереження адресної книги у файл
    with open(FILENAME, 'wb') as file:
        dump(address_book, file)


def print_menu_commmands():
    # Друк команд
    print('''All commands:
    - add-contact [name]  - add contact with it's name
    - edit-contact [name] - editing contact information
    - delete-contact      - deleting contact
    - show-contacts       - displays all contacts in the address book
    - upcoming-birthdays  - display a list of contacts whose birthday is a specified number of days from the current date
    - search-contact      - search for contacts in the address book
    - add-note            - add note with author if he/she is in the contact book
    - show-notes          - show all notes with authors
    - search-notes        - search for a note by word or author
    - exit                - enter 'exit' to exit the Assistant
    ''')


def fun_add_contact(address_book, name):
    # Функція для додавання контакту в адресну книгу

    # Створюється новий запис (контакт) з ім'ям name
    record = Record(name)

    # Додається створений запис в адресну книгу
    address_book.add_record(record)

    # Користувачу пропонується ввести телефон для контакту
    phone = input(f'Enter the phone of contact {name} (c - close): ')

    # Ввод телефонів для контакту, можливо введення 'c' для закриття
    while phone != 'c':
        try:
            # Додає телефон до запису контакту
            record.add_phone(phone)
            phone = input(f'Enter the phone of contact {name} (c - close): ')
        except ValueError:
            # Обробка виключення, якщо введено некоректний телефон
            phone = input(f'Enter the phone (10 digits) (c - close): ')

    # Користувачу пропонується ввести день народження для контакту
    birthday = input(f'Enter the birthday of contact {name} (c - close): ')

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
            email = input('Enter a valid email format (c - close): ')

    # Користувачу пропонується ввести адресу для контакту
    address = input(f'Enter the address of contact {name} (c - close): ')

    # Якщо адреса не 'c', встановлює адресу для запису контакту
    if address != 'c':
        record.set_address(address)


def fun_edit_contact(address_book, contact_name = ""):
    if not contact_name:
        contact_name = input('Write the name of contact in which you want to change something: ')
    if contact_name in address_book.data:
        contact_edit = address_book.data[contact_name]
        print(f'Contact found')
        while True:
            edit = input('Enter what you want to edit(p - phone, b - birthday, a - address, e - email) (c - close): ')
            if edit.lower() == 'c':
                break 
            try:
                if edit == 'p':
                    new_phone = input("Enter new phone number: ")
                    if contact_edit.phones:
                        contact_edit.edit_phone(contact_edit.phones[0].value, new_phone)
                    else:
                        contact_edit.add_phone(new_phone)
                elif edit == 'b':
                    new_birthday = input('Enter new birthday: ')
                    contact_edit.set_birthday(new_birthday)
                elif edit == 'a':
                    new_address = input('Enter new address: ')
                    contact_edit.set_address(new_address)
                elif edit == 'e':
                    new_email = input('Enter new email: ')
                    if contact_edit.email:
                        contact_edit.edit_email(new_email)
                    else:
                        contact_edit.add_email(new_email)

                else:
                    print('Ivailid comand, please enter(phone, birthday, address, email) (c - close): ')
            except ValueError:
                edit = input('Ivailid comand, please enter(phone, birthday, address, email) (c - close): ')
    else:
        print(f'Contact {contact_name} not found')


def fun_delete_contact(address_book):
    # Видалення контакту з книги контактів
    contact_name = input('Enter the name of contact you want to delete: ')
    if contact_name in address_book.data:
        question = input(f'Are you sure you want to delete this contact {contact_name}? (yes or no): ')
        if question == 'yes':
            del address_book.data[contact_name]
            print('Contact deleted')
        else:
            print('Deletion canceled')
    else:
        print(f'contact with thw name {contact_name} not found.')


def print_table(AddressBook, text_title):
    # Виведення у вигляді таблиці

    # Перевірка на порожню книгу
    if not AddressBook.data:
        print("\n Книга порожня.\n")
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


def fun_upcoming_birthdays(address_book):
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


def get_upcoming_birthdays(address_book, days_count):
    # Список для зберігання записів з найближчими днями народженнями
    upcoming_birthdays = []    

    # Отримання поточної дати та часу                
    today = datetime.today()          

    # Перебір записів у адресній книзі       
    for record in address_book.data.values():
        # Перевірка, чи є в запису вказана дата народження

        if record.birthday:                    
            # Формування дати наступного дня народження
            next_birthday = datetime(today.year, record.birthday.month, record.birthday.day)  

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


def fun_add_note(address_book):
    # Функція для додавання нотаток в адресну книгу

    author = input('Enter an author of note (c - close): ')
    if author not in address_book.data:
        print('The author is not found in the contact book.')
        return

    # Користувачу пропонується ввести текст нотатки (до тих пір, поки не введе 'c' або 'C' для закриття)
    note_text = input('Enter your note (c - close): ')

    while note_text.lower() != 'c':
        # Додає нотатку до об'єкту notes_manager в адресній книзі
        address_book.notes_manager.add_note(author, note_text)

        # Виводить повідомлення про успішне додавання нотатки
        print('Note added successfully!')

         # Знову запитує користувача ввести нотатку або закрити введення
        note_text = input('Enter your note (c - close): ')

    # Після закриття введення зберігає всі нотатки в файл з ім'ям FILENAME2
    address_book.notes_manager.save_notes(FILENAME2)


def fun_show_notes(address_book, filename):
    # Функція для відображення нотаток з файла

    # Завантажує нотатки з файлу в об'єкт notes_manager
    address_book.notes_manager.load_notes(filename)

    # Виводить всі нотатки за допомогою методу print_notes
    address_book.notes_manager.print_notes()

def fun_search_notes(address_book, filename):
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
        table = Table(title='Notes', show_header=True,
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

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        self.value = value

    # getter
    @property
    def value(self):
        return self._value

    # setter
    @value.setter
    def value(self, new_value):
        self._value = new_value

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()
    
    # getter
    @property
    def value(self):
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)
    
class Email(Field):
    def __init__(self, value):
        if not self.is_valid_email(value):
            raise ValueError('Invalid email format')
        super().__init__(value)

    @staticmethod
    def is_valid_email(value):
        return fullmatch(EMAIL_REGULAR, value, flags = IGNORECASE) is not None
    
    # getter
    @property
    def value(self):
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value):
        if not self.is_valid_email(new_value):
            raise ValueError('Invalid email format')
        self._value = new_value

    def __str__(self):
        return str(self._value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    # getter
    @property
    def value(self):
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value):
        self._value = new_value

class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    # getter
    @property
    def value(self):
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value):
        self._value = new_value

class Notes:
    def __init__(self, text, author):
        self.text = text
        self.author = author

    def __str__(self):
        return f"{self.text} (by {self.author})"
    
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, author, text):
        note = Notes(text, author)
        self.notes.append(note)

    def print_notes(self):
        if self.notes:
            console = Console()
            table = Table(title="Wish list", show_header=True, header_style="bold magenta")
            table.title_align = "center"
            table.title_style = "bold yellow"
            table.add_column("Index", style="cyan", width=5, justify="center")
            table.add_column("Note", style="green")
            table.add_column("Author", style="blue")  # Додано новий стовпець для автора

            for i, note in enumerate(self.notes, start=1):
                table.add_row(str(i), note.text, note.author)

            console.print(table)
        else:
            print("No notes available.")

    def save_notes(self, filename):
        with open(filename, 'wb') as file:
            dump(self.notes, file)

    def load_notes(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.notes = load(file)
        except FileNotFoundError:
            self.notes = []

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None
        self.notes = []

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)
        
    def add_email(self, email):
        email = Email(email)
        self.email = email
            
    def edit_phone(self, old_phone=None, new_phone=None):
        # Редагування телефону
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        
        if not found:
            raise ValueError(f"Phone {old_phone} not found in the record")
    
    def edit_email(self, new_email):
        if not Email.is_valid_email(new_email):
            raise ValueError('Invalid email format')
        self.email.value = new_email

    def remove_phone(self, number):
        # Видалення телефону
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)

    def find_phone(self, number):
        # Знаходження телефону
        for phone in self.phones:
            if phone.value.lower() == number:
                return phone
        return None

    def set_birthday(self, birthday):
        # Перевірка коректності формату дати та збереження в атрибут birthday
        try:
            self.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid birthday date format. Use YYYY-MM-DD.")

    def set_address(self, address):
        self.address = Birthday(address)

    def days_to_birthday(self):
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

    def __str__(self):
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

    def add_record(self, record):
        self.data[record.name.value] = record

    def add_note(self, text):
        self.notes_manager.add_note(text)

    def print_notes(self):
        self.notes_manager.print_notes()

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        return AddressBookIterator(self, items_per_page=5)  # items_per_page - кількість записів на сторінці

    def search_contact(self):
        # пошук контактів серед контактів книги
        search_query = input("Enter search term: ")
        results, suggestions = self.search(search_query)

        if results:
            print("Search results:")
            for result in results:
                print(result)
        elif suggestions:
            print(f"Possible suggestions: {', '.join(suggestions)}")
        else:
            print(f"Contact '{search_query}' not found. Phone number, address, and email were also not found.")

    def search(self, query):
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
    def __init__(self, address_book, items_per_page):
        self.address_book = address_book
        self.items_per_page = items_per_page
        # Визначається поточна сторінка, починаючи з нуля (перша сторінка)
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Метод обчислює індекс початку (start) і кінця (end) діапазону записів, які повинні бути виведені на поточній сторінці. 
        # Наприклад, якщо items_per_page дорівнює 5, то на першій сторінці будуть виводитися записи з індексами 0 до 4, 
        # на другій сторінці - з 5 до 9, і так далі.
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        records = list(self.address_book.data.values())[start:end]

        if not records:
            raise StopIteration

        self.current_page += 1
        return records


if __name__ == "__main__":
    main()