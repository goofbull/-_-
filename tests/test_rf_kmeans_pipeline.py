import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.base import BaseEstimator, TransformerMixin
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ClusterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=2, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=n_clusters, n_init='auto', random_state=random_state)
    
    def fit(self, X, y=None):
        self.kmeans.fit(X)
        return self
    
    def transform(self, X):
        clusters = self.kmeans.predict(X)
        X_with_clusters = pd.DataFrame(X.toarray())
        X_with_clusters['cluster'] = clusters
        X_with_clusters.columns = X_with_clusters.columns.astype(str)
        return X_with_clusters

@pytest.fixture
def trained_pipeline():
    texts = ["cat sat on mat", "dog barked loudly", "fish swam in pond", "bird flew high"]
    labels = ["cat", "dog", "fish", "bird"]
    pipeline = ImbPipeline([
        ('tfidf', TfidfVectorizer()),
        ('cluster', ClusterTransformer(n_clusters=2)),
        ('oversample', RandomOverSampler(random_state=42)),
        ('clf', RandomForestClassifier(
            n_estimators=10,
            bootstrap=True,
            class_weight='balanced',
            max_features=2,
            max_depth=5,
            random_state=42
        ))
    ])
    pipeline.fit(texts, labels)
    return pipeline

def test_pipeline_with_unseen_or_empty_texts(trained_pipeline):
    # Unseen text and empty string
    test_texts = ["elephant trumpets", "", "the quick brown fox", "cat sat on mat"]
    # Should not raise and should return predictions for all inputs
    predictions = trained_pipeline.predict(test_texts)
    assert len(predictions) == len(test_texts)
    # Check that predictions are strings (labels)
    assert all(isinstance(label, str) for label in predictions)

def test_pipeline_with_missing_values():
    texts = ["cat sat on mat", None, "dog barked loudly", ""]
    labels = ["cat", "dog", "dog", "cat"]

    # Заменяем None на пустую строку
    texts_cleaned = [text if text is not None else "" for text in texts]

    pipeline = ImbPipeline([
        ('tfidf', TfidfVectorizer()),
        ('cluster', ClusterTransformer(n_clusters=2)),
        ('oversample', RandomOverSampler(random_state=42)),
        ('clf', RandomForestClassifier(
            n_estimators=10,
            bootstrap=True,
            class_weight='balanced',
            max_features=2,
            max_depth=5,
            random_state=42
        ))
    ])

    pipeline.fit(texts_cleaned, labels)


def test_random_oversampler_balances_classes():
    texts = ["apple", "banana", "cherry", "date", "elderberry", "fig"]
    labels = ["fruit", "fruit", "fruit", "fruit", "fruit", "not-fruit"]
    pipeline = ImbPipeline([
        ('tfidf', TfidfVectorizer()),
        ('cluster', ClusterTransformer(n_clusters=2)),
        ('oversample', RandomOverSampler(random_state=42)),
        ('clf', RandomForestClassifier(n_estimators=10, random_state=42))
    ])
    X = pipeline.named_steps['tfidf'].fit_transform(texts)
    X_cluster = pipeline.named_steps['cluster'].fit_transform(X)
    X_resampled, y_resampled = pipeline.named_steps['oversample'].fit_resample(X_cluster, labels)
    unique, counts = np.unique(y_resampled, return_counts=True)
    # All classes should have the same number of samples after oversampling
    assert len(set(counts)) == 1

def test_cluster_transformer_adds_cluster_labels():
    texts = ["red apple", "green apple", "yellow banana", "ripe banana"]
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(texts)
    transformer = ClusterTransformer(n_clusters=2, random_state=42)
    transformer.fit(X)
    X_with_clusters = transformer.transform(X)
    # The last column should be 'cluster' and contain only 0 or 1 (since n_clusters=2)
    assert 'cluster' in X_with_clusters.columns
    assert set(X_with_clusters['cluster'].unique()).issubset({0, 1})

def test_pipeline_fit_predict_valid_data():
    train_texts = ["dog barks", "cat meows", "fish swims", "bird flies"]
    train_labels = ["mammal", "mammal", "fish", "bird"]
    test_texts = ["dog runs", "cat sleeps", "fish jumps", "bird sings"]
    test_labels = ["mammal", "mammal", "fish", "bird"]
    pipeline = ImbPipeline([
        ('tfidf', TfidfVectorizer()),
        ('cluster', ClusterTransformer(n_clusters=3)),
        ('oversample', RandomOverSampler(random_state=42)),
        ('clf', RandomForestClassifier(n_estimators=10, random_state=42))
    ])
    pipeline.fit(train_texts, train_labels)
    predictions = pipeline.predict(test_texts)
    assert len(predictions) == len(test_texts)
    # Compute metrics to ensure pipeline produces valid outputs
    acc = accuracy_score(test_labels, predictions)
    prec = precision_score(test_labels, predictions, average='weighted', zero_division=0)
    rec = recall_score(test_labels, predictions, average='weighted', zero_division=0)
    f1 = f1_score(test_labels, predictions, average='weighted', zero_division=0)
    assert 0.0 <= acc <= 1.0
    assert 0.0 <= prec <= 1.0
    assert 0.0 <= rec <= 1.0
    assert 0.0 <= f1 <= 1.0