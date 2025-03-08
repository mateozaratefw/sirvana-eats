from playwright.sync_api import sync_playwright
import sys
import re
import json
import os
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_store_url(product_url):
    return product_url.split("?")[0]


def append_to_json(product_data, filename="products.json"):
    products_dir = "products"
    os.makedirs(products_dir, exist_ok=True)

    file_path = os.path.join(products_dir, filename)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    products.append(product_data)

    with open(file_path, "w") as f:
        json.dump(products, f, indent=2)


def scrape_product(url, output_filename="products.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            logger.info(f"Going to: {url}")
            page.goto(url)
            store_url = get_store_url(url)

            page.wait_for_selector('[data-qa="modal-name"]')

            name = page.locator('[data-qa="modal-name"]').inner_text()

            try:
                description = page.locator(
                    '[data-testid="product-info"] p'
                ).inner_text()
            except:
                description = ""

            price_text = page.locator('[data-testid="price"]').inner_text()

            price = (
                price_text.replace("$", "").replace(".", "").replace(",", ".").strip()
            )

            options = []
            if page.locator('[data-qa="topping-list"]').count() > 0:
                topping_list = page.locator('[data-qa="topping-list"]')
                topping_items = topping_list.locator('[data-qa="topping-item"]').all()

                for item in topping_items:
                    name_element = item.locator('[data-testid="typography"]').first
                    option_name = name_element.inner_text()

                    price_elements = item.locator('[data-testid="typography"]').all()
                    option_price = 0.0

                    if len(price_elements) > 1:
                        price_text = price_elements[1].inner_text()
                        if price_text:
                            price_match = re.search(
                                r"[\d.,]+", price_text.replace(".", "")
                            )
                            if price_match:
                                option_price = float(
                                    price_match.group().replace(",", ".")
                                )

                    options.append({"name": option_name, "price": option_price})

            image_element = page.locator(
                '[data-qa="modal-body"] > div > div > div > div > span > img'
            )
            image_url = image_element.get_attribute("src")

            product_data = {
                "name": name,
                "description": description,
                "price": float(price),
                "options": options,
                "image_url": image_url,
                "store_url": store_url,
            }

            append_to_json(product_data, output_filename)
            return product_data

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return None
        finally:
            browser.close()


if __name__ == "__main__":
    url = "https://www.rappi.com.ar/restaurantes/189247-arredondo?productDetail=2112146587"
    scrape_product(url)
