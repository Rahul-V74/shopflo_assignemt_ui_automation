from pages.base_page import BasePage
from playwright.sync_api import expect


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('[data-test="title"]')
        self.inventory_items = page.locator('[data-test="inventory-item"]')
        self.inventory_list = page.locator('[data-test="inventory-list"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.burger_menu_btn = page.locator("#react-burger-menu-btn")
        self.close_menu_btn = page.locator("#react-burger-cross-btn")
        self.sidebar_menu = page.locator(".bm-menu-wrap")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')
        self.reset_link = page.locator('[data-test="reset-sidebar-link"]')
        self.about_link = page.locator('[data-test="about-sidebar-link"]')
        self.all_items_link = page.locator('[data-test="inventory-sidebar-link"]')

    def get_product_names(self):
        return self.page.locator('[data-test="inventory-item-name"]').all_text_contents()

    def get_product_prices(self):
        return self.page.locator('[data-test="inventory-item-price"]').all_text_contents()

    def get_product_descriptions(self):
        return self.page.locator('[data-test="inventory-item-desc"]').all_text_contents()

    def add_item_to_cart(self, item_id: str):
        add_btn = self.page.locator(f'[data-test="add-to-cart-{item_id}"]')
        remove_btn = self.page.locator(f'[data-test="remove-{item_id}"]')
        add_btn.click()
        expect(remove_btn).to_be_visible()

    def remove_item_from_cart(self, item_id: str):
        remove_btn = self.page.locator(f'[data-test="remove-{item_id}"]')
        add_btn = self.page.locator(f'[data-test="add-to-cart-{item_id}"]')
        remove_btn.click()
        expect(add_btn).to_be_visible()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def sort_by(self, value: str):
        self.sort_dropdown.select_option(value)
        expect(self.sort_dropdown).to_have_value(value)

    def open_menu(self):
        self.burger_menu_btn.click()
        expect(self.sidebar_menu).to_have_attribute("aria-hidden", "false")

    def close_menu(self):
        self.close_menu_btn.click()
        expect(self.sidebar_menu).to_have_attribute("aria-hidden", "true")

    def is_menu_open(self) -> bool:
        return self.sidebar_menu.get_attribute("aria-hidden") == "false"

    def logout(self):
        self.open_menu()
        self.logout_link.click()
        self.page.wait_for_load_state("networkidle")

    def reset_app_state(self):
        self.open_menu()
        self.reset_link.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.cart_badge).to_have_count(0)

    def go_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

    def get_item_image(self, item_id: str):
        return self.page.locator(f'[data-test="item-{item_id}-img-link"] img')

    def _name_to_item_id(self, name: str) -> str:
        return name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("'", "")

    def add_items_by_index(self, indices: list[int]) -> list[str]:
        names = []
        for i in indices:
            name = self.get_product_names()[i]
            names.append(name)
            item_id = self._name_to_item_id(name)
            self.add_item_to_cart(item_id)
        return names
