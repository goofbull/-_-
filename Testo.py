# from ruslingua import RusLingua
# from untitled import lemmatized_and_no_stop_words
# from untitled import extract_text_from_docx
# import logging
# import time


# start_time = time.time()
# # Настройка логирования
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ruslingua = RusLingua()
# key_words = []

# # Путь к Word файлу
# file_path = "output_terminology.docx"


# logging.info("Загрузка файла...")
# # Извлекаем текст
# terminology_list = extract_text_from_docx(file_path)
# logging.debug(f"Терминология: {terminology_list}")

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Время выполнения операции: {execution_time:.4f} секунд")

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

# print(key_words)
from pypdf import PdfReader
import nltk
import razdel
from razdel import tokenize
import re
from docx import Document
import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer
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

def extract_text_from_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"  # Сохраняем переносы строк для разделения абзацев
    return text.strip()

directory = "./docx_cases/"


def CleanText(file_number: int):
    # Путь к Word файлу
    filename = "case_" + str(file_number) + ".docx"
    file_path = os.path.join(directory, filename)

    # Извлекаем текст
    text = extract_text_from_docx(file_path)

    # print(text)

    #tokens = [token.text for token in tokenize(text)]

    text = text.replace('\n', '')
    text = text.replace('Р Е Ш Е Н И Е', '')
    text = text.replace('Р Е Ш И Л', '')
    print("Извлеченный текст:")
    print(text)
    # Разделяем текст на слова
    words = text.split()

    print("\nРАЗДЕЛЕННЫЙ ТЕКСТ")
    print(words)

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

    # Лемматизация и удаление стоп-слов
    lemmatized_and_no_stop_words = [morph.parse(word)[0].normal_form for word in words if morph.parse(word)[0].normal_form not in stop_words_set]

    # Список для частей речи
    parts_of_speech = []
    nouns_list = []
    loc = []
    per = []
    org = []

    # Создаем документ для NER из всего текста
    doc = Doc(text)
    doc.segment(segmenter)
    print("Токенизация текста для NER завершена.")
    
    # Добавляем NER-теги
    doc.tag_ner(ner_tagger)
    print("NER теги добавлены.")

    # Проверяем, какие сущности найдены
    for span in doc.spans:
        print(f"Сущность: {span.text}, Тип: {span.type}")
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
                nouns_list.append(word)

    # Отображаем результаты
    print("\nСущности LOC:")
    print(loc)

    print("\nСущности PER:")
    print(per)

    print("\nСущности ORG:")
    print(org)

    print("\nNouns List:")
    print(nouns_list)

    
    # Итерация через копию списка, чтобы избежать проблем с удалением элементов
    for word in nouns_list[:]:  # Создаем копию списка для безопасной итерации
        parsed_word = morph.parse(word)[0]
        #print(parsed_word.tag.POS)

        # Если часть речи None, удаляем слово из списка
        if parsed_word.tag.POS is None and word in nouns_list:
            nouns_list.remove(word)
        
        # Если слово - это целое число, удаляем его
        if isinstance(word, int) and word in nouns_list:
            nouns_list.remove(word)
        
        # Если слово содержит "http", удаляем его
        if "http" in word and word in nouns_list:
            nouns_list.remove(word)
        
        # Если слово - "-", удаляем его
        if word == "-" and word in nouns_list:
            try:
                nouns_list.remove(word)
            except ValueError:
                pass  # Игнорируем ошибку, если слово не найдено в списке


    nouns_list_clear = [re.sub(r'\d+', '', i) for i in nouns_list] 
    #print("\nТокены:")
    #print(tokens)
    # Возвращаем результаты
    return {
        "nouns": nouns_list_clear,
        "loc_entities": loc,
        "per_entities": per,
        "org_entities": org
    }



case2_result = CleanText(2)
case3_result = CleanText(1)


# Сравнение слов
same_words = list(set(case2_result['nouns']).intersection(set(case3_result['nouns'])))
print("\nОДИНАКОВЫЕ СЛОВА:")
print(same_words)
