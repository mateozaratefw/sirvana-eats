import json
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from scrape_product import scrape_product


def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def form_product_url(store_url, product_id):
    return f"{store_url}?productDetail={product_id}"


def process_file(file_path):
    try:
        data = read_json_file(file_path)
        urls = []
        for item in data:
            if isinstance(item, dict) and "store_url" in item and "product_id" in item:
                url = form_product_url(item["store_url"], item["product_id"])
                urls.append(url)
        return urls
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []


async def scrape_urls_concurrently(urls, output_filename, max_concurrent=5):
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for url in urls:
            task = loop.run_in_executor(executor, scrape_product, url, output_filename)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r is not None]


async def process_single_file(file_path):
    json_file = os.path.basename(file_path)
    print(f"\nProcessing file: {json_file}")

    # Create output filename based on input filename
    output_filename = f"scraped_{json_file}"

    urls = process_file(file_path)
    if urls:
        print(f"Found {len(urls)} products to scrape in {json_file}")
        results = await scrape_urls_concurrently(urls, output_filename)
        print(f"Successfully scraped {len(results)} products to {output_filename}")
    else:
        print(f"No valid URLs found in file {json_file}")


async def main():
    output_dir = "output"
    json_files = [
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.endswith(".json")
    ]

    # Create tasks for concurrent processing
    tasks = [process_single_file(file_path) for file_path in json_files]

    # Process files concurrently, limiting to 3 at a time
    chunk_size = 3
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i : i + chunk_size]
        await asyncio.gather(*chunk)


if __name__ == "__main__":
    asyncio.run(main())
