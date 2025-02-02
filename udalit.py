import pandas as pd
import re

# Пример данных
df = pd.DataFrame({
    'Title': ["Text Mining Techniques for Knowledge of Defects in Power Equipment"]
})

# Ключевые слова с несколькими словами
phrases = ["equipment based, research advances, text mining techniques, application, automatic classification, evaluation, defects according, challenges, severity, precise extraction, ontology dictionary, typical applications, knowledge, help readers, general steps, summarize, equipment, paper, paper first analyzes, systematically, construction, field, including, power equipment defects, electric power equipment, health status, power equipment text mining techniques, end, defects, defect details, work, research hotspot, quickly know, text mining, text information, proposed, knowledge graphs, power equipment, become, face, research hotspots, focuses, techniques"]
phrases = [phrase.strip().lower() for phrase in phrases[0].split(',')]
print(phrases)
def count_keyword_phrases(text, phrases):
    text = text.lower()
    count = 0
    matches = []
    for phrase in phrases:
        if phrase in text:
            count += text.count(phrase)
            matches.append(phrase)
    return count, matches

# Применение функции к данным
df['Count'], df['Matches'] = zip(*df['Title'].apply(lambda x: count_keyword_phrases(x, phrases)))

print(df)
