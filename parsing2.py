import re
import os
import threading
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

# Функция для получения ссылок на статьи
def get_data_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)  # Задержка для загрузки страницы
        links = driver.find_elements(By.CSS_SELECTOR, 'a.fw-bold')
        unique_links = list(set([link.get_attribute("href") for link in links]))  # Проверка уникальности ссылок
        driver.quit()  # Корректное закрытие драйвера
        return unique_links
    except Exception as ex:
        print(f"Error in get_data_selenium: {ex}")
        return []

# Функция для извлечения ключевых слов из HTML-файла
def extract_keywords_from_html(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return [], [], []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            page_content = file.read()
        
        soup = BeautifulSoup(page_content, 'html.parser')
        
        json_data = None
        for script in soup.find_all('script'):
            try:
                script_content = script.string
                if script_content:
                    # Регулярное выражение для поиска JSON-данных
                    match = re.search(r'xplGlobal\.document\.metadata\s*=\s*(\{.*?\});', script_content, re.DOTALL)
                    if match:
                        json_text = match.group(1)
                        json_data = json.loads(json_text)
                        break
            except Exception as e:
                print(f"Error processing script: {e}")
                continue

        if not json_data:
            print("No JSON data found in HTML.")
            return [], [], []

        ieee_keywords = []
        index_terms = []
        author_keywords = []

        for keyword_section in json_data.get('keywords', []):
            if keyword_section.get('type') == "IEEE Keywords":
                ieee_keywords.extend(keyword_section.get('kwd', []))
            elif keyword_section.get('type') == "Author Keywords":
                author_keywords.extend(keyword_section.get('kwd', []))
            elif keyword_section.get('type') == "Index Terms":
                index_terms.extend(keyword_section.get('kwd', []))

        return list(set(ieee_keywords)), list(set(index_terms)), list(set(author_keywords))  # Удаляем дубликаты
    
    except Exception as e:
        print(f"Error extracting keywords from HTML: {e}")
        return [], [], []

# Функция для парсинга данных с конкретной страницы статьи
def ged_data_publikum(url, semaphore, result_lock, result, thread_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(7)  # Задержка для загрузки страницы

        # Уникальное имя файла для сохранения страницы
        file_name = f"driverpage_{thread_id}.html"
        page_source = driver.page_source
        
        # Убедитесь, что файл создан и доступен для записи
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(page_source)
        
        # Извлечение данных
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()  # Корректное закрытие драйвера

        title_element = soup.find("h1", class_="document-title text-2xl-md-lh").find("span")
        title = title_element.text.strip() if title_element else 'Заголовок не найден'

        annotation_element = soup.find("div", class_="abstract-text row g-0").find("div")
        annotation = annotation_element.text.strip().replace("Abstract:", "") if annotation_element else "Аннотация не найдена"
        
        # Извлечение ключевых слов
        ieee_keywords, index_terms, author_keywords = extract_keywords_from_html(file_name)
        ieee_keywords_str = ", ".join(ieee_keywords) if ieee_keywords else "Keywords not found"
        index_terms_str = ", ".join(index_terms) if index_terms else "Keywords not found"
        author_keywords_str = ", ".join(author_keywords) if author_keywords else "Keywords not found"

        # Добавление данных в общий список с использованием блокировки
        with result_lock:
            result.append((title, annotation, ieee_keywords_str, index_terms_str, author_keywords_str))

        # Задержка перед удалением файла для предотвращения конфликтов доступа
        time.sleep(3)
        
        # Удаление временного файла
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as ex:
        print(f"Error in ged_data_publikum: {ex}")
    finally:
        semaphore.release()

# Функция для обработки страницы поиска и запуска парсинга для каждой статьи
def process_page(url, semaphore, result_lock):
    result = []
    urls = get_data_selenium(url)
    threads = []
    thread_id = 0  # Идентификатор для потока и имени файла
    for link in urls:
        semaphore.acquire()
        thread = threading.Thread(target=ged_data_publikum, args=(link, semaphore, result_lock, result, thread_id))
        threads.append(thread)
        thread.start()
        thread_id += 1  # Увеличение идентификатора потока для уникальных имен файлов
    for thread in threads:
        thread.join()

    # Объединение результатов из всех потоков
    titles = [item[0] for item in result if item[0]]
    annotations = [item[1] for item in result if item[1]]
    ieee_keywords = [item[2] for item in result if item[2]]
    index_terms = [item[3] for item in result if item[3]]
    author_keywords = [item[4] for item in result if item[4]]

    return titles, annotations, ieee_keywords, index_terms, author_keywords

if __name__ == '__main__':
    semaphore = threading.Semaphore(5)  # Ограничение на 5 параллельных запросов
    result_lock = threading.Lock()  # Блокировка для защиты доступа к общим спискам
    urls = [f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Fuzzy%20Logic&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber={i}&rowsPerPage=100&refinements=PublicationTopics:Fuzzy%20Logic&returnFacets=ALL' for i in range(1, 11+1)]
    
    all_titles = []
    all_annotations = []
    all_ieee_keywords = []
    all_index_terms = []
    all_author_keywords = []
    
    for url in urls:
        titles, annotations, ieee_keywords, index_terms, author_keywords = process_page(url, semaphore, result_lock)
        all_titles.extend(titles)
        all_annotations.extend(annotations)
        all_ieee_keywords.extend(ieee_keywords)
        all_index_terms.extend(index_terms)
        all_author_keywords.extend(author_keywords)
    
    # Сохранение заголовков в файл
    with open("titles(FL).txt", "w", encoding="utf-8") as file:
        for title in all_titles:
            file.write(title + "\n")
    
    # Сохранение аннотаций в файл
    with open("annotations(FL).txt", "w", encoding="utf-8") as file:
        for annotation in all_annotations:
            file.write(annotation + "\n")
    
    # Сохранение ключевых слов в файл
    with open("IEE-keywords(FL).txt", "w", encoding="utf-8") as file:
        for keyword_string in all_ieee_keywords:
            file.write(keyword_string + "\n")
    
    # Сохранение Index Terms в файл
    with open("Index-terms(FL).txt", "w", encoding="utf-8") as file:
        for index_term_string in all_index_terms:
            file.write(index_term_string + "\n")
    
    # Сохранение Author Keywords в файл
    with open("Author-keywords(FL).txt", "w", encoding="utf-8") as file:
        for author_keyword_string in all_author_keywords:
            file.write(author_keyword_string + "\n")

    print("Заголовки, аннотации и ключевые слова сохранены в файл")
