import os
from docx import Document
from multi_rake import Rake
import pycld2
import pyrsistent
import pycld2 as cld2
#from rake_nltk import Rake
import nltk
#nltk.download('punkt_tab')

def extract_text_from_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"  # Сохраняем переносы строк для разделения абзацев
    return text.strip()

directory = "./docx_cases/"

def GetFullTextFromDocx(file_number: int):
    filename = "case_" + str(file_number) + ".docx"
    file_path = os.path.join(directory, filename)

    # Извлекаем текст
    text = extract_text_from_docx(file_path)
    text = text.replace('\n', '')
    return {
        text
    }

full_text = GetFullTextFromDocx(1)
text_ru = str(full_text)
#print(full_text)

# !!! rake работает некорректно
#rake = Rake(language='russian')

text = str(full_text)
rake = Rake()

keywords = rake.apply(text_ru)

print(keywords[:100])
#rake.extract_keywords_from_text(text)

# Получение отсортированных по значимости фраз
#keywords = rake.get_ranked_phrases()

# Вывод ключевых фраз
#print("Ключевые фразы:", keywords)
