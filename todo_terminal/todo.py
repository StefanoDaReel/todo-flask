import requests

from .handlers import request_exc_handler
from .menu import MenuEnum


class ToDo:
    def __init__(self):
        self.menu = {
            MenuEnum.LIST_ALL: "Wyświetl wszystkie notatki.",
            MenuEnum.ADD: "Dodaj notatkę.",
            MenuEnum.DELETE: "Usuń notatkę.",
            MenuEnum.UPDATE: "Edytuj notatkę.",
            }

        self.interrupt_option = len(self.menu) + 1

        self.tasks = {
            MenuEnum.LIST_ALL: self.__print_all,
            MenuEnum.ADD: self.__add_note,
            MenuEnum.DELETE: self.__delete_note,
            MenuEnum.UPDATE: self.__update_note,
            self.interrupt_option: self.__task_exit,
        }

        self.is_running = True

        self.timeout = 30

        self.notes = None

        request_exc_handler(self.__update_notes)

    def run(self):
        if not self.notes:
            return

        while self.is_running:
            self.__print_menu()

            choice = self.__get_task()
            task = self.tasks.get(choice, self.__unavailable)

            request_exc_handler(task)

    def __print_menu(self):
        print("".join((23*"-", "MENU", 23*"-")))

        for option, task in self.menu.items():
            print(f"{option}. {task}")
        print(f"{self.interrupt_option}. Wyjdź.")

        print(50*"-")

    def __print_all(self):
        if not self.notes:
            print("Brak notatek.")

        for number, note in enumerate(self.notes, start=1):
            note_number = note.setdefault('number', number)
            output = (
                    f"{note_number}. {note['title']}\n"
                    f"      {note['content']}"
                )
            print(output)

    def __update_notes(self):
        r = requests.get('http://127.0.0.1:5000/todo-api/notes', timeout=self.timeout)
        self.notes = r.json()

    def __add_note(self):
        title = input("Wpisz tytuł notatki:\n")
        content = input("Wpisz treść notatki:\n")

        data = {
            'title': title,
            'content': content,
        }

        requests.post('http://127.0.0.1:5000/todo-api/notes', json=data, timeout=self.timeout)

        self.__update_notes()

    def __delete_note(self):
        print("Wybierz notatkę do usunięcia")
        self.__print_all()

        number = self.__get_task("Numer: ")
        to_delete = self.__get_note_id(number)

        if not to_delete:
            return

        requests.delete(f'http://127.0.0.1:5000/todo-api/notes/{to_delete}', timeout=self.timeout)

        self.__update_notes()

    def __update_note(self):
        print("Wybierz notatkę do edycji")
        self.__print_all()

        number = self.__get_task("Numer: ")
        to_update = self.__get_note_id(number)

        if not to_update:
            return

        title = input("Wpisz nowy tytuł notatki, zostaw puste pole, by ominąć:\n")
        content = input("Wpisz treść notatki, zostaw puste pole, by ominąć:\n")

        data = {
            'title': title,
            'content': content,
        }

        requests.put(f'http://127.0.0.1:5000/todo-api/notes/{to_update}', json=data, timeout=self.timeout)

        self.__update_notes()

    def __get_note_id(self, number):
        if isinstance(number, int) and number <= len(self.notes):
            return self.notes[number-1].get('id')

    def __get_task(self, message=''):
        choice = input(message)
        try:
            return int(choice)
        except ValueError:
            return choice

    def __task_exit(self):
        self.is_running = False

    def __unavailable(self):
        return
