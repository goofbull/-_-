from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import nltk

# Скачиваем стоп-слова
nltk.download('stopwords')
russian_stopwords = stopwords.words("russian")

# Пример текстов
texts = [
    "Это первый пример текста на русском языке.",
    "А вот и второй пример с другим содержанием.",
    "Этот текст немного отличается от остальных.",
    "Тут совершенно другой стиль написания текста.",
    "Новый текст, не похожий на предыдущие."
]

# Векторизация
vectorizer = TfidfVectorizer(max_features=1000, stop_words=russian_stopwords)
X = vectorizer.fit_transform(texts)

# Кластеризация с KMeans (например, хотим 2 кластера)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X)

# Вывод результатов
for i, text in enumerate(texts):
    print(f"Текст: {text} \n--> Кластер: {clusters[i]}\n")
