
#from datasets import load_dataset

# Загрузка датасета
##dataset = load_dataset("taln-ls2n/inspec",trust_remote_code=True)

#combined = pd.concat([pd.DataFrame(dataset[split]) for split in dataset.keys()])
#combined.to_csv("inspec_combined.csv", index=False)
#print("Объединённый датасет сохранён в inspec_combined.csv!")
#print("Датасет успешно сохранён в формате CSV!")

import pandas as pd
#file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"
# Загрузка датафрейма из файла CSV
#df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

 #Вывод первых нескольких строк датафрейма
#print(df.head(40))

# Проверка, что столбцы title и abstract существуют
#if 'title' in df.columns and 'abstract' in df.columns:
    # Объединение столбцов title и abstract в новый столбец Text
   # df['Text'] = df['title'].fillna('') + ' ' + df['abstract'].fillna('')
    
    # Сохранение обновленного датафрейма в новый файл
    #new_file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"
   # df.to_csv(new_file_path, index=False)
   # print(f"Обновленный датасет сохранен в {new_file_path}")
#else:
  #  print("Ошибка: В датафрейме отсутствуют столбцы 'title' и 'abstract'")
# Проверка, что столбец keyphrases существует



import pandas as pd

# Путь к вашему CSV-файлу
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # Использовать индекс из CSV

# Проверка, что столбец keyphrases существует
if 'keyphrases' in df.columns:
    # Путь для сохранения файла
    output_file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\nastroi hyperparameters\KeywordsIstin(Inspec).txt"
    
     # Преобразование столбца keyphrases в текст
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for keyphrases in df['keyphrases']:
            # Убираем скобки и кавычки, соединяем ключевые слова через запятую
            cleaned_keyphrases = ', '.join(eval(keyphrases)) if isinstance(keyphrases, str) else keyphrases
            f.write(cleaned_keyphrases + '\n')  # Записываем строку
            
    print(f"Столбец 'keyphrases' успешно сохранён в {output_file_path}")
else:
    print("Ошибка: В датафрейме отсутствует столбец 'keyphrases'")







import pandas as pd
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"
# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Вывод первых нескольких строк датафрейма
print(df.head(40))
