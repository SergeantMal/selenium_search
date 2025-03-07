from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")

assert "Википедия" in driver.title
time.sleep(1)
#Находим окно поиска
search_box = driver.find_element(By.ID, "searchInput")
#Прописываем ввод текста в поисковую строку. В кавычках тот текст, который нужно ввести
query = input("Статью о чем вы хотите открыть? ")
query = query[0].upper() + query[1:].lower()
search_box.send_keys(query)
#Добавляем не только введение текста, но и его отправку
search_box.send_keys(Keys.RETURN)
time.sleep(1)

try:
    link = driver.find_element(By.LINK_TEXT, query)
    # Добавляем клик на элемент
    link.click()
except:
    print("Статья не найдена")

while True:
    print('Что вы хотите сделать?')
    print('1. листать параграфы статьи')
    print('2. Открыть связанную статью')
    print('3. Выход')
    choice = input()
    if choice == '1':
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        # Для перебора пишем цикл
        for paragraph in paragraphs:
            print(paragraph.text)
            input()

    elif choice == '2':
        link = driver.find_element(By.LINK_TEXT, query)
        # Добавляем клик на элемент
        link.click()
    elif choice == '3':
        break
time.sleep(100)

