import requests
# import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select

headers = {
    'authority': 'ras.arbitr.ru',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

session = requests.session()

response = session.get("https://ras.arbitr.ru/", headers=headers)

if response.status_code == 200:
    print("Success")
else:
    print("Bad result")


service = Service(GeckoDriverManager().install())
firefox_options = Options()
firefox_options.add_argument("--start-maximized")  # Запуск браузера в полноэкранном режиме


driver = webdriver.Firefox(service=service, options=firefox_options)


driver.get('https://ras.arbitr.ru/')

# Закрываем всплывающее окно
close_popup_banner = driver.find_element(By.CLASS_NAME, 'b-promo_notification-popup-close')
close_popup_banner.click()


type_of_argument_select = driver.find_element(By.CLASS_NAME, "js-select")

select = Select(type_of_argument_select)


find_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/dl/dd/div[9]/div/div/button"))
)
find_button.click()

print(driver.current_url)
driver.quit()