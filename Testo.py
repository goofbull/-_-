# from ruslingua import RusLingua
# from untitled import lemmatized_and_no_stop_words
# from untitled import extract_text_from_docx
import logging
import time



# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

# ruslingua = RusLingua()
# key_words = []

# # Путь к Word файлу
# file_path = "output_terminology.docx"


# 
# # Извлекаем текст
# terminology_list = extract_text_from_docx(file_path)
# logging.debug(f"Терминология: {terminology_list}")



# for word in lemmatized_and_no_stop_words:
#     start_time = time.time()
#     logging.debug(f"Обрабатываем слово: {word}")

#     # Однокоренные слова
#     cognates = ruslingua.get_cognate_words(''+str(word)+'')
#     time.sleep(2)
#     logging.debug(f"Однокоренные слова для {word}: {cognates}")

#     if cognates == []:
#         logging.info("Нет однокоренных слов, проверяем по списку терминов...")
#         for y in terminology_list:
#             if word == y:
#                 logging.info(f"Найдено совпадение: {word}")
#                 key_words.append(word)
#     else:
#         for i in cognates:
#             for y in terminology_list:
#                 if i == y:
#                     logging.info(f"Найдено совпадение: {i}")
#                     key_words.append(i)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Время выполнения операции: {execution_time:.4f} секунд")
# print(lemmatized_and_no_stop_words)
# for i in lemmatized_and_no_stop_words:
#     if i == "банктрот":
#         print("yes")


import re
import pymorphy3
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
import os
import fitz


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()



def remove_strings_with_english(text_list):
    # Регулярное выражение для поиска английских букв
    return [text for text in text_list if not re.search(r'[a-zA-Z]', text)]

def remove_non_russian_alpha_lines(lines):
    return [line for line in lines if re.match("^[А-яёЁ]+$", line)]

def remove_lines_with_multiple_spaces(lines):
    return [line for line in lines if not re.search(r"\s{2,}", line)]


# Пример списка стоп-слов
stop_words_set = {"я", "ты", "он", "она", "оно", "мы", "вы", "они", "не", "нет", "того" "это", "тот", "та", "те", "который", "чей", "кто", "что", 
                      "да", "а", "но", "и", "или", "да", "также", "же", "ли", "бы", "для", "от", "из", "с", "на", 
                      "в", "по", "к", "у", "о", "об", "при", "для", "за", "перед", "после", "до", "через", "между", "над", 
                      "под", "вокруг", "из-за", "около", "через", "вон", "про", "между", "если", "когда", "пока", "хотя", 
                      "как", "так", "потому что", "чтобы", "ибо", "то есть", "где", "когда", "куда", "откуда", "уж", "вот", "вот такой", 
                      "именно", "вот это", "тот", "всё", "вся", "все", "некоторый", "несколько", "один", "два", "три", "первый", "второй", 
                      "последний", "каждый", "любой", "любой", "даже", "довольно", "вовсе", "только", "никогда", "всегда", "потом", "когда-то", 
                      "везде", "впрочем", "мало", "много", "больше", "меньше", "слишком", "скорее", "уж", "как бы", "например", "например", 
                      "возможно", "следует", "конечно", "вроде", "чем", "что-то", "тот", "этот", "такой", "никакой", "другой", "так как", 
                      "а вот", "пусть", "либо", "просто", "типо", "короче", "хотя бы", "и так далее", "далее", "есть", "потому", "то", "поскольку", "б"}


def CleanText(directory: str, filename: str):
    start_time = time.time()
    logging.info("Загрузка файла...")
    doc = fitz.open(directory+filename)
    text = "\n".join([page.get_text() for page in doc])

    text = text.replace('\n', '')
    text = text.replace('Р Е Ш Е Н И Е', '')
    text = text.replace('Р Е Ш И Л', '')
    words = text.split()

    # Лемматизация и удаление стоп-слов
    lemmatized_and_no_stop_words = [morph.parse(word)[0].normal_form for word in words if morph.parse(word)[0].normal_form not in stop_words_set]

    nouns = []
    loc = []
    per = []
    org = []

    # Создаем документ для NER из всего текста
    doc = Doc(text)
    doc.segment(segmenter)
    #print("Токенизация текста для NER завершена.")
    
    # Добавляем NER-теги
    doc.tag_ner(ner_tagger)
    #print("NER теги добавлены.")

    # Проверяем, какие сущности найдены
    for span in doc.spans:
        if span.type == "LOC":
            loc.append(span.text)  # Добавляем все сущности LOC
        elif span.type == "PER":
            per.append(span.text)  # Добавляем все сущности PER
        elif span.type == "ORG":
            org.append(span.text)  # Добавляем все сущности ORG


    # Добавляем все слова, которые не относятся к INFN, LOC, ORG, PER в nouns_list
    for word in lemmatized_and_no_stop_words:
        # Проверяем тип части речи с помощью pymorphy2
        parsed_word = morph.parse(word)[0]
        if parsed_word.tag.POS not in ['INFN']:
            # Не добавляем части речи: предлог, союз, частица, междометие
            if parsed_word.tag.POS != 'NPRO' and not any(word in entity_list for entity_list in [loc, per, org]):
                # Исключаем местоимения и сущности LOC, PER, ORG
                nouns.append(word) 

    nouns = [str for str in nouns if len(str) > 1]

    nouns = remove_strings_with_english(nouns)
    nouns = remove_non_russian_alpha_lines(nouns)
    per = remove_lines_with_multiple_spaces(per)

    # Отображаем результаты
    #print("\nСущности LOC:")
    #print(loc)

    #print("\nСущности PER:")
    #print(per)

    #print("\nСущности ORG:")
    #print(org)

    #print("\nNouns List:")
    #print(nouns)

    a = []
    a.extend(loc)
    a.extend(per)
    a.extend(org)
    a.extend(nouns)

    #print("\nОЧИЩЕННЫЙ ТЕКСТ: ")
    clean_text = " ".join(a)
    #print(clean_text)
    end_time = time.time()
    
    execution_time = end_time - start_time
    logging.info("Извлечение данных завершено")
    logging.info(f"Время выполнения операции: {execution_time:.4f} секунд")
    return clean_text, per[-1]