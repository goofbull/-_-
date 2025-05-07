from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from ruslingua import RusLingua
import wikipediaapi
from weasyprint import HTML
import time

ruslingua = RusLingua()


chrome_driver_path = 'E:\\chromedriver-win64\\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без графического интерфейса (для серверов)
chrome_options.add_argument("--ignore-certificate-errors")  # Отключаем проверку SSL-сертификатов
chrome_options.add_argument("--disable-web-security")  # Отключаем дополнительные проверки безопасности

Создаём объект драйвера
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
driver.get("https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%AE%D1%80%D0%B8%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D1%8B/ru")
print(driver.title)

results = []
word = 'банкрот'
Однокоренные слова
cognates = ruslingua.get_cognate_words(''+str(word)+'')
print(cognates)

i = 1
while i < 6:
   for x in cognates:
       print(x)

       true_answer = 0
       while true_answer != 1:
           try:
               list_item = driver.find_element(By.LINK_TEXT, ''+str(x)+'')
               list_item.click()
               print(driver.current_url)
               results.append(x)
               true_answer = 1          
           except:
               true_answer = 1
               pass
   i += 1

print(results)

