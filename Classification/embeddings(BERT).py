import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

# Пути к файлам с текстами для каждой модели
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'

def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower().split(', ') for line in f.readlines()]

rake_keywords = read_keywords(rake_file_path)
yake_keywords = read_keywords(yake_file_path)
keybert_keywords = read_keywords(keybert_file_path)

# Инициализация токенизатора и модели BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Функция для получения BERT эмбеддингов
def get_bert_embeddings(texts):
    embeddings = []
    for i, text in enumerate(texts):
        inputs = tokenizer(' '.join(text), return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :].detach().numpy()
        embeddings.append(cls_embedding.flatten())
        
        # Промежуточный вывод
        if i % 100 == 0:
            print(f"Processed {i} texts. Example vector (first 5 values): {cls_embedding.flatten()[:5]}")
    
    return np.array(embeddings)

# Получение эмбеддингов и их сохранение в файлы
rake_embeddings = get_bert_embeddings(rake_keywords)
yake_embeddings = get_bert_embeddings(yake_keywords)
keybert_embeddings = get_bert_embeddings(keybert_keywords)

np.save('rake_embeddings(BERT).npy', rake_embeddings)
np.save('yake_embeddings(BERT).npy', yake_embeddings)
np.save('keybert_embeddings(BERT).npy', keybert_embeddings)
