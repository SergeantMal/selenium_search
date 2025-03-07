from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

# Инициализация драйвера
driver = webdriver.Chrome()
driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")

assert "Википедия" in driver.title
time.sleep(1)

# Находим окно поиска
search_box = driver.find_element(By.ID, "searchInput")

# Вводим текст для поиска
query = input("Статью о чем вы хотите открыть? ")
query = query[0].upper() + query[1:].lower()  # Преобразуем в формат: первая буква заглавная, остальные строчные
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(1)

# Получаем список результатов поиска
results = []
elements = driver.find_elements(By.CLASS_NAME, 'mw-search-result')  # Ищем блоки результатов

for element in elements:
    try:
        link = element.find_element(By.CSS_SELECTOR, ".mw-search-result-heading a").get_attribute("href")
        results.append(link)
    except:
        print("Ссылка не найдена в элементе:", element.text)

# Если нашлись статьи, переходим на первую
if results:
    driver.get(results[0])
    header = driver.title
else:
    print("Ничего не найдено!")
    driver.quit()
    exit()

while True:
    print("\nЧто вы хотите сделать?")
    print("1. Листать параграфы статьи")
    print("2. Открыть связанную статью")
    print("3. Выход")
    choice = input()

    if choice == '1':
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            print(paragraph.text)
            input()  # Ждем нажатия перед следующим абзацем

    elif choice == '2':
        driver.get(random.choice(results))
        print("Открыли связанную статью:", driver.title)
        time.sleep(1)

        # Очищаем старые ссылки перед поиском новых
        all_links = []

        # Находим все ссылки внутри основного контента
        articles = driver.find_elements(By.CLASS_NAME, 'mw-content-ltr')

        for article in articles:
            links = article.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href:
                    all_links.append(href)

        while True:
            print("\nЧто вы хотите сделать?")
            print("1. Листать параграфы статьи")
            print("2. Открыть случайную внутреннюю статью")
            print("3. Вернуться в предыдущую статью ", header)
            choice = input()

            if choice == '1':
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                for paragraph in paragraphs:
                    print(paragraph.text)
                    input()

            elif choice == '2':
                if all_links:  # Проверяем, есть ли ссылки в списке
                    driver.get(random.choice(all_links))
                    print('Открыли случайную внутреннюю статью:', driver.title)
                else:
                    print("Нет доступных внутренних ссылок.")

            elif choice == '3':
                driver.get(results[0])
                break
    elif choice == '3':
        break

# Закрываем браузер после выхода
driver.quit()

