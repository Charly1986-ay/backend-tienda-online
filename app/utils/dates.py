from datetime import datetime as dt

def getCurrentDateTime() -> str:
    # dt.now() se ejecuta cada vez que llamas a la función
    return dt.now().strftime('%d/%m/%Y %H:%M:%S')

def getCurrentDate() -> str:
    return dt.now().strftime('%d/%m/%Y')