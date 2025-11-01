import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from functions import collect_product_info

def get_products_links(item_name='macbook air m3'):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}&cpumodel=101062019&sorting=rating'
    driver.get(url=current_url)
    time.sleep(2)

    # for i in range(3): # крутим страницу вниз
    #     driver.execute_script("window.scrollBy(0, 200);")
    #     time.sleep(1)

    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
        product_urls = list(set([f'{link.get_attribute('href')}' for link in find_links]))[:5]

        print('[+] Ссылки на товары успешно собраны!')
    except:
        print('[!] Что-то пошло не так со сбором ссылок на товары!')

    product_urls_dict = {}

    for i, j in enumerate(product_urls):
        product_urls_dict[i] = j

    with open('products.json', 'w', encoding='utf-8') as file:
        json.dump(product_urls_dict, file, indent=4, ensure_ascii=False)

    time.sleep(2)

    products_data = []

    for i in product_urls:
        data = collect_product_info(driver=driver, url=i)
        print(f'[+] Собрал данные товара с id: {data['product_id']}')
        time.sleep(2)
        products_data.append(data)

    with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)


    driver.close()
    driver.quit()


def main():
    print('[INFO] Сбор данных начался. Пожалуйста, ожидайте...')
    get_products_links()
    print('[INFO] Сбор данных завершен успешно!')

if __name__ == '__main__':
    main()


# https://www.ozon.ru/category/noutbuki-15692/apple-26303000/?brand_was_predicted=true&category_was_predicted=true&deny_category_prediction=true&from_global=true&text=macbook+air+m3
