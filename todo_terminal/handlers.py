import requests


def request_exc_handler(func):
    try:
        func()
    except requests.ConnectionError:
        print("Błąd połączenia.")
    except requests.Timeout:
        print("Przekroczono czas oczekiwania.")
    except requests.RequestException:
        print("Błąd.")
