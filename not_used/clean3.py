import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Загрузка данных
df = pd.read_csv('./csv/prepared_data.csv')
texts = df['data']
labels = df['decision']

# Векторизация текста с помощью TfidfVectorizer
vectorizer = TfidfVectorizer()

# Создаем модель KMeans
kmeans = KMeans(random_state=42)

# Создаем модель RandomForestClassifier
clf = RandomForestClassifier(random_state=42)

# Создаем пайплайн
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('kmeans', kmeans),
    ('clf', clf)
])

# Параметры для поиска
param_grid = {
    # Параметры для KMeans
    'kmeans__n_clusters': [5, 10, 15, 20],  # Количество кластеров
    'kmeans__init': ['k-means++', 'random'],  # Метод инициализации
    'kmeans__max_iter': [300, 500],  # Максимальное количество итераций
    'kmeans__n_init': [10, 20],  # Количество запусков алгоритма

    # Параметры для RandomForest
    'clf__n_estimators': [100, 200, 300],  # Количество деревьев в лесу
    'clf__max_depth': [10, 50, 100, None],  # Максимальная глубина деревьев
    'clf__max_features': ['auto', 'sqrt', 'log2'],  # Количество признаков для каждого дерева
    'clf__min_samples_split': [2, 5, 10],  # Минимальное количество образцов для разделения
    'clf__min_samples_leaf': [1, 2, 4],  # Минимальное количество образцов в листе
}

# Настройка GridSearchCV для поиска лучших параметров
grid_search = GridSearchCV(pipeline, param_grid, cv=3, n_jobs=-1, verbose=1, scoring='accuracy')

# Обучение модели с поиском по сетке
grid_search.fit(texts, labels)

# Лучшие параметры
print(f"Best parameters: {grid_search.best_params_}")

# Лучшая модель после поиска по сетке
best_model = grid_search.best_estimator_

# Прогнозирование на тестовых данных
df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
new_texts = df2['data']
new_labels = df2['decision']

# Предсказания
predictions = best_model.predict(new_texts)

# Оценка модели
accuracy = accuracy_score(new_labels, predictions)
precision = precision_score(new_labels, predictions, average='micro')
recall = recall_score(new_labels, predictions, average='micro')
f1 = f1_score(new_labels, predictions, average='micro')

# Выводим результаты
print(f"Accuracy: {accuracy:.2f}")
print("Precision Score:", precision)
print("Recall Score:", recall)
print("F1 Score:", f1)
