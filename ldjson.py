import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urlunsplit
from typing import Dict, List, Tuple
import multiprocessing
import os
from itertools import chain
from datetime import datetime


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


def find_product_images(soup: BeautifulSoup, product_name: str) -> List[str]:
    """Find product image URLs by searching for img tags with matching alt text."""
    images = []
    # Find all img tags with alt text containing the product name
    img_tags = soup.find_all(
        "img", alt=lambda x: x and product_name.lower() in x.lower()
    )

    # Add images with data-test attributes that might contain product images
    img_tags.extend(soup.find_all("img", attrs={"data-test-id": True}))

    for img in img_tags:
        src = img.get("src")
        if src and src.startswith("https://"):
            images.append(src)

    return images


def update_product_urls(
    menu_items: List[Dict], soup: BeautifulSoup, store_url: str
) -> List[Dict]:
    """Update product URLs and images with product IDs."""
    for item in menu_items:
        product_id = find_product_id(soup, item["name"])
        if product_id:
            item["product_url"] = f"{store_url}?productDetail={product_id}"

        # Find and add product images
        images = find_product_images(soup, item["name"])
        if images:
            item["images"] = images
    return menu_items


def extract_menu_items(url: str) -> Tuple[List[Dict], Dict]:
    """Extract menu items from Rappi's JSON-LD data."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    error_info = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "error_type": None,
        "error_message": None,
        "status_code": None,
    }

    try:
        response = requests.get(url, headers=headers)
        error_info["status_code"] = response.status_code

        if response.status_code != 200:
            error_info["error_type"] = "HTTP_ERROR"
            error_info["error_message"] = (
                f"HTTP {response.status_code}: {response.reason}"
            )
            return [], error_info

        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        script = soup.find(
            "script", {"type": "application/ld+json", "id": "seo-structured-schema"}
        )
        if not script:
            error_info["error_type"] = "PARSING_ERROR"
            error_info["error_message"] = "JSON-LD script not found"
            return [], error_info

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
        return menu_items, None

    except requests.RequestException as e:
        error_info["error_type"] = "REQUEST_ERROR"
        error_info["error_message"] = str(e)
        return [], error_info
    except json.JSONDecodeError as e:
        error_info["error_type"] = "JSON_ERROR"
        error_info["error_message"] = str(e)
        return [], error_info
    except Exception as e:
        error_info["error_type"] = "UNEXPECTED_ERROR"
        error_info["error_message"] = str(e)
        return [], error_info


def process_restaurant_chunk(chunk: List[Dict], process_id: int) -> Tuple[str, str]:
    """Process a chunk of restaurants and write results to a temporary file."""
    muerte_dir = "muerte"
    os.makedirs(muerte_dir, exist_ok=True)

    output_file = os.path.join(muerte_dir, f"muerte_items_temp_{process_id}.json")
    error_file = os.path.join(muerte_dir, f"muerte_errors_temp_{process_id}.json")

    results = []
    errors = []

    for restaurant in chunk:
        items, error = extract_menu_items(restaurant["url"])
        if error:
            error["restaurant_name"] = restaurant.get("name", "Unknown")
            errors.append(error)
        results.extend(items)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    with open(error_file, "w", encoding="utf-8") as f:
        json.dump(errors, f, ensure_ascii=False, indent=4)

    print(output_file)
    return output_file, error_file


def combine_temp_files(
    temp_files: List[str],
    error_files: List[str],
    output_file: str,
    error_output_file: str,
):
    """Combine all temporary files into the final output file."""
    all_items = []
    all_errors = []

    for temp_file, error_file in zip(temp_files, error_files):
        with open(temp_file, "r", encoding="utf-8") as f:
            items = json.load(f)
            all_items.extend(items)

        with open(error_file, "r", encoding="utf-8") as f:
            errors = json.load(f)
            all_errors.extend(errors)

        # Clean up temporary files
        os.remove(temp_file)
        os.remove(error_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=4)

    with open(error_output_file, "w", encoding="utf-8") as f:
        json.dump(all_errors, f, ensure_ascii=False, indent=4)

    # Print summary of errors
    error_count = len(all_errors)
    if error_count > 0:
        print(f"\nFound {error_count} errors while processing restaurants:")
        error_types = {}
        for error in all_errors:
            error_type = error["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        for error_type, count in error_types.items():
            print(f"- {error_type}: {count} occurrences")
        print(f"\nDetailed error log written to: {error_output_file}")


if __name__ == "__main__":
    # Create muerte directory if it doesn't exist
    muerte_dir = "muerte"
    os.makedirs(muerte_dir, exist_ok=True)

    # Read restaurants from JSON file
    with open("restaurants.json", "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    # Determine number of processes (use CPU count - 1 to leave one core free)
    num_processes = max(1, multiprocessing.cpu_count() - 1)

    # Split restaurants into chunks
    chunk_size = len(restaurants) // num_processes + (
        1 if len(restaurants) % num_processes else 0
    )
    chunks = [
        restaurants[i : i + chunk_size] for i in range(0, len(restaurants), chunk_size)
    ]

    # Create process pool and process chunks
    with multiprocessing.Pool(num_processes) as pool:
        # Process each chunk and get temporary file names
        results = pool.starmap(
            process_restaurant_chunk, [(chunk, i) for i, chunk in enumerate(chunks)]
        )

        # Separate temp files and error files
        temp_files, error_files = zip(*results)

    # Combine all temporary files into final output in muerte directory
    final_output = os.path.join(muerte_dir, "muerte_items.json")
    error_output = os.path.join(muerte_dir, "muerte_errors.json")
    combine_temp_files(temp_files, error_files, final_output, error_output)
