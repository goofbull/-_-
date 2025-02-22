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
#reader = PdfReader("Дело_1.pdf")

#text = ""
#for page in reader.pages:
#    text += page.extract_text() + "\n"


#tokens = [token.text for token in tokenize(text)]
#print("Токены:", tokens)
#cleaned_text = re.sub(r'\s+', ' ', text).strip()
#print(cleaned_text)
def extract_text_from_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"  # Сохраняем переносы строк для разделения абзацев
    return text.strip()

case2 = "case_2"
case3 = "case_3"

# def CleanText(name:  str):
#     # Путь к Word файлу
#     file_path = name + ".docx"

#     # Извлекаем текст
#     text = extract_text_from_docx(file_path)
#     print("Извлеченный текст:")
#     #/print(text)

#     # Токенизация текста с помощью razdel
#     tokens = [token.text for token in tokenize(text)]
#     print("\nТокены:")
#     #/print(tokens)

#     # Токеннизированный текст целиком
#     tokenized_text = " ".join(tokens)
#     print("Токенизированный текст:")
#     #/print(tokenized_text)

#     # Разделяем текст на слова
#     words = text.split()

#     # Лемматизация слов
#     #lemmatized_words = [morph.parse(word)[0].normal_form for word in words]

#     # Выводим результат
#     #print("Лемматизированные слова:", lemmatized_words)

#     # Лемматизированный текст
#     #lemmatized_text = " ".join(lemmatized_words)
#     #print("Лемматизированный текст:", lemmatized_text)

#     # Лемматизация и удаление слов, которые являются предлогами, частицами и т.д.
#     # Пример списка стоп-слов (например, некоторые предлоги и частички)
#     stop_words_set = {"я", "ты", "он", "она", "оно", "мы", "вы", "они", "это", "тот", "та", "те", "который", "чей", "кто", "что", 
#                 "да", "нет", "а", "но", "и", "или", "да", "также", "же", "не", "ли", "бы", "для", "от", "из", "с", "на", 
#                 "в", "по", "к", "у", "о", "об", "при", "для", "за", "перед", "после", "до", "через", "между", "над", 
#                 "под", "вокруг", "без", "из-за", "около", "через", "вон", "про", "между", "если", "когда", "пока", "хотя", 
#                 "как", "так", "потому что", "чтобы", "ибо", "то есть", "где", "когда", "куда", "откуда", "уж", "вот", "вот такой", 
#                 "именно", "вот это", "тот", "всё", "вся", "все", "некоторый", "несколько", "один", "два", "три", "первый", "второй", 
#                 "последний", "каждый", "любой", "любой", "даже", "довольно", "вовсе", "только", "никогда", "всегда", "потом", "когда-то", 
#                 "везде", "впрочем", "мало", "много", "больше", "меньше", "слишком", "скорее", "уж", "как бы", "например", "например", 
#                 "возможно", "следует", "конечно", "вроде", "чем", "что-то", "тот", "этот", "такой", "никакой", "другой", "так как", 
#                 "а вот", "пусть", "либо", "просто", "типо", "короче", "хотя бы", "и так далее", "далее", "есть", "потому", "то"
#     }

#     # Лемматизация и удаление стоп-слов
#     lemmatized_and_no_stop_words = [morph.parse(word)[0].normal_form for word in words if morph.parse(word)[0].normal_form not in stop_words_set]

#     # Результат
#     #/print(lemmatized_and_no_stop_words)

#    # Определение частей речи для каждого лемматизированного слова
#     parts_of_speech = []


 
#     for word in lemmatized_and_no_stop_words:
#         # Получаем анализ для каждого слова
#         parse_result = morph.parse(word)[0]
#         # Получаем часть речи из анализа
#         part_of_speech = parse_result.tag.POS
#         parts_of_speech.append((word, part_of_speech))


#     nouns_list = []

#     # Вывод частей речи
#     print("\nЧасти речи для лемматизированных слов:")
#     for word, pos in nouns_list:
#         print(f"Слово: {word}, Часть речи: {pos}")
#         #
#         if pos != "INFN":
#             nouns_list.append(word)




#     # Создаем новый текст, исключив символы новой строки
#     clean_text = ''
#     for char in text:
#         if char != '\n':  # Если символ не является новой строкой, добавляем его
#             clean_text += char

#     print(clean_text)


#     doc = Doc(clean_text)

#     doc.segment(segmenter)
#     print(doc.sents[:2])
#     print(doc.tokens[:5])


#     doc.tag_ner(ner_tagger)
#     print(doc.spans[:5])

#     doc.ner.print()


#     print(nouns_list)
#     return nouns_list

## НЕ РАБОТАЕТ 
# vectorizer = TfidfVectorizer(stop_words=stop_words_list)

# tfidf_matrix = vectorizer.fit_transform([clean_text]) 
# feature_names = vectorizer.get_feature_names_out()
# tfidf_scores = tfidf_matrix.sum(axis=0).A1
# keywords = [(feature_names[i], tfidf_scores[i]) for i in range(len(feature_names))]
# keywords = sorted(keywords, key=lambda x: x[1], reverse=True)
# print(keywords[:15])  # 15 наиболее важных слов
def CleanText(name: str):
    # Путь к Word файлу
    file_path = name + ".docx"

    # Извлекаем текст
    text = extract_text_from_docx(file_path)
    print("Извлеченный текст:")
    # /print(text)

    # Токенизация текста с помощью razdel
    tokens = [token.text for token in tokenize(text)]
    print("\nТокены:")
    # /print(tokens)

    # Токенизированный текст целиком
    tokenized_text = " ".join(tokens)
    print("Токенизированный текст:")
    # /print(tokenized_text)

    # Разделяем текст на слова
    words = text.split()

    # Пример списка стоп-слов (предлоги, частицы и т.д.)
    stop_words_set = {"я", "ты", "он", "она", "оно", "мы", "вы", "они", "это", "тот", "та", "те", "который", "чей", "кто", "что", 
                      "да", "нет", "а", "но", "и", "или", "да", "также", "же", "не", "ли", "бы", "для", "от", "из", "с", "на", 
                      "в", "по", "к", "у", "о", "об", "при", "для", "за", "перед", "после", "до", "через", "между", "над", 
                      "под", "вокруг", "без", "из-за", "около", "через", "вон", "про", "между", "если", "когда", "пока", "хотя", 
                      "как", "так", "потому что", "чтобы", "ибо", "то есть", "где", "когда", "куда", "откуда", "уж", "вот", "вот такой", 
                      "именно", "вот это", "тот", "всё", "вся", "все", "некоторый", "несколько", "один", "два", "три", "первый", "второй", 
                      "последний", "каждый", "любой", "любой", "даже", "довольно", "вовсе", "только", "никогда", "всегда", "потом", "когда-то", 
                      "везде", "впрочем", "мало", "много", "больше", "меньше", "слишком", "скорее", "уж", "как бы", "например", "например", 
                      "возможно", "следует", "конечно", "вроде", "чем", "что-то", "тот", "этот", "такой", "никакой", "другой", "так как", 
                      "а вот", "пусть", "либо", "просто", "типо", "короче", "хотя бы", "и так далее", "далее", "есть", "потому", "то"}

    # Лемматизация и удаление стоп-слов
    lemmatized_and_no_stop_words = [morph.parse(word)[0].normal_form for word in words if morph.parse(word)[0].normal_form not in stop_words_set]

    # Список для частей речи
    parts_of_speech = []
    nouns_list = []
    loc = []
    per = []
    org = []

    for word in lemmatized_and_no_stop_words:
        # Получаем анализ для каждого слова
        parse_result = morph.parse(word)[0]
        # Получаем часть речи из анализа
        part_of_speech = parse_result.tag.POS
        
        # Применяем NER для проверки на наличие сущностей LOC, PER, ORG
        doc = Doc(word)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)

        for span in doc.spans:
            if span.type == "LOC":
                loc.append(word)
            elif span.type == "PER":
                per.append(word)
            elif span.type == "ORG":
                org.append(word)

        # Если слово является сущностью "LOC", "PER" или "ORG", пропускаем его
        if any(span.type in ["LOC", "PER", "ORG"] for span in doc.spans):
            continue  # Пропускаем это слово

        # Если не сущность, добавляем его в список частей речи
        parts_of_speech.append((word, part_of_speech))

        # Добавляем в список существительных, если это существительное
        if part_of_speech != "INFN":
            nouns_list.append(word)

    # Выводим результат
    print("\nЧасти речи для лемматизированных слов:")
    for word, pos in parts_of_speech:
        print(f"Слово: {word}, Часть речи: {pos}")

    # Создаем новый текст, исключив символы новой строки
    clean_text = ''
    for char in text:
        if char != '\n':  # Если символ не является новой строкой, добавляем его
            clean_text += char

    print("\nТекст без новых строк:")
    print(clean_text)

    # Применяем сегментацию и выводим предложения
    doc = Doc(clean_text)
    doc.segment(segmenter)
    print(doc.sents[:2])
    print(doc.tokens[:5])

    # Применяем NER и выводим сущности
    doc.tag_ner(ner_tagger)
    print("\nСущности:")
    doc.ner.print()

    print("\nСущности LOC:")
    print(loc)

    print("\nСущности PER:")
    print(per)

    print("\nСущности ORG:")
    print(org)

    # Возвращаем список существительных
    return {
        "nouns": nouns_list,
        "loc_entities": loc,
        "per_entities": per,
        "org_entities": org
    }
case2 = CleanText(case2)
case3 = CleanText(case3)

same_words =[]

for i in case2:
    for y in case3:
        if i == y:
            same_words.append(i)
print("\nОДИНАКОВЫЕ СЛОВА")
same_words = list(dict.fromkeys(same_words))
print(same_words)