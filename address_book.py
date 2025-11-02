"""
Модуль для роботи з адресною книгою.

Містить класи:
- Field — базовий клас для полів запису.
- Name — клас для зберігання імені контакту.
- Phone — клас для зберігання номера телефону з перевіркою валідності (10 цифр).
- Record — клас, який представляє окремий контакт (ім’я + список телефонів).
- AddressBook — клас для зберігання та управління записами (успадковує UserDict).

Основна функціональність:
- Додавання, пошук і видалення записів у книзі контактів.
- Додавання, редагування, пошук і видалення телефонів у межах одного запису.
- Валідація телефонних номерів при створенні.
"""

# Імпорт базових класів і типів
from collections import UserDict   # Дозволяє створювати власний словник (використовується для AddressBook)
from typing import List, Optional   # Для типізації списків і можливих None-значень (анотації типів)


# Базовий клас для всіх полів (наприклад, Name, Phone)
class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value  # Зберігає значення поля

    def __str__(self) -> str:
        return str(self.value)  # Повертає рядкове представлення значення


# Клас для зберігання імені контакту
class Name(Field):
    pass


# Клас для зберігання номера телефону з перевіркою валідності
class Phone(Field):
    def __init__(self, value: str) -> None:
        # Перевіряємо, що номер складається лише з 10 цифр
        if value.isdigit() and len(value) == 10:
            self.value: str = value
        else:
            raise ValueError("Invalid phone number")


# Клас, який представляє один запис (контакт)
class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)        # Ім’я контакту
        self.phones: List[Phone] = []       # Список телефонів (об’єкти Phone)

    # Додає новий телефон у запис
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    # Редагує існуючий номер телефону
    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        if self.find_phone(old_phone) is None:
            return False
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
        return True

    # Шукає номер телефону серед збережених
    def find_phone(self, phone: str) -> Optional[str]:
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    # Видаляє номер телефону
    def remove_phone(self, phone: str) -> Optional[bool]:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return None

    # Текстове представлення запису
    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


# Клас адресної книги, що містить усі записи
class AddressBook(UserDict):
    # Додає запис (ключ — ім’я, значення — Record)
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    # Шукає запис за ім’ям
    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    # Видаляє запис за ім’ям
    def delete(self, name: str) -> bool:
        if name in self.data:
            self.data.pop(name)
            return True
        return False

# Створення нової адресної книги
book = AddressBook()

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

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
