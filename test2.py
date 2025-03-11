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

result = re.search(r'А\d{2}-\d+ /\d{4}', text)
print(result.group())

result = re.search(r'\d{2}\s+(декабря|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября)\s+\d{4}\s+года', text)
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

#result = re.findall(r'\b[А-Яа-яЁё]+\b\s[А-Я]\.[А-Я]\.', text)
#print(result)


directory = "./pdf_cases/"
filename = "case_1.pdf"
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

article_declensions = ["статья", "статьи", "статей", "статье", 
      "статьям", "статьями", "статью", "статьёй", 
      "статьей", "статьях"]

code_declensions = ["кодекс", "кодексы", "кодекса", "кодексов",
                    "кодексу", "кодексам", "кодексом", "кодексами",
                    "кодексе", "кодексах",]
claimant_declensions = ["истец", "истцы", "истца", "истцов",
             "истцу", "истцам", "истцом", "истцами",
             "истце", "истцах",]
defendant_declensions = ["ответчик", "ответчики", "ответчика", "ответчиков",
                         "ответчику", "ответчикам", "ответчиком", "ответчиками",
                         "ответчике", "ответчиках",]


text = text.replace('\n', '')
# Инициализация Natasha для лемматизации

text_splitted = text.split()
text_splitted_clean = []
for i in text_splitted:
    if '-' in i:
        i = i.replace('-', '')
    text_splitted_clean.append(i)
text = " ".join(text_splitted)

p = []
for i in text_splitted_clean:
    if i in claimant_declensions:
        index = text_splitted_clean.index(i)
        surname = text_splitted_clean[index+1]
        name = text_splitted_clean[index+2]
        p.append(surname + ' '+ name)
        break
    
for i in text_splitted_clean:
    if i in defendant_declensions:
        index = text_splitted_clean.index(i)
        surname = text_splitted_clean[index+1]
        name = text_splitted_clean[index+2]
        p.append(surname + ' '+ name)
        break

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

# Словарь сокращений кодексов
abbreviations = {
    "земельный": "зк", "гражданский": "гк", "трудовой": "тк", "налоговый": "нк", "кодекс об административный правонарушения": "коап", 
    "уголовный": "ук", "гражданский процессуальный": "гпк", "уголовно-процессуальный": "упк", "арбитражный процессуальный": "апк",
    "жилищный": "жк", "семейный": "ск", "бюджетный": "бк", "градостроительный": "гдк", "таможенный": "тк", 
    "кодекс административный судопроизводство": "кас", "уголовно-исполнительный": "уик", "лесной": "лк", 
    "водный": "вк", "воздушный": "вшк", "кодекс торговый мореплавание": "ктм", "кодекс внутренний водный транспорт": "кввт" 
}

# Лемматизация текста с помощью Natasha
def lemmatize_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    return " ".join(token.lemma for token in doc.tokens)

# Регулярное выражение для поиска статьи и номеров
pattern = re.compile(r"\bстатья\s+((?:\d+[,-]?\s*)+)((?:[А-Яа-я]+(?:\s+[А-Яа-я]+)*)?) кодекс российский федерация", re.IGNORECASE)

def extract_articles(text):
    article_dict = defaultdict(set)  # Используем множество для удаления дубликатов
    text = lemmatize_text(text)  # Применяем лемматизацию
    
    matches = pattern.findall(text)
    for numbers, code_type in matches:
        code_type = code_type.strip()
        article_numbers = set()
        for part in numbers.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                article_numbers.update(range(start, end + 1))
            else:
                article_numbers.add(int(part.strip()))
        # Заменяем полное название кодекса на сокращение
        if code_type in abbreviations:
            code_type = abbreviations[code_type]
        article_dict[code_type].update(article_numbers)
    
    return {key: sorted(value) for key, value in article_dict.items()}  # Преобразуем множества в отсортированные списки


result = extract_articles(text)
print(result)  # {'АПК': [110, 167, 168, 169, 170, 171, 176, 318]}

print(p)

# loc = []
# doc = Doc(text)
# doc.segment(segmenter)
# doc.tag_ner(ner_tagger)
# locs = [span.text for span in doc.spans if span.type == "LOC"]
# print(locs)
#print(text_splitted)
for word in text_splitted:
    if word == 'г.':
        ind = text_splitted.index(word)
print(text_splitted[ind+1])        