from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not self.is_valid(value):  # Перевірка на коректність введеного значення
            raise ValueError(f"Invalid {self.__class__.__name__} format")
        self.value = value

    def is_valid(self, value):
        return True  

class Name(Field):
    ...

class Phone(Field):
    @staticmethod
    def is_valid(value):
        return len(value) == 10 and value.isdigit()  # Перевірка на коректність номера телефону

class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name: str, birthday=None) -> None:  # Клас Record приймає ще один додатковий аргумент класу Birthday
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone: int):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone: int):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
    
    def edit_phone(self, old_phone: int, new_phone: int):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                if p.is_valid(new_phone):
                    p.value = new_phone
                    found = True
                else:
                    raise ValueError("Invalid phone number format")
        if not found:
            raise ValueError(f"Phone number '{old_phone}' not found")


    def find_phone(self, phone: int):
        for p in self.phones:
            if p.value == phone:
                return p

    def days_to_birthday(self):  # Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження
        if self.birthday:
            today = datetime.now()
            birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            next_birthday = birthday.replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_remaining = (next_birthday - today).days
            return days_remaining
        return None

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            return self.data[name]

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def __iter__(self):  # AddressBook реалізує метод iterator, який повертає генератор записів AddressBook і за одну ітерацію повертає виявлення для N записів
        return AddressBookIterator(self)

class AddressBookIterator:
    def __init__(self, address_book):
        self.address_book = address_book
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.address_book.data):
            records = list(self.address_book.data.values())
            result = records[self.index]
            self.index += 1
            return result
        raise StopIteration

# Приклад використання:
book = AddressBook()
john_record = Record("John", "1990-05-15")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane", "1985-08-21")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for record in book:
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name.value}: {found_phone}")

book.delete("Jane")

for record in book:
    print(record)
