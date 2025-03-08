import datetime
import json
import os
import fcntl
from typing import List, Dict, Optional, Union
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import asyncio

# Initial dummy cookie string - replace this with your actual initial cookies
INITIAL_COOKIES = """
rappi.acceptedCookies	1	.www.rappi.com.ar	/	2026-03-07T16:51:25.249Z	22			Lax			Medium	
rappi.data	eyJpZCI6NDk4NzQ2MjE0LCJmaXJzdE5hbWUiOiJNYXRlbyIsImxhc3ROYW1lIjoiWmFyYXRlIiwiZ2VuZGVyIjoiIiwiaWRlbnRpZmljYXRpb25UeXBlIjowLCJpZGVudGlmaWNhdGlvbiI6IiIsImVtYWlsIjoibWF0ZW96YXJhdGVmd0BnbWFpbC5jb20iLCJkZWZhdWx0Q2MiOm51bGwsImxhc3RQdXNoQ3VzdG9tIjpudWxsLCJiaXJ0aGRheSI6bnVsbCwicmVwbGFjZW1lbnRDcml0ZXJpYUlkIjpudWxsLCJyZWZlcmVkQ29kZSI6bnVsbCwicGhvbmUiOiIzNDM1MTM1MTY5IiwicmVtZW1iZXJUb2tlbiI6bnVsbCwiaXNQaG9uZUNvbmZpcm1lZCI6dHJ1ZSwiY2NCbG9ja2VkIjpmYWxzZSwiZGV2aWNlSWQiOiIyMDFjMjFkNS0zZDVmLTRmNGUtOWI5MS1mMjliYTkyODc2ZWUiLCJibG9ja2VkIjpmYWxzZSwiZXhpdG9JZCI6bnVsbCwiZXhpdG9Mb3lhbHR5VHlwZSI6bnVsbCwiYXBwbGljYXRpb24iOiJyYXBwaSIsInZpcCI6ZmFsc2UsInBheXBhbEJsb2NrZWQiOmZhbHNlLCJzdGF0dXNGcmF1ZCI6Im5vdF92ZXJpZmllZCIsImluc3RhbGxtZW50cyI6MSwiY291bnRyeUNvZGUiOiIrNTQiLCJzb2NpYWxQcm92aWRlciI6Imdvb2dsZSIsIm5hbWUiOiJNYXRlbyBaYXJhdGUiLCJwaWMiOiIiLCJyYXBwaUNyZWRpdHMiOiIwIiwicmFwcGlDcmVkaXRBY3RpdmUiOmZhbHNlLCJnbXYiOjAsImNyZWF0ZWRBdCI6IjIwMjQtMDItMTEgMTI6NDc6MDgiLCJhY3RpdmVBZGRyZXNzIjpudWxsLCJsb3lhbHR5Ijp7ImlkIjotMSwibmFtZSI…	.rappi.com.ar	/	2026-03-08T17:09:17.000Z	1626			Lax			Medium	
rappi.id	eyJhY2Nlc3NfdG9rZW4iOiJmdC5nQUFBQUFCbnpIbTdkTnZCazFKRUVJbTYwTHo5LXZZUzhwSHAwZmlVTlFHa0duX3c1dVJ2Tk4wNzcyV3hwVjA4OGhqcWlGMkllYUtObVNvZ2x4aWN0bUhMOUIwWHp3LS0tdjdKRW44RFRQZnV4eVZsUy02MWh3MjhBLVhmTDlmemJSQjFXaUlfUkRYZGh3cGFDZHBUbTN0UDJsTFF6ZUNScG1Yb015bU84THEycHVYZGw3WXAwUGhOQW1TSjBIVmFJSWlxVjlTUlZTNzdRN2JlazZ6VkprMWdpV0NoOXRXSGJvYXIyQ1hNMWY3ZDNNbzIxemFXOEpOQUxBZUo0M2Ixc20yd2RvSXFlbXZtWUdBa0dCdXVWb0RTTDFPalV0ai1HalRrejk4SmEyaloxTDJmNmF2bXZmN2p0bC1hYUY3WHNESDhXckV2cjNiclNpZlFlVUUtQWRlZE1LekVNaTAwZ2VnNEJtQVVEelQ3bmZSdk12enBldG1HcFpGS3p3TFVYTWZNb1pjWEdveTh1YlgybmhxZk93SUFrMmpMUk9jZS13PT0iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiZXhwaXJlc19pbiI6NjA0ODAwLCJyZWZyZXNoX3Rva2VuIjoiZnQuZ0FBQUFBQm56SG03b0x1TGR3MHJzcTFMVEIxZWRxXzdGOXNXOHBKcXFGMVFtOC0tbG03bTkwWTcxYy1HdVpGSGJBcXdtUDFnME0tZDBwWFFXOG5Ga0Y0eldMSk1RTXJTQ1RXeFNwTHF0Z0Y5R24ySVl3WUtDWHl1eTBPLVkxc1d2bUwyNURoN25KRDhRZmtZNjdBdm9LNjM0c1ZHX0xRTXJOY3ctZ1NVQThLME11eFRPc00xZ2RTaEdrNnpPLWFkZ1diSG5UVjdZSmEtcDlnc3FoSjJnT25uQ21lYWZQMDExYUFBTGkzVk50eFlwVURQY01raXJ…	.rappi.com.ar	/	2025-06-07T23:09:25.485Z	1272			Lax			Medium	
rappi.type	1	.rappi.com.ar	/	2025-06-07T23:09:25.485Z	11			Lax			Medium	
rappi_refresh_token	ZnQuZ0FBQUFBQm56SG03b0x1TGR3MHJzcTFMVEIxZWRxXzdGOXNXOHBKcXFGMVFtOC0tbG03bTkwWTcxYy1HdVpGSGJBcXdtUDFnME0tZDBwWFFXOG5Ga0Y0eldMSk1RTXJTQ1RXeFNwTHF0Z0Y5R24ySVl3WUtDWHl1eTBPLVkxc1d2bUwyNURoN25KRDhRZmtZNjdBdm9LNjM0c1ZHX0xRTXJOY3ctZ1NVQThLME11eFRPc00xZ2RTaEdrNnpPLWFkZ1diSG5UVjdZSmEtcDlnc3FoSjJnT25uQ21lYWZQMDExYUFBTGkzVk50eFlwVURQY01raXJaX2F0bmFHQkdKZDkza1dsa3o5NFdkVFQyX3dXb0l6aGVNT1M4cXhwVmcwTVFtdkZOUzlRcjkyVWNZb3E3cm5reUpnWUcxYlphaDhzUnhEeWZZMDNDSGxpSlZnd2xqTVljVDdHVjFnRTlQcFVFRFVWeW5xcmNvMDNRYlktbXFET1p2VFA0RlJyYlB6M3puTVdJdDhXOWQ4R1ZXNm9NTHk5LXhpRW9Ed2lkRlRNQT09	.rappi.com.ar	/	2025-06-07T23:09:25.485Z	583			Lax			Medium	
"""


def parse_expires(expires_str: str) -> Optional[int]:
    """
    Convert the 'Expires' column (e.g. 2025-08-28T22:59:56.694Z) to an int UNIX timestamp.
    If 'Expires' is 'Session', return None (session cookie with no explicit expiry).

    Args:
        expires_str: The expiration date string from the cookie

    Returns:
        Optional[int]: Unix timestamp or None for session cookies
    """
    expires_str = expires_str.strip()
    if expires_str.lower() == "session" or not expires_str:
        return None
    # Remove trailing 'Z' and parse
    iso_str = expires_str.replace("Z", "+00:00")
    dt = datetime.datetime.fromisoformat(iso_str)
    return int(dt.timestamp())


def parse_samesite(samesite_str: str) -> Optional[str]:
    """
    Parse the SameSite attribute of a cookie.

    Args:
        samesite_str: The SameSite value from the cookie string

    Returns:
        Optional[str]: 'Lax', 'Strict', 'None', or None if invalid
    """
    val = samesite_str.strip().capitalize()
    if val in ["Lax", "Strict", "None"]:
        return val
    return None


def parse_checkmark(value_str: str) -> bool:
    """
    Convert checkmark symbol to boolean.

    Args:
        value_str: String containing checkmark or empty

    Returns:
        bool: True if checkmark present, False otherwise
    """
    return "✓" in value_str


def parse_cookie_line(line: str) -> Optional[Dict[str, Union[str, bool, int]]]:
    """
    Parse a single line from a cookie string into a dictionary format compatible with Playwright.

    Args:
        line: Tab-separated cookie string line

    Returns:
        Optional[Dict]: Cookie dictionary or None if parsing fails
    """
    parts = line.split("\t")
    if len(parts) < 9:
        return None

    name = parts[0].strip()
    value = parts[1].strip()
    domain = parts[2].strip()
    path = parts[3].strip()
    expires_raw = parts[4].strip()
    httpOnly_raw = parts[6]
    secure_raw = parts[7]
    sameSite_raw = parts[8]

    cookie = {
        "name": name,
        "value": value,
        "domain": domain,
        "path": path,
    }

    expires_ts = parse_expires(expires_raw)
    if expires_ts is not None:
        cookie["expires"] = expires_ts

    cookie["httpOnly"] = parse_checkmark(httpOnly_raw)
    cookie["secure"] = parse_checkmark(secure_raw)
    samesite_val = parse_samesite(sameSite_raw)
    if samesite_val:
        cookie["sameSite"] = samesite_val

    return cookie


async def setup_browser_with_cookies(
    cookie_string: str, headless: bool = True
) -> tuple[Browser, BrowserContext]:
    """
    Create a new browser and context with the provided cookies.

    Args:
        cookie_string: Multi-line string containing tab-separated cookie data
        headless: Whether to run browser in headless mode (default: True)

    Returns:
        tuple[Browser, BrowserContext]: Configured browser and context objects

    Example:
        cookie_string = '''
        name    value   domain  path    expires httpOnly    secure  sameSite
        cookie1 value1  .example.com    /   2025-08-28T22:59:56.694Z    ✓   ✓   Lax
        '''
        browser, context = setup_browser_with_cookies(cookie_string)
    """
    # Parse cookies from string
    cookies: List[Dict] = []
    lines = cookie_string.strip().splitlines()

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        parsed = parse_cookie_line(ln)
        if parsed:
            cookies.append(parsed)

    # Create browser and context
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=headless)
    context = await browser.new_context()

    # Add cookies to context
    if cookies:
        await context.add_cookies(cookies)

    return browser, context


async def create_context_with_cookies(
    cookie_string: str, browser: Browser
) -> BrowserContext:
    """
    Create a new context with the provided cookies using an existing browser instance.

    Args:
        cookie_string: Multi-line string containing tab-separated cookie data
        browser: Existing browser instance

    Returns:
        BrowserContext: New context with cookies configured
    """
    # Parse cookies from string
    cookies: List[Dict] = []
    lines = cookie_string.strip().splitlines()

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        parsed = parse_cookie_line(ln)
        if parsed:
            cookies.append(parsed)

    # Create new context
    context = await browser.new_context()

    # Add cookies to context
    if cookies:
        await context.add_cookies(cookies)

    return context


async def process_category(
    context: BrowserContext, category_index: int, total_categories: int
):
    """
    Process a single category in its own page and append restaurants to a JSON file.
    """
    page = await context.new_page()
    await page.goto("https://www.rappi.com.ar/restaurantes")
    # await page.wait_for_load_state("networkidle")

    # Get all category buttons
    buttons = page.locator('button[data-qa="category-item"]')
    current_button = buttons.nth(category_index)

    # Click the button
    await current_button.click()
    await asyncio.sleep(2)

    # Scrape restaurants
    restaurants = page.locator('a[data-qa^="store-item-restaurant"]')
    processed_urls = set()
    current_count = await restaurants.count()

    print(
        f"\nScraping restaurants for category {category_index + 1}/{total_categories}"
    )

    for j in range(current_count):
        restaurant = restaurants.nth(j)
        link = await restaurant.get_attribute("href")

        if link in processed_urls:
            continue

        processed_urls.add(link)

        name = await restaurant.locator("h3").text_content()
        delivery_time = await restaurant.locator(
            'span[class*="jeSkjq"]'
        ).first.text_content()
        delivery_price = await restaurant.locator(
            'span[data-testid="store-delivery-cost"]'
        ).text_content()

        restaurant_info = {
            "name": name,
            "delivery_time": delivery_time,
            "delivery_price": delivery_price,
            "url": "https://www.rappi.com.ar" + link,
            "category_index": category_index + 1,
        }

        # Append to JSON file with file locking for concurrent safety
        filename = "restaurants.json"
        try:
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    json.dump([], f)

            with open(filename, "r+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    data = json.load(f)
                    data.append(restaurant_info)
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            print(f"Error saving restaurant data: {e}")

        print(restaurant_info)

    await page.close()


if __name__ == "__main__":

    async def main():
        async with async_playwright() as p:
            # Start with initial cookies
            browser, context = await setup_browser_with_cookies(
                INITIAL_COOKIES, headless=False
            )
            page = await context.new_page()

            await page.goto("https://www.rappi.com.ar")
            print("\nStarted with initial cookies. Please log in if needed.")
            print("Once you're done, press Enter to continue...")
            input()  # Wait for user to press Enter

            cookies = await context.cookies()
            await browser.close()

            # Create new browser and context with updated cookies
            browser1 = await p.chromium.launch(headless=False)
            context1 = await browser1.new_context()
            await context1.add_cookies(cookies)

            # Rest of the code remains the same
            temp_page = await context1.new_page()
            await temp_page.goto("https://www.rappi.com.ar/restaurantes")
            await temp_page.wait_for_load_state("networkidle")
            buttons = temp_page.locator('button[data-qa="category-item"]')
            button_count = await buttons.count()
            await temp_page.close()

            # Process all categories concurrently
            tasks = []
            for i in range(button_count):
                task = asyncio.create_task(process_category(context1, i, button_count))
                tasks.append(task)

            # Wait for all tasks to complete
            await asyncio.gather(*tasks)
            await browser1.close()

    # Run the async main function
    asyncio.run(main())
