import csv
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# Загрузка обучающих данных
df = pd.read_csv('./csv/prepared_data.csv')
texts = df['data']
labels = df['decision'].tolist()

# Векторизация текста
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(texts)

# Кластеризация
kmeans = KMeans(n_clusters=10, n_init='auto', random_state=42)
cluster_labels = kmeans.fit_predict(X_tfidf)

# Дополнительные признаки
additional_features = df[['region', 'judge', 'articles']].copy()
for col in additional_features.columns:
    additional_features[col] = LabelEncoder().fit_transform(additional_features[col].astype(str))

# Объединение TF-IDF + кластер + дополнительные признаки
X_with_clusters = pd.DataFrame(X_tfidf.toarray())
X_with_clusters['cluster'] = cluster_labels
X_with_clusters = pd.concat([X_with_clusters, additional_features.reset_index(drop=True)], axis=1)
X_with_clusters.columns = X_with_clusters.columns.astype(str)
# Обучение модели
clf = RandomForestClassifier(
    n_estimators=100,
    bootstrap=True,
    class_weight='balanced',
    max_features=3,
    max_depth=100,
    random_state=42
)
clf.fit(X_with_clusters, labels)

# Загрузка тестовых данных
df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
new_texts = df2['data']
X_new_tfidf = vectorizer.transform(new_texts)
new_cluster = kmeans.predict(X_new_tfidf)

# Подготовка дополнительных признаков для теста
new_additional = df2[['region', 'judge', 'articles']].copy()
for col in new_additional.columns:
    new_additional[col] = LabelEncoder().fit_transform(new_additional[col].astype(str))

# Объединение тестовой матрицы признаков
X_new_df = pd.DataFrame(X_new_tfidf.toarray())
X_new_df['cluster'] = new_cluster
X_new_df = pd.concat([X_new_df, new_additional.reset_index(drop=True)], axis=1)
X_new_df.columns = X_new_df.columns.astype(str)
# Предсказание
prediction = clf.predict(X_new_df)

# Оценка
accuracy = accuracy_score(df2['decision'], prediction)
print(f"Accuracy: {accuracy:.2f}")
print("Precision Score : ", precision_score(df2['decision'], prediction, average='micro'))
print("Recall Score : ", recall_score(df2['decision'], prediction, average='micro'))
print("F1 Score : ", f1_score(df2['decision'], prediction, average='micro'))

# Матрица путаницы
cm = confusion_matrix(df2['decision'], prediction)
print("Confusion Matrix:\n", cm)
