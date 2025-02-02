import spacy

# Загрузка модели spaCy
nlp = spacy.load("en_core_web_sm")

# Путь к файлу с ключевыми словами
input_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/MultipartiteRank_keywords(Inspec-6).txt'
output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/MultipartiteRankLemma_keywords(Inspec-6).txt'

# Функция для лемматизации набора ключевых слов
def lemmatize_keywords(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Разделяем строку на фразы (предполагается, что они разделены запятыми)
            phrases = [phrase.strip() for phrase in line.strip().split(',')]
            
            # Лемматизация каждой фразы
            updated_phrases = []
            for phrase in phrases:
                doc = nlp(phrase.lower())
                # Лемматизируем каждое слово в фразе и собираем обратно в строку
                lemmatized_phrase = " ".join([token.lemma_ for token in doc])
                # Если лемматизация изменила фразу, заменяем ее и выводим изменения
                if lemmatized_phrase != phrase.lower():
                    print(f"Изменение: '{phrase}' -> '{lemmatized_phrase}'")
                updated_phrases.append(lemmatized_phrase if lemmatized_phrase != phrase.lower() else phrase)

            # Записываем результат в выходной файл
            outfile.write(", ".join(updated_phrases) + "\n")

# Запуск функции
lemmatize_keywords(input_file_path, output_file_path)

print(f"Ключевые слова сохранены с учетом изменений в файл: {output_file_path}")
