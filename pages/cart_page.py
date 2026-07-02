from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('[data-test="title"]')
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.item_quantities = page.locator('[data-test="item-quantity"]')
        self.item_descriptions = page.locator('[data-test="inventory-item-desc"]')
        self.checkout_btn = page.locator('[data-test="checkout"]')
        self.continue_shopping_btn = page.locator('[data-test="continue-shopping"]')
        self.remove_btns = page.locator('[data-test^="remove-"]')

    def goto(self):
        self.page.goto("/cart.html")
        self.page.wait_for_load_state("networkidle")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self):
        return self.item_names.all_text_contents()

    def get_item_prices(self):
        return self.item_prices.all_text_contents()

    def get_item_quantities(self):
        return self.item_quantities.all_text_contents()

    def checkout(self):
        self.checkout_btn.click()
        self.page.wait_for_load_state("networkidle")

    def continue_shopping(self):
        self.continue_shopping_btn.click()
        self.page.wait_for_load_state("networkidle")

    def remove_item(self, item_id: str):
        self.page.locator(f'[data-test="remove-{item_id}"]').click()
        self.page.wait_for_timeout(300)
