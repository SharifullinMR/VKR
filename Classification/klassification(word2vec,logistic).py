import pandas as pd
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Пути к файлам с текстами для каждой модели
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
keybert_file_path ='C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'

def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower().split(', ') for line in f.readlines()]

rake_keywords = read_keywords(rake_file_path)
yake_keywords = read_keywords(yake_file_path)
keybert_keywords = read_keywords(keybert_file_path)

# Определение истинных меток классов для каждого текста
true_labels = ['Text Mining'] * 1100 + ['Information Retrieval'] * 1100 + ['Fuzzy Logic'] * 1100

# Функция для векторизации текстов и классификации
def classify_texts(keywords, true_labels):
    # Создание модели Word2Vec
    word2vec_model = Word2Vec(sentences=keywords, vector_size=100, window=5, min_count=1, workers=4)
    
    def get_mean_vector(model, words):
        # Получение среднего вектора для списка слов
        words = [word for word in words if word in model.wv]
        if len(words) >= 1:
            return np.mean(model.wv[words], axis=0)
        else:
            return np.zeros(model.vector_size)

    # Векторизация всех текстов
    X = np.array([get_mean_vector(word2vec_model, text) for text in keywords])
    
    # Инициализация классификатора логистической регрессии
    clf = LogisticRegression(max_iter=1000)
    
    # Прогнозирование классов с использованием кросс-валидации
    y_pred = cross_val_predict(clf, X, true_labels, cv=5)
    
    # Вычисление метрик качества
    accuracy = accuracy_score(true_labels, y_pred)
    report = classification_report(true_labels, y_pred, zero_division=0)
    
    # Создание DataFrame с истинными и предсказанными метками
    misclassifications = pd.DataFrame({
        'True Label': true_labels,
        'Predicted Label': y_pred
    })
    
    return accuracy, report, misclassifications

# Классификация и оценка для каждого набора ключевых слов
rake_accuracy, rake_report, rake_misclassifications = classify_texts(rake_keywords, true_labels)
yake_accuracy, yake_report, yake_misclassifications = classify_texts(yake_keywords, true_labels)
keybert_accuracy, keybert_report, keybert_misclassifications = classify_texts(keybert_keywords, true_labels)

# Вывод результатов
print("RAKE Classification:")
print(f"Accuracy: {rake_accuracy:.2f}")
print("\nClassification Report:\n", rake_report)
print("\nMisclassifications (first 10 rows):\n", rake_misclassifications.head(10))

print("YAKE Classification:")
print(f"Accuracy: {yake_accuracy:.2f}")
print("\nClassification Report:\n", yake_report)
print("\nMisclassifications (first 10 rows):\n", yake_misclassifications.head(10))

print("KeyBERT Classification:")
print(f"Accuracy: {keybert_accuracy:.2f}")
print("\nClassification Report:\n", keybert_report)
print("\nMisclassifications (first 10 rows):\n", keybert_misclassifications.head(10))
