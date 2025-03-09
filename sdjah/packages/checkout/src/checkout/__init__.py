from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import logging
from cookies import create_cookies, create_storage
import time

# Basic logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class RappiCheckout:
    def __init__(self):
        """Initialize the RappiCheckout with browser and authentication."""
        # Start the browser immediately
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context(viewport={"width": 1280, "height": 720})
        self.page = self.context.new_page()
        self.page.goto("https://www.rappi.com.ar/")

        time.sleep(5)
        logging.info("Browser started")

        # Add authentication cookies immediately
        cookies = create_cookies()
        local_storage = create_storage()

        self.context.add_cookies(cookies)
        self.context.storage_state(path="storage_state.json")

        logging.info("Added authentication cookies")

    def add_to_cart(self, link):
        """
        Navigate to the product link and add the item to cart.

        Args:
            link (str): The URL of the product to add to cart

        Returns:
            bool: True if the item was successfully added to cart, False otherwise
        """
        try:
            # Navigate to the product link
            self.page.goto(link)
            logging.info(f"Navigated to product page: {link}")

            # Wait for the page to load
            self.page.wait_for_load_state("networkidle")

            time.sleep(5)

            # Find and click the "Add to cart" button
            button_selector = "#portal-root-container > div > div > div > div.sc-dnqmqq.qAAlT > div > button.chakra-button.css-1qhp8j2"
            self.page.wait_for_selector(button_selector, state="visible", timeout=10000)
            self.page.click(button_selector)
            logging.info("Clicked add to cart button")

            # Optional: Wait for some confirmation that the item was added
            # This could be a toast message or cart counter updating
            # self.page.wait_for_selector("some-confirmation-selector", timeout=5000)

            return True
        except Exception as e:
            logging.error(f"Failed to add item to cart: {e}")
            return False

    def navigate_to_checkout(self):
        """Navigate to the checkout page."""
        self.page.goto("https://www.rappi.com.ar/checkout/restaurant")
        logging.info("Navigated to checkout page")

        # Handle popup if it appears
        try:
            popup = self.page.wait_for_selector(
                "#chakra-modal--header-\\:Rdarq6\\: > button", timeout=5000
            )
            if popup:
                popup.click()
                logging.info("Closed popup")
        except Exception:
            logging.info("No popup detected or couldn't close it")

        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle")

    def select_tip_and_nullify(self):
        """Select the delivery option."""
        try:
            selector = "#__next > div.sc-eef0b166-0.jdRUhU > div > div.sc-eef0b166-2.keKrGQ > div.sc-47055ebf-0.huuGwh > div.sc-47055ebf-4.kYqEOc > div.sc-47055ebf-11.lcmsru > label:nth-child(8)"
            self.page.wait_for_selector(selector, state="visible", timeout=10000)
            self.page.click(selector)
            logging.info("Selected delivery option")
        except Exception as e:
            logging.error(f"Failed to select delivery option: {e}")
            return False

        try:
            selector = "#chakra-modal--body-\\:r0\\: > div > div.css-1j7pvyd > button.chakra-button.css-smujo5"
            self.page.wait_for_selector(selector, state="visible", timeout=10000)
            logging.info("Ready to confirm order")
        except Exception as e:
            logging.error(f"Failed to find confirmation button: {e}")
            return False

        return True

    def take_screenshot(self, filepath="rappi_checkout_screenshot.png"):
        """Take a screenshot of the current page."""
        self.page.screenshot(path=filepath, full_page=True)
        logging.info(f"Screenshot saved to {filepath}")

    def close(self):
        """Close the browser."""
        self.browser.close()
        self.playwright.stop()
        logging.info("Browser closed")


def main():
    """Run the Rappi checkout process."""
    checkout = RappiCheckout()
    try:
        checkout.add_to_cart(
            "https://www.rappi.com.ar/restaurantes/225445-fabric-sushi?productDetail=2113106137"
        )

        checkout.navigate_to_checkout()
        checkout.select_tip_and_nullify()

    except Exception as e:
        logging.error(f"Error during checkout process: {e}")
        try:
            checkout.take_screenshot("rappi_error.png")
        except Exception:
            pass
    finally:
        # Close browser
        checkout.close()


if __name__ == "__main__":
    main()


# def add_local_storage_to_context(page, local_storage_items):
#     """
#     Add local storage items to a Playwright page context.
#
#     Args:
#         page: The Playwright page object
#         local_storage_items: Dictionary of key-value pairs to add to local storage
#     """
#     # Convert the items to a JavaScript-compatible format
#     items_str = json.dumps(local_storage_items)
#
#     # Execute JavaScript to set localStorage items
#     page.evaluate(f"""
#         const items = {items_str};
#         for (const [key, value] of Object.entries(items)) {{
#             localStorage.setItem(key, value);
#         }}
#     """)
#
#     print(f"Added {len(local_storage_items)} items to local storage")
