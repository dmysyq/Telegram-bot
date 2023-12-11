import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

class Product:
    def __init__(self, title, price, old_price, discount, link):
        self.title = title
        self.price = price
        self.old_price = old_price
        self.discount = discount
        self.link = link

    def calculate_discount(self):
        if self.old_price and self.price:
            old_price_float = float(''.join(filter(str.isdigit, self.old_price)))
            price_float = float(''.join(filter(str.isdigit, self.price)))
            return round(((old_price_float - price_float) / old_price_float) * 100)
        else:
            return None

def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open('result.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    return response.text

def parse_html_shopkz(html, base_url):
    print(f"Executing parse_html_shopkz for URL: {base_url}")

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='bx_catalog_item gtm-impression-product')

    products = []
    for item in items:
        title_element = item.find('div', class_='bx_catalog_item_title')
        title = title_element.text.strip() if title_element else None

        # Extracting the current price
        price_element = item.find('span', class_='current_price')
        price = price_element.text.strip() if price_element else None

        # Extracting the old price
        old_price_element = item.find('span', class_='old_price')
        old_price = old_price_element.text.strip() if old_price_element else None

        # Extracting the link
        link_element = title_element.find('a', href=True)
        link = urljoin(base_url, link_element['href']) if link_element else None

        product = Product(title, price, old_price, None, link)
        product.discount = product.calculate_discount()
        products.append(product)

    return products

def parse_html_sulpak(html, base_url):
    print(f"Executing parse_html_sulpak for URL: {base_url}")

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product__item product__item-js tile-container')

    products = []
    if not items:
        print("No product items found on the page.")
        return products

    for item in items:
        title_element_block = item.find('div', class_='product__item-name-block')
        title_element = title_element_block.find('div', class_='product__item-name') if title_element_block else None
        title = title_element.text.strip() if title_element else None

        # Extracting the current price
        price_element = item.find('div', class_='product__item-price')
        price = price_element.text.strip() if price_element else None

        # Extracting the old price
        old_price_element = item.find('div', class_='product__item-price-old')
        old_price = old_price_element.text.strip() if old_price_element else None

        # Extracting the link
        link_element = title_element_block.find('a', href=True)
        link = urljoin(base_url, link_element['href']) if link_element else None

        product = Product(title, price, old_price, None, link)
        product.discount = product.calculate_discount()
        products.append(product)

    if not products:
        print("No products were extracted from the page.")
    else:
        print(f"Extracted {len(products)} products from the page.")

    return products


def parse_html_dns(html, base_url):
    print(f"Executing parse_html_dns for URL: {base_url}")

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-product ui-button-widget')

    products = []
    if not items:
        print("No product items found on the page.")
        return products

    for item in items:
        # Extracting the title and link
        title_element = item.find('a', class_='catalog-product__name', href=True)
        title = title_element.text.strip() if title_element else None
        link = urljoin(base_url, title_element['href']) if title_element else None

        # Extracting the current price
        price_element = item.find('div', class_='product-buy__price_active')
        price = price_element.text.strip() if price_element else None

        # Extracting the old price
        old_price_element = item.find('span', class_='product-buy__prev')
        old_price = old_price_element.text.strip() if old_price_element else None

        product = Product(title, price, old_price, None, link)
        product.discount = product.calculate_discount()
        products.append(product)

    if not products:
        print("No products were extracted from the page.")
    else:
        print(f"Extracted {len(products)} products from the page.")

    return products


def get_parsed_products(category, start_page, end_page):
    base_url = get_base_url(category)
    if base_url is None:
        print(f"Invalid category: {category}. Returning empty list.")
        return []  # Вернуть пустой список, если категория не распознана

    products_to_send = []

    # Define category-specific filter function
    category_filter = get_category_filter(category)

    if category_filter is None:
        print(f"No filter found for category: {category}. Returning empty list.")
        return []

    for page_num in range(start_page, end_page + 1):
        url = f'{base_url}{page_num}'
        print(f"Processing page {page_num} for URL: {url}")
        html = get_page(url)
        if category_filter:
            products = category_filter(html, base_url)
        else:
            print(f"No filter found for category: {category}. Returning empty list.")
            return []  # Вернуть пустой список, если фильтр не определен

        # Filtering out products with no old price
        filtered_products = [product for product in products if product.old_price is not None]
        for product in filtered_products:
            if product.discount is not None and product.discount > 15:
                products_to_send.append(product)

    return products_to_send

def get_category_filter(category):
    if category == 'smartphones_shopkz':
        return parse_html_shopkz
    elif category == 'video_cards_shopkz':
        return parse_html_shopkz
    elif category == 'laptops_shopkz':
        return parse_html_shopkz
    elif category == 'smartphones_sulpakkz':
        return parse_html_sulpak
    elif category == 'video_cards_sulpakkz':
        return parse_html_sulpak
    elif category == 'laptops_sulpakkz':
        return parse_html_sulpak
    elif category == 'smartphones_dns':
        return parse_html_dns
    elif category == 'video_cards_dns':
        return parse_html_dns
    elif category == 'laptops_dns':
        return parse_html_dns
    else:
        return None

def get_base_url(category):
    if category == 'smartphones_shopkz':
        return 'https://shop.kz/almaty/offers/smartfony/?PAGEN_1='
    elif category == 'video_cards_shopkz':
        return 'https://shop.kz/almaty/offers/videokarty/filter/action_filter-is-%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B0%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82/apply/?PAGEN_1='
    elif category == 'laptops_shopkz':
        return 'https://shop.kz/almaty/offers/noutbuki/?PAGEN_1='
    elif category == 'smartphones_sulpakkz':
        return 'https://www.sulpak.kz/f/smartfoniy?page='
    elif category == 'video_cards_sulpakkz':
        return 'https://www.sulpak.kz/f/videokartiy?page='
    elif category == 'laptops_sulpakkz':
        return 'https://www.sulpak.kz/f/noutbuki?page='
    elif category == 'smartphones_dns':
        return 'https://www.dns-shop.kz/catalog/17a8a01d16404e77/smartfony/?p='
    elif category == 'video_cards_dns':
        return 'https://www.dns-shop.kz/catalog/17a89aab16404e77/videokarty/?p='
    elif category == 'laptops_dns':
        return 'https://www.dns-shop.kz/catalog/17a892f816404e77/noutbuki/?p='
    else:
        return None

def main():
    start_page = 1
    end_page = 10
    category = 'smartphones_shopkz'
    get_parsed_products(category, start_page, end_page)

if __name__ == '__main__':
    main()
