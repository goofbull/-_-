from typing import Tuple, Optional

import fitz
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
from nltk import tokenize
import re
from collections import defaultdict
from important_features import CleanText
import pymorphy3


segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
morph = pymorphy3.MorphAnalyzer()

# Словарь сокращений кодексов
abbreviations = {
    "земельный": "зк", "гражданский": "гк", "трудовой": "тк", "налоговый": "нк", "кодекс об административный правонарушения": "коап", 
    "уголовный": "ук", "гражданский процессуальный": "гпк", "уголовно-процессуальный": "упк", "арбитражный процессуальный": "апк",
    "жилищный": "жк", "семейный": "ск", "бюджетный": "бк", "градостроительный": "гдк", "таможенный": "тк", 
    "кодекс административный судопроизводство": "кас", "уголовно-исполнительный": "уик", "лесной": "лк", 
    "водный": "вк", "воздушный": "вшк", "кодекс торговый мореплавание": "ктм", "кодекс внутренний водный транспорт": "кввт" 
}

def lemmatize_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    return " ".join(token.lemma for token in doc.tokens)

def extract_articles(text, article_pattern):
    article_dict = defaultdict(set)
    text = lemmatize_text(text)
    
    matches = article_pattern.findall(text)
    for numbers, code_type in matches:
        code_type = code_type.strip()
        article_numbers = set()
        for part in numbers.split(','):
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    article_numbers.update(range(start, end + 1))
                except ValueError:
                    continue
            else:
                found_numbers = re.findall(r'\d+', part)
                for num in found_numbers:
                    try:
                        article_numbers.add(int(num))
                    except ValueError:
                        continue

        if code_type in abbreviations:
            code_type = abbreviations[code_type]
        article_dict[code_type].update(article_numbers)
    
    return {key: sorted(value) for key, value in article_dict.items()}


def ustanovil(ust: str, text: str, resh: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    # Разделяем текст по ust
    parts = text.split(ust, 1)
    if len(parts) != 2:
        return None, None, None

    before_ustanovil = parts[0].strip()
    after_ustanovil = parts[1]

    # Далее разделяем оставшийся текст по resh
    parts2 = after_ustanovil.split(resh, 1)
    if len(parts2) != 2:
        return None, None, None

    before_reshil = parts2[0].strip()
    reshil = before_reshil[-1000:]

    # Анализируем before_ustanovil
    doc = Doc(before_ustanovil[-700:])
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)

    orgs = [span for span in doc.spans if span.type == "ORG"]
    orgs = [span for span in orgs if span.text not in ("Арбитражный суд", "АРБИТРАЖНЫЙ СУД")]

    persons = [span for span in doc.spans if span.type == "PER"]

    first_org = min(orgs, key=lambda x: x.start) if orgs else None
    first_person = min(persons, key=lambda x: x.start) if persons else None

    if first_org and first_person:
        if first_org.start < first_person.start:
            return first_org.text, first_person.text, reshil
        else:
            return first_person.text, first_org.text, reshil
    elif len(orgs) >= 2:
        return orgs[0].text, orgs[1].text, reshil
    elif len(persons) >= 2:
        return persons[0].text, persons[1].text, reshil
    elif len(orgs) == 1 and len(persons) == 1:
        return orgs[0].text, persons[0].text, reshil
    elif len(orgs) == 1:
        return orgs[0].text, "Не найдено", reshil
    elif len(persons) == 1:
        return persons[0].text, "Не найдено", reshil
    else:
        return "Не найдено", "Не найдено", reshil


# Лишние слова для последующего удаления
dl = ["край", "края", "область", "области", "район", "района", "России", "РФ", "Российской Федерации"]

# Формы слов для последующего поиска с помощью регулярного выражения
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
                         "ответчике", "ответчиках"]

months = {
    "января": "01", "февраля": "02", "марта": "03", "апреля": "04", 
    "мая": "05", "июня": "06", "июля": "07", "августа": "08", 
    "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
}

def get_data_from_file(directory: str, active_file_number: str):

    list_with_data = []

    index = active_file_number
    #print("Индекс файла: ", index)

    list_with_data.append(index)

    filename = "case_" + str(active_file_number) + ".pdf"
    doc = fitz.open(directory+filename)
    text = "\n".join([page.get_text() for page in doc])
    text = text.replace('Дело', '')
    clean_text = ' '.join(text.split())

    #print("Текст дела: ", clean_text)
    list_with_data.append(clean_text)


    clean_ver_text, judge = CleanText(directory, filename)

    #print("ОЧИЩЕННЫЙ ТЕКСТ: ")
    #print(clean_ver_text)

    #print("Судья: ", judge)
    list_with_data.append(clean_ver_text)
    list_with_data.append(judge)

    t2 = tokenize.sent_tokenize(clean_text)

    ###########################################################
    # Поиск номера дела по регулярному выражению
    case_number = re.search(r'А\d{2,}-\d+ /\d+', clean_text)
    if case_number == None:
        case_number = re.search(r'А\d{2,}-\d+/\d+', clean_text)
    #print("Номер судебного дела: ", case_number.group())

    list_with_data.append(case_number.group())

    pattern1 = r'\d{2}\s+(декабря|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября)\s+\d{4}\s+года'

    # Паттерн для поиска даты в формате "дд.мм.гггг"
    pattern2 = r'(\d{2})\.(\d{2})\.(\d{4})'

    # Паттерн для поиска даты в формате «день месяц год г.» (в кавычках)
    pattern3 = r'«(\d{2})»\s+(декабря|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября)\s+(\d{4})г\.'

    result1 = re.search(pattern1, text)
    result2 = re.search(pattern2, text)
    result3 = re.search(pattern3, text)

    formatted_date = None

    if result1:
        date_string = result1.group().replace("года", "").strip()
        day, month, year = date_string.split()

        month_num = months[month]
        formatted_date = f"{day}/{month_num}/{year}"

    elif result2:
        formatted_date = re.sub(pattern2, r'\1/\2/\3', result2.group())

    elif result3:
        day = result3.group(1)
        month = result3.group(2)
        year = result3.group(3)
        month_num = months[month]
        formatted_date = f"{day}/{month_num}/{year}"

    if formatted_date and len(formatted_date) > 50:
        formatted_date = 0
    
    #print("Дата: ", formatted_date)
    list_with_data.append(formatted_date)


    # Регулярное выражение для поиска статей
    article_pattern = re.compile(r"\bстатья\s+((?:\d+[,-]?\s*)+)((?:[А-Яа-я]+(?:\s+[А-Яа-я]+)*)?) кодекс российский федерация", re.IGNORECASE)
    articles = extract_articles(clean_text, article_pattern)

    list_with_data.append(articles)

    # Разбиение текста на слова
    text_splitted = text.split()

    number_or_words_in_text = len(text_splitted)

    list_with_data.append(number_or_words_in_text)

    text_splitted_clean = []
    for i in text_splitted:
        if '-' in i:
            i = i.replace('-', '')
        text_splitted_clean.append(i)
    text = " ".join(text_splitted)

    pattern = r"обоснованность заявления\s+(\w+)"

    text = text.replace('установил:', 'stop_point')
    text = text.replace('у с т а н о в и л:', 'stop_point')
    text = text.replace('УСТАНОВИЛ:', 'stop_point')
    text = text.replace('У С Т А Н О В И Л:', 'stop_point')
    text = text.replace('У с т а н о в и л:', 'stop_point')
    text = text.replace('Установил:', 'stop_point')

    text = text.replace('Р Е Ш И Л', 'start_point')
    text = text.replace('р е ш и л', 'start_point')
    text = text.replace('РЕШИЛ', 'start_point')
    text = text.replace('решил', 'start_point')
    text = text.replace('Решил', 'start_point')
    text = text.replace('Р е ш и л', 'start_point')


    t3 = tokenize.word_tokenize(text)

    claimant = ''
    defendant = ''
    reshil = ''

    claimant_found = False

    for t in t3:
            if t == "stop_point":
                claimant, defendant, reshil = ustanovil(t, text, 'start_point')
                if defendant == 'Не найдено' and claimant != 'Не найдено':
                    defendant = 'Суд'
                    list_with_data.append(claimant)
                    list_with_data.append(defendant)
                    reshil = reshil.replace('start_point', "")
                    reshil = reshil.replace('stop_point', "")
                    list_with_data.append(reshil)
                    claimant_found = True
                    break
                elif defendant == 'Не найдено' and claimant == 'Не найдено':
                    list_with_data.append(0)
                    list_with_data.append(0)
                    reshil = reshil.replace('start_point', "")
                    reshil = reshil.replace('stop_point', "")
                    list_with_data.append(reshil)
                    claimant_found = True
                    break
                else:
                    list_with_data.append(claimant)
                    list_with_data.append(defendant)
                    reshil = reshil.replace('start_point', "")
                    reshil = reshil.replace('stop_point', "")
                    list_with_data.append(reshil)
                    claimant_found = True
                    break

    if not claimant_found:
        list_with_data.append(0)
        list_with_data.append(0)
        list_with_data.append(reshil)
    loc = ''
    for i in t3:
        if i == "г.":
            y = t3.index('г.')
            loc = t3[y +1]
            list_with_data.append(loc)
            break
        elif "г." in i:
            i = i.replace('г.', '')
            loc = i
            list_with_data.append(loc)
            break

    if loc == '':
        list_with_data.append(0)

    decision = ''
    doc = ''
    match = re.search(pattern, text)
    if match:
        filtered_loc = match.group(1)
        #decision = "в пользу истца"
        decision = "принято"
        list_with_data.append(decision)
    else:
        if 'start_point' in text:
            if "частично" in text:
                decision = "частично"
                list_with_data.append(decision)
            elif "отказать" in text or "оставить без" in text:
                decision = "отказано"
                list_with_data.append(decision)
            elif "удовлетворении" in text or "признать обоснованным" in text or "удовлетворить" in text:
                decision = "принято"
                list_with_data.append(decision)
            elif "в пользу":
                parts = text.split("в пользу", 1)
                if len(parts) > 1:
                    t2 = parts[1].strip()
                    doc = Doc(t2)
                    doc.segment(segmenter)
                    doc.tag_ner(ner_tagger)
                    orgs = [span.text for span in doc.spans if span.type == "ORG"]
                    persons = [span.text for span in doc.spans if span.type == "PER"]
                    #print("ФАЙЛ ", active_file_number)
                    if orgs or persons:
                        if orgs!= [] and defendant == orgs[0]:
                            #decision = "в пользу ответчика"
                            decision = "отказано"
                            list_with_data.append(decision)
                        elif orgs!= [] and claimant == orgs[0]:
                            #decision = "в пользу истца"
                            decision = "принято"
                            list_with_data.append(decision)
                        elif persons != [] and claimant == persons[0]:
                            #decision = "в пользу истца"
                            decision = "принято"
                            list_with_data.append(decision)
                        else:
                            #decision = "в пользу ответчика"
                            decision = "отказано"
                            list_with_data.append(decision)
            else:
                list_with_data.append(0)
    return list_with_data

dict = {}

def get_dict_with_data(directory: str, number_of_docs: int):
    for i in range (1, number_of_docs + 1):

        active_file_number = str(i)
        list_with_data = get_data_from_file(directory, active_file_number)
        print("ФАЙЛ " + active_file_number + " ОБРАБОТАН")
        dict[active_file_number] = list_with_data
    return dict