import sys
import sysconfig
import fitz
from collections import defaultdict
#print(sys.executable) # show which Python we are running
#print(sys.path) 
#print(sysconfig.get_paths()["purelib"])
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time

from natasha import (
        Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)
#service = Service("E:\geckodriver\geckodriver.exe")
#driver = webdriver.Firefox(service=service)


myfile = open("text.txt", "rt")
text = myfile.read()
myfile.close()

result = re.search(r'А\d{2,}-\d+ /\d+', text)
print(result.group())

result = re.search(r'\d{2}\s+(декабря|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября)\s+\d{4}\s+года', text)
#print(result.group())

date_string = result.group()


months = {
    "января": "01", "февраля": "02", "марта": "03", "апреля": "04", 
    "мая": "05", "июня": "06", "июля": "07", "августа": "08", 
    "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
}

date_string = date_string.replace("года", "")

# Разбиваем строку на части
day, month, year = date_string.split()
month_num = months[month]

# Собираем строку в нужном формате
formatted_date = f"{day}/{month_num}/{year}"

print(formatted_date)

#result = re.findall(r'\b[А-Яа-яЁё]+\b\s[А-Я]\.[А-Я]\.', text)
#print(result)


directory = "./pdf_cases/"
filename = "case_10.pdf"
doc = fitz.open(directory+filename)
text = "\n".join([page.get_text() for page in doc])

clean_text = ' '.join(text.split())
#print(clean_text)

#print(text)
#result = re.findall(r'\b[А-Яа-яЁё]+\b\s[А-Я]\.[А-Я]\.', text)
#print(result)


# p = 'Романовой' 
# driver.get("https://textovod.com/morph")
# search_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "text"))
# )
# search_box.send_keys(p)
# time.sleep(2)

# search_button = driver.find_element(By.XPATH, "//button[span[text()='Выполнить']]")
# search_button.click()
# time.sleep(2)

# wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.XPATH, "//h4[text()='Формы слова']")))

# forms = driver.find_elements(By.XPATH, "//h4[text()='Формы слова']/following-sibling::div//div")

# sent = []
# for form in forms:
#     print(form.text)
#     sent.append(form.text)


# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'mt-2')]")))

# text = element.text
# driver.quit()
# print(text)

# modified_text = text.replace(",", " ")
# print(modified_text)
# sp = modified_text.split()
# print(sp)

# for i in sent:
#     if "им" in i and sp[4] in i:
#         infinitiv = i.split()
#         print(infinitiv[0])
#         break
#
