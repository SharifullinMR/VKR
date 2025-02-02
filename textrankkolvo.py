# Путь к файлу с ключевыми словами, сохраненными TextRank
textrank_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords.txt'

# Чтение ключевых слов из файла
with open(textrank_output_file_path, 'r', encoding='utf-8') as f:
    # Каждая строка файла содержит ключевые слова, разделенные запятыми
    keywords_lines = [line.strip().split(', ') for line in f.readlines()]

# Подсчет общего количества ключевых слов
total_keywords = sum(len(keywords) for keywords in keywords_lines)

# Вывод результата
print(f"Общее количество ключевых слов, извлеченных TextRank: {total_keywords}")
