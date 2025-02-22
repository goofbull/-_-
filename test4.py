from rake_nltk import Rake
import nltk
nltk.download('punkt_tab')
# Инициализируем Rake с русским языком
rake = Rake(language='russian')

# Пример текста на русском языке
text = """
Python — это язык программирования, который используется для создания различных приложений. Он популярен в науке, анализе данных и веб-разработке.
"""

# Извлечение ключевых фраз
rake.extract_keywords_from_text(text)

# Получение отсортированных по значимости фраз
keywords = rake.get_ranked_phrases()

# Вывод ключевых фраз
print("Ключевые фразы:", keywords)
