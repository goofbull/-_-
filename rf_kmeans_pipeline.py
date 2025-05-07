import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import RandomOverSampler


# Загрузка данных
df = pd.read_csv('./csv/prepared_data.csv')

texts = df['data']  # Тексты для обучения
labels = df['decision'].tolist()  # Метки решений

# Кастомный трансформер для добавления кластеров
class ClusterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=20, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=n_clusters, n_init='auto', random_state=random_state)
    
    def fit(self, X, y=None):
        self.kmeans.fit(X)
        return self
    
    def transform(self, X):
        clusters = self.kmeans.predict(X)
        # Преобразование X (матрица признаков) в DataFrame и добавляем кластерные метки
        X_with_clusters = pd.DataFrame(X.toarray())
        X_with_clusters['cluster'] = clusters
        X_with_clusters.columns = X_with_clusters.columns.astype(str)
        return X_with_clusters

# Создание пайплайна
pipeline_with_random_oversampler = ImbPipeline([
    ('tfidf', TfidfVectorizer()),
    ('cluster', ClusterTransformer()),
    ('oversample', RandomOverSampler(random_state=42)),
    ('clf', RandomForestClassifier(n_estimators=100, bootstrap=True, class_weight='balanced', 
                                   max_features=6, max_depth=100, random_state=42))
])

pipeline_with_random_oversampler.fit(texts, labels)
df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
new_texts = df2['data']
new_labels = df2['decision']

# Предсказания
predictions = pipeline_with_random_oversampler.predict(new_texts)

# Метрики
accuracy = accuracy_score(new_labels, predictions)
precision = precision_score(new_labels, predictions, average='weighted')
recall = recall_score(new_labels, predictions, average='weighted')
f1 = f1_score(new_labels, predictions, average='weighted')

# Печать результатов
print(f"Accuracy: {accuracy:.2f}")
print("Precision Score: ", precision)
print("Recall Score: ", recall)
print("F1 Score: ", f1)


cm = confusion_matrix(df2['decision'], predictions)
print("Confusion Matrix:\n", cm)