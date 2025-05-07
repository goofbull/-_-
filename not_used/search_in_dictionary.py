from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
from important_features import same_words

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
legal_terms =[]


for word in same_words:

    try:
        # Открываем сайт
        driver.get("https://juridical.slovaronline.com/")
        
        # Ждем, пока загрузится поле поиска
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "s"))
        )
        check_dictionary = "юридический словарь"
        # Вводим "иск"
        search_box.send_keys(word)
        time.sleep(2)  # Ожидаем появления выпадающего списка

        # Проверяем, появился ли выпадающий список
        try:
            dropdown = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-autocomplete"))
            )
            print("Выпадающий список найден!")
            
            # Получаем все элементы списка
            suggestions = dropdown.find_elements(By.TAG_NAME, "li")
            for idx, suggestion in enumerate(suggestions, 1):
                print(f"{idx}. {suggestion.text}")
                if check_dictionary in suggestion.text:
                    print("СЛОВАРЬ НАЙДЕН")
                    legal_terms.append(word)
                    break
        except:
            print("Выпадающий список отсутствует.")

    finally:
        time.sleep(5)  # Даем время посмотреть результат
        continue

legal_terms = list(dict.fromkeys(legal_terms))

driver.quit()
print(legal_terms)