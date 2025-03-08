import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urlunsplit
from typing import Dict, List


def get_base_url(url: str) -> str:
    """Remove query parameters from URL."""
    parsed = urlparse(url)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def find_product_id(soup: BeautifulSoup, product_name: str) -> str:
    """Find product ID by searching for the product name and traversing up to find the product-info div."""
    elements = soup.find_all(
        lambda tag: tag.string and product_name.lower() in tag.string.lower()
    )

    elements.extend(soup.find_all(attrs={"data-test-id": True}))
    elements.extend(soup.find_all(["h3", "span"]))

    for element in elements:
        if product_name.lower() in element.get_text().lower():
            current = element
            while current and current.name != "div":
                current = current.parent
                if current:
                    data_qa = current.get("data-qa", "")
                    if data_qa.startswith("product-info-"):
                        return data_qa.replace("product-info-", "")

    product_divs = soup.find_all(
        "div", attrs={"data-qa": lambda x: x and x.startswith("product-info-")}
    )
    for div in product_divs:
        if product_name.lower() in div.get_text().lower():
            return div["data-qa"].replace("product-info-", "")

    return None


def update_product_urls(
    menu_items: List[Dict], soup: BeautifulSoup, store_url: str
) -> List[Dict]:
    """Update product URLs with product IDs."""
    for item in menu_items:
        product_id = find_product_id(soup, item["name"])
        if product_id:
            item["product_url"] = f"{store_url}?productDetail={product_id}"
    return menu_items


def extract_menu_items(url: str) -> List[Dict]:
    """Extract menu items from Rappi's JSON-LD data."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        script = soup.find(
            "script", {"type": "application/ld+json", "id": "seo-structured-schema"}
        )
        if not script:
            raise ValueError("JSON-LD script not found")

        # Parse JSON data
        data = json.loads(script.string)

        # Store base URL
        store_url = get_base_url(url)

        # Extract menu items
        menu_items = []

        if "hasMenu" in data:
            menu_sections = data["hasMenu"].get("hasMenuSection", [])

            # Handle nested structure
            for category in menu_sections:
                if isinstance(category, list):
                    category = category[0]

                section_name = category.get("name", "")
                menu_items_data = category.get("hasMenuItem", [])

                # Handle nested menu items
                for item_list in menu_items_data:
                    if isinstance(item_list, list):
                        item = item_list[0]
                    else:
                        item = item_list

                    menu_item = {
                        "name": item.get("name", ""),
                        "description": item.get("description", ""),
                        "price": item.get("offers", {}).get("price", 0),
                        "product_url": store_url,  # This will be updated later
                        "store_url": store_url,
                        "category": section_name,
                    }
                    menu_items.append(menu_item)

        # Update product URLs with product IDs
        menu_items = update_product_urls(menu_items, soup, store_url)

        return menu_items

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


if __name__ == "__main__":
    url = "https://www.rappi.com.ar/restaurantes/48-la-boheme-crepes-y-bagels"

    menu_items = extract_menu_items(url)

    # Save menu items to JSON file
    with open("menu_items.json", "w", encoding="utf-8") as f:
        json.dump(menu_items, f, ensure_ascii=False, indent=4)
