from collections import UserDict
from datetime import datetime
from pickle import dump, load
from os import path

from rich.console import Console
from rich.table import Table

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


# Отримання поточного каталогу, в якому знаходиться виконуваний файл
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Створення повного шляху до файлу "address_book.pkl" в поточному каталозі
FILENAME = path.join(CURRENT_DIRECTORY, 'address_book.pkl')

def main():
    # Завантаження адресної книги або створення нової
    book = load_book(FILENAME)

    print("Hi! I am Santa's Personal Assistant - Mr.Corgi. How can I help you?")

    # Список доступних команд
    commands = ['add-contact', 'all-contacts', 'edit-contact', 'delete-contact', 'upcoming-birthdays', 'search-contact', 'exit']

    # Створення об'єкту WordCompleter, який використовується для автодоповнення команд
    completer = WordCompleter(commands, ignore_case=True)

    # Запит на введення команди від користувача з можливістю автодоповнення
    command = prompt('Write a command (help - all commands): ', completer=completer)

    # Цикл для команд в консолі 
    while command != 'exit':
        words_commands = command.split() # розділення рядка на масив слів

        if command == 'help':
            # Вивід меню команд
            print_menu_commmands()

        elif words_commands[0] == 'add-contact':
            # Додавання контакту
            while len(words_commands) < 2:
                command = input('Enter command "add-contact [name]": ')
                words_commands = command.split()
            fun_add_contact(book, words_commands[1])

        elif words_commands[0] == 'all-contacts':
            # Виведення всіх записів у книзі
            print_table(book)
        
        elif words_commands[0] == 'edit-contact':
            # Редактування контакту
            fun_edit_contact(book)

        elif words_commands[0] == 'delete-contact':
            # Видалення контакту
            fun_delete_contact(book)

        elif words_commands[0] == 'upcoming-birthdays':
            # Вивід контакту у якого через n днів день народження
            fun_upcoming_birthdays(book)

        elif words_commands[0] == 'search-contact':
            # Пошук контактів серед контактів книги;
            book.search_contact()

        else: 
            print("The command was not found. Please enter another command.")

        # Запит на введення команди від користувача з можливістю автодоповнення
        command = prompt('Write a command (help - all commands): ', completer=completer)

        # Збереження книги
        save_book(book)


def load_book(FILENAME):
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
    - add-contact [name] - add contact with it's name
    - edit-contact       - editing contact information
    - delete-contact     - deleting contact
    - all-contacts       - displays all contacts in the address book
    - upcoming-birthdays - display a list of contacts whose birthday is a specified number of days from the current date
    - exit               - enter 'exit' to exit the Assistant
    - search-contact     - search for contacts in the address book
    ''')


def fun_add_contact(address_book, name):
    record = Record(name)
    address_book.add_record(record)
    phone = input(f'Enter the phone of contact {name} (c - close): ')
    while phone != 'c':
        try:
            record.add_phone(phone)
            phone = input(f'Enter the phone of contact {name} (c - close): ')
        except ValueError:
            phone = input(f'Enter the phone (10 digits) (c - close): ')

    birthday = input(f'Enter the birthday of contact {name} (c - close): ')

    while birthday != 'c':
        try:
            record.set_birthday(birthday)
            break
        except ValueError:
            birthday = input(f'Enter the birthday (Year-month-day) (c - close): ')

    email = input(f'Enter the email adress (c - close): ')
    while email != 'c':
        try:
            record.add_email(email)
            break
        except ValueError:
            email = input('Enter a valid email format (c - close): ')

    address = input(f'Enter the address of contact {name} (c - close): ')
    if address != 'c':
        record.set_address(address)


def fun_edit_contact(address_book):
    contact_name = input('Write the name of contact in which you want to change something: ')
    if contact_name in address_book.data:
        contact_edit = address_book.data[contact_name]
        print(f'Contact found')
        while True:
            edit = input('Enter what you want to edit(phone, birthday, address, email) (c - close): ')
            if edit.lower() == 'c':
                break 
            try:
                if edit == 'phone':
                    new_phone = input("Enter new phone number: ")
                    contact_edit.edit_phone(contact_edit.phones[0].value, new_phone)
                elif edit == 'birthday':
                    new_birthday = input('Enter new birthday: ')
                    contact_edit.set_birthday(new_birthday)
                elif edit == 'address':
                    new_address = input('Enter new address: ')
                    contact_edit.set_address(new_address)
                elif edit == 'email':
                    new_email = input('Enter new email: ')
                    contact_edit.edit_email(new_email)
                else:
                    print('Ivailid comand, please enter(phone, birthday, address, email) (c - close): ')
            except ValueError:
                edit = input('Ivailid comand, please enter(phone, birthday, address, email) (c - close): ')
    else:
        print(f'Contact {contact_name} not found')


def fun_delete_contact(address_book):
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


def print_table(AddressBook):
    # Виведення у вигляді таблиці

    print('\nAddress book')

    # Перевірка на порожню книгу
    if not AddressBook.data:
        print("Книга порожня.\n")
        return 

    # Створення об'єкту Console
    console = Console()

    # Створення таблиці
    table = Table(show_header=True, header_style="bold magenta")

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
            "; ".join(str(phone.value) for phone in record.phones),
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
        print('*' * 10)
        print(f'Upcoming birthdays within the next {days_count} days:')
        for contact in upcoming_birthdays:
            print(contact)
            print('*' * 10)
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
        if not self.is_vallid_email(value):
            raise ValueError('Invalid email format')
        super().__init__(value)

    @staticmethod
    def is_vallid_email(value):
        return '@' in value
    
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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)
        
    def add_email(self, email):
        email = Email(email)
        self.email = email
        
    def edit_phone(self, old_phone, new_phone):
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
        if not Email.is_vallid_email(new_email):
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
        return contact_info


class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        return AddressBookIterator(self, items_per_page=5)  # items_per_page - кількість записів на сторінці
    
    def save_to_file(self, filename):
        # Завантаження до файлу
        with open(filename, "wb") as file:
            dump(self.data, file)

    def load_from_file(self, filename):
        # Завантаження з файлу
        with open(filename, "rb") as file:
            self.data = load(file)

    def search(self, query):
        # Пошук за кількома цифрами номера телефону або літерами імені 
        results = []
        try:
            int(query[0])
        except Exception:
            for name, record in self.data.items():
                if query.lower() in name.lower():
                    results.append(record)
        else:
            for name, record in self.data.items():
                for phone in record.phones:
                    if query.lower() in phone.value.lower():
                        results.append(record)
        finally:        
            return results
        
    # пошук контактів серед контактів книги
    def search_contact(self):
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