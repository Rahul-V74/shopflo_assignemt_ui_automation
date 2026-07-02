from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('[data-test="title"]')
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.item_quantities = page.locator('[data-test="item-quantity"]')
        self.item_descriptions = page.locator('[data-test="inventory-item-desc"]')
        self.payment_info_label = page.locator('[data-test="payment-info-label"]')
        self.payment_info_value = page.locator('[data-test="payment-info-value"]')
        self.shipping_info_label = page.locator('[data-test="shipping-info-label"]')
        self.shipping_info_value = page.locator('[data-test="shipping-info-value"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')

    def goto(self):
        self.page.goto("/checkout-step-two.html")
        self.page.wait_for_load_state("networkidle")

    def finish(self):
        self.finish_btn.click()
        self.page.wait_for_load_state("networkidle")

    def cancel(self):
        self.cancel_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self):
        return self.item_names.all_text_contents()

    def get_item_prices(self):
        return self.item_prices.all_text_contents()

    def get_item_quantities(self):
        return self.item_quantities.all_text_contents()

    def get_subtotal(self) -> str:
        return self.subtotal_label.text_content()

    def get_tax(self) -> str:
        return self.tax_label.text_content()

    def get_total(self) -> str:
        return self.total_label.text_content()
