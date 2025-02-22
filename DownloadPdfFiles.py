from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)



try:
    # Открываем сайт
    driver.get("https://ras.arbitr.ru/")
        
    # Ждем, пока загрузится поле поиска
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "b-button-container"))
    )
    search_box.click()
    time.sleep(2)  # Ожидаем появления выпадающего списка

    # Проверяем, появился ли выпадающий список
    try:
        dropdown = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "b-document-list"))
        )
        print("Выпадающий список найден!") 
        # Получаем все элементы списка
        suggestions = dropdown.find_elements(By.TAG_NAME, "li")
        for idx, suggestion in enumerate(suggestions, 1):
            print(f"{idx}. {suggestion.text}")
    except:
        print("Выпадающий список отсутствует.")

finally:
    time.sleep(5)
