from pypdf import PdfReader
import nltk
import razdel
from razdel import tokenize
import re
from docx import Document
import pymorphy3

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

# Путь к Word файлу
file_path = "output.docx"

# Извлекаем текст
text = extract_text_from_docx(file_path)
print("Извлеченный текст:")
print(text)

# Токенизация текста с помощью razdel
tokens = [token.text for token in tokenize(text)]
print("\nТокены:")
print(tokens)

# Токеннизированный текст целиком
tokenized_text = " ".join(tokens)
print("Токенизированный текст:")
print(tokenized_text)

# Разделяем текст на слова
words = text.split()

# Лемматизация слов
lemmatized_words = [morph.parse(word)[0].normal_form for word in words]

# Выводим результат
print("Лемматизированные слова:", lemmatized_words)

# Лемматизированный текст
#lemmatized_text = " ".join(lemmatized_words)
#print("Лемматизированный текст:", lemmatized_text)

# Пример: определение части речи
parsed_word = morph.parse(word)[0]
print(f'Часть речи для "{word}": {parsed_word.tag.POS}')

