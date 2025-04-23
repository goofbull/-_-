import csv
import pandas as pd
#from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#import category_encoders as ce
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv('./csv/prepared_data.csv')

# df_copy = df.copy()
#all_text = []
# low_reg_text = []


# df.to_csv('./csv/arbitr_dataset.csv', index=False, encoding='utf-8')

texts = df['data']#.iloc[1:101].str.lower() + '.'

labels = df['decision'].tolist()  # Колонка с метками решений

# Векторизация текста с помощью TfidfVectorizer
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(texts)

# Применяем кластеризацию (если нужно для извлечения признаков)

kmeans = KMeans(n_clusters=10, n_init='auto', random_state=42)

cluster_labels = kmeans.fit_predict(X_tfidf)

# Объединяем TF-IDF и кластеры
X_with_clusters = pd.DataFrame(X_tfidf.toarray())
X_with_clusters['cluster'] = cluster_labels

# Приводим все столбцы к строковому типу
X_with_clusters.columns = X_with_clusters.columns.astype(str)

# Обучаем классификатор (Random Forest)
clf = RandomForestClassifier(n_estimators=100, bootstrap = True, class_weight = 'balanced', max_features = 4,
                            max_depth=100, random_state=42)
clf.fit(X_with_clusters, labels)

# # Новый текст для предсказания

df2 = pd.read_csv('./csv/prepared_data_for_testing.csv')
new_texts = df2['data']


X_new_tfidf = vectorizer.transform(new_texts)
new_cluster = kmeans.predict(X_new_tfidf)

# Добавляем кластер к вектору
X_new_df = pd.DataFrame(X_new_tfidf.toarray())
X_new_df['cluster'] = new_cluster

# Приводим столбцы к строковому типу
X_new_df.columns = X_new_df.columns.astype(str)

# Предсказание
prediction = clf.predict(X_new_df)
#print("Предсказание:", prediction[0])

# Оценка модели на обучающих данных
#predictions = clf.predict(X_with_clusters)
# print(classification_report(labels, predictions))
# print(f'Accuracy: {accuracy_score(df['decision'], predictions)}')
accuracy = accuracy_score(df2['decision'], prediction)

print(f"Accuracy: {accuracy:.2f}")
print("Precision Score : ", precision_score(df2['decision'], prediction, average='micro'))
print("Recall Score : ", recall_score(df2['decision'], prediction, average='micro'))
print("F1 Score : ", f1_score(df2['decision'], prediction, average='micro'))