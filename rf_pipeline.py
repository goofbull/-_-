import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import RandomOverSampler

# Загрузка обучающих данных
df = pd.read_csv('./csv/prepared_data.csv')
texts = df['data']
labels = df['decision'].tolist()

# Пайплайн: TF-IDF → Oversampling → RandomForest
pipeline = ImbPipeline([
    ('tfidf', TfidfVectorizer()),
    ('oversample', RandomOverSampler(random_state=42)),
    ('clf', RandomForestClassifier(
        n_estimators=100,
        bootstrap=True,
        class_weight='balanced',
        max_features=6,
        max_depth=100,
        random_state=42
    ))
])

# Обучение модели
pipeline.fit(texts, labels)

# Загрузка тестовых данных
df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
new_texts = df2['data']
new_labels = df2['decision']

# Предсказания
predictions = pipeline.predict(new_texts)

# Метрики
accuracy = accuracy_score(new_labels, predictions)
precision = precision_score(new_labels, predictions, average='weighted')
recall = recall_score(new_labels, predictions, average='weighted')
f1 = f1_score(new_labels, predictions, average='weighted')

# Вывод
print(f"Accuracy: {accuracy:.2f}")
print("Precision Score:", precision)
print("Recall Score:", recall)
print("F1 Score:", f1)
