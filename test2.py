import sys
import sysconfig

print(sys.executable) # show which Python we are running
print(sys.path) 
print(sysconfig.get_paths()["purelib"])
import re



line = 'Владимир                                                                               Дело №  А11-9330 /2021 28 января  2022 года '

result = re.search(r'А\d{2}-\d+ /\d{4}', line)
print(result.group())

result = re.search(r'\d{2}\s+(декабря|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября)\s+\d{4}\s+года', line)
print(result.group())

date_string = result.group()

# Словарь для перевода русского месяца в числовое значение
months = {
    "января": "01", "февраля": "02", "марта": "03", "апреля": "04", 
    "мая": "05", "июня": "06", "июля": "07", "августа": "08", 
    "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
}

date_string = date_string.replace("года", "")

# Разбиваем строку на части
day, month, year = date_string.split()

# Переводим месяц в числовой формат
month_num = months[month]

# Собираем строку в нужном формате
formatted_date = f"{day}/{month_num}/{year}"

print(formatted_date)