import fitz
from nltk import tokenize
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
import re

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

directory = "./pdf_cases/"




number_of_docs = 100

for i in range (1, number_of_docs + 1):
    active_file_number = str(i)

    filename = "case_" + active_file_number + ".pdf"
    doc = fitz.open(directory+filename)
    text = "\n".join([page.get_text() for page in doc])


    clean_text = ' '.join(text.split())
    t2 = tokenize.sent_tokenize(clean_text)
    org = []
    per = []
    for text in t2:
  

        pattern_fio = r"(?i)привлечь(?:\s+\w+)*\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+к"

        # Поиск ФИО в тексте
        match_fio = re.search(pattern_fio, text, re.IGNORECASE)
        full_name = " ".join(match_fio.groups()) if match_fio else None

        # Анализ текста с Natasha
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)

        # Ищем организации (ORG)
        orgs = [span.text for span in doc.spans if span.type == "ORG"]
        persons = [span.text for span in doc.spans if span.type == "PER"]

        # Определяем границы нужного отрезка
        start = text.lower().find("привлечь")
        end = text.lower().rfind("к")

        # Проверяем, есть ли организация или ФИО в нужном диапазоне
        found_orgs = []
        found_fio = []
        if start != -1 and end != -1:
            text_between = text[start:end]  # Извлекаем текст между "привлечь" и "к"
            found_orgs = [org for org in orgs if org in text_between]  # Оставляем только организации из нужного диапазона
            found_fio = [per for per in persons if per in text_between]

        # Вывод результата (либо ФИО, либо организация)
        if full_name:

            print(active_file_number)
            print("Найдено ФИО:", full_name)
        elif found_orgs:
            print(active_file_number)
            print("Найдена организация:", found_orgs[0])  # Берем первую найденную организацию
        elif found_fio:
            print(active_file_number)
            print("Найдено ФИО:", found_fio[0])
        else:
            continue


