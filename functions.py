import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def collect_product_info(driver, url=''):

    driver.switch_to.new_window('tab')

    time.sleep(2)
    driver.get(url=url)
    time.sleep(3)

    product_id = driver.find_element(
        By.XPATH, '//div[contains(text(), "Артикул: ")]'
    ).text.split(': ')[1]

    page_source = str(driver.page_source) # сохраняем весь html-код страницы в переменную
    soup = BeautifulSoup(page_source, 'lxml') # парсим страницу

    with open(f'product_{product_id}.html', 'w', encoding='utf-8') as file:
        file.write(page_source)

    product_name = soup.find('h1', attrs={'class': 'pdp_g1b tsHeadline550Medium'}).text.strip()

    try:
        product_statistic = soup.find(
            'div', attrs={'data-widget': 'webSingleProductScore'}
        ).text.strip()

        if ' • ' in product_statistic:
            product_stars = product_statistic.split(' • ')[0].strip()
            product_reviews = product_statistic.split(' • ')[1].strip()
        else:
            product_statistic = product_statistic
    except:
        product_statistic = None
        product_stars = None
        product_reviews = None

    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
        product_ozon_card_price = ozon_card_price_element.text.strip(
        ).replace(' ', '') if ozon_card_price_element else ''

        price_element = soup.find(
            'span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

        product_discount_price = price_element[0].text.strip(
        ).replace(' ', '') if price_element[0] else ''
        product_base_price = price_element[1].text.strip(
        ).replace(' ', '') if price_element[1] is not None else ''
    except:
        product_ozon_card_price = None
        product_discount_price = None
        product_base_price = None

        # product price
    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
    except AttributeError:
        card_price_div = soup.find(
            'div', attrs={"data-widget": "webPrice"}).findAll('span')

        product_base_price = card_price_div[0].text.strip()
        product_discount_price = card_price_div[1].text.strip()

    product_data = (
        {
            'product_id': product_id,
            'product_name': product_name,
            'product_ozon_card_price': product_ozon_card_price,
            'product_discount_price': product_discount_price,
            'product_base_price': product_base_price,
            'product_statistic': product_statistic,
            'product_stars': product_stars,
            'product_reviews': product_reviews,
        }
    )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return product_data