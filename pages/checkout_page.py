from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('[data-test="title"]')
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def goto(self):
        self.page.goto("/checkout-step-one.html")
        self.page.wait_for_load_state("networkidle")

    def fill_details(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_checkout(self):
        self.continue_btn.click()
        self.page.wait_for_load_state("networkidle")

    def cancel(self):
        self.cancel_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.text_content()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
