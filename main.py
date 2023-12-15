from collections import UserDict
from datetime import datetime
from pickle import dump
from pickle import load
from os import path

CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

FILENAME = path.join(CURRENT_DIRECTORY, 'address_book.pkl')

def main():

    # Створення нової адресної книги
    book = AddressBook()

    # Завантаження адресної книги з диска
    if path.exists(FILENAME):
        print('\nLoad contacts...')
        book.load_from_file(FILENAME)
    else:
        # Додавання записів до пустої книги
        print('\nAdd contacts...')

        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)

        # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")

        # Встановлення дати народження для John
        john_record.set_birthday("2001-08-19")

        # print(john_record)                      # Виведення: Contact name: John, phones: 1112223333; 5555555555, birthday: 2001-08-19
        # print(john_record.days_to_birthday())   # Виведення: There are 319 days left before the birthday.

        # Створення записів для інших котанктів
        kol_record = Record("Kol")
        anna_record = Record("Anna")
        lily_record = Record("Lily")

        # Додавання нових записів до адресної книги
        book.add_record(kol_record)
        book.add_record(anna_record)
        book.add_record(lily_record)

        # Додавання номерів до контактів
        kol_record.add_phone("1234567890")
        anna_record.add_phone("0667954896")
        lily_record.add_phone("0955739843")

        # Встановлення дати народження контактів
        anna_record.set_birthday("2003-02-24")
        lily_record.set_birthday("2000-10-01")


    print('\nbook')
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Пошук контактів за іменем або номером телефону
    search_query = input("\nEnter a name or phone number to search('exit' to finish): ")
    search_results = book.search(search_query)
    while search_query != 'exit': 
        if search_results:
            print("Search results:")
            for record in search_results:
                print(record)
            search_results = None
        else:
            print("No matching contacts found.")

        search_query = input("\nEnter a name or phone number to search('exit' to finish): ")
        search_results = book.search(search_query)

    # Збереження адресної книги на диск
    book.save_to_file(FILENAME)


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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу
    def add_phone(self, phone):
        # Додавання телефону
        phone = Phone(phone)
        self.phones.append(phone)
    
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
            raise ValueError("Invalid birthday date.")


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
            contact_info += f", phones: {'; '.join(phone.value for phone in self.phones)}"
        if self.birthday:
            contact_info += f", birthday: {self.birthday.strftime('%Y-%m-%d')}"
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
        if not path.exists(filename):
            return
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