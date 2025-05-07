import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Загрузка данных
df = pd.read_csv('./csv/prepared_data.csv')
texts = df['data']
labels = df['decision']

# Векторизация текста с помощью TfidfVectorizer
vectorizer = TfidfVectorizer()

# Создаем модель RandomForestClassifier
clf = RandomForestClassifier(random_state=42)

# Создаем пайплайн
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('clf', clf)
])

# Определяем параметры для RandomForest
param_grid = {
    'clf__n_estimators': [50, 100, 200],
    'clf__max_depth': [None, 10, 20, 50, 100],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 4],
    'clf__max_features': ['auto', 'sqrt', 'log2'],
    'clf__bootstrap': [True, False],
    'clf__class_weight': ['balanced', None]
}

# Создаем GridSearchCV с 5-кратной кросс-валидацией
grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')

# Запуск поиска лучших параметров
grid_search.fit(texts, labels)

# Вывод лучших параметров
print("Лучшие параметры:", grid_search.best_params_)

# Выводим результат по лучшей модели
best_model = grid_search.best_estimator_

# Для тестирования модели
df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
X_new_df = df2['data']
y_new_df = df2['decision']

# Прогнозирование
predictions = best_model.predict(X_new_df)

# Метрики
accuracy = accuracy_score(y_new_df, predictions)
print(f"Accuracy: {accuracy:.2f}")
print("Precision Score : ", precision_score(y_new_df, predictions, average='micro'))
print("Recall Score : ", recall_score(y_new_df, predictions, average='micro'))
print("F1 Score : ", f1_score(y_new_df, predictions, average='micro'))
