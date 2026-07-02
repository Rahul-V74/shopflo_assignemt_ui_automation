import json
import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def load_users():
    with open("data/users.json") as f:
        return json.load(f)


EXPECTED_PRODUCTS = [
    {"name": "Sauce Labs Backpack", "item_id": "sauce-labs-backpack"},
    {"name": "Sauce Labs Bike Light", "item_id": "sauce-labs-bike-light"},
    {"name": "Sauce Labs Bolt T-Shirt", "item_id": "sauce-labs-bolt-t-shirt"},
    {"name": "Sauce Labs Fleece Jacket", "item_id": "sauce-labs-fleece-jacket"},
    {"name": "Sauce Labs Onesie", "item_id": "sauce-labs-onesie"},
    {"name": "Test.allTheThings() T-Shirt (Red)", "item_id": "test.allthethings-t-shirt-red"},
]


class TestInventory:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        user = self.users["validUser"]
        login_page.login(user["username"], user["password"])
        self.inventory_page = InventoryPage(page)

    def test_display_inventory_page(self):
        page = self.inventory_page
        expect(page.title).to_have_text("Products")

    def test_display_six_products(self):
        expect(self.inventory_page.inventory_items).to_have_count(6)

    def test_display_all_product_names(self):
        names = self.inventory_page.get_product_names()
        expected_names = [p["name"] for p in EXPECTED_PRODUCTS]
        assert names == expected_names

    def test_add_item_to_cart_increases_badge_count(self):
        page = self.inventory_page
        assert page.get_cart_count() == 0
        page.add_item_to_cart("sauce-labs-backpack")
        assert page.get_cart_count() == 1

    def test_add_and_remove_item_from_cart(self):
        page = self.inventory_page
        page.add_item_to_cart("sauce-labs-backpack")
        assert page.get_cart_count() == 1
        page.remove_item_from_cart("sauce-labs-backpack")
        assert page.get_cart_count() == 0

    def test_add_multiple_items_increments_cart_count(self):
        page = self.inventory_page
        page.add_item_to_cart("sauce-labs-backpack")
        page.add_item_to_cart("sauce-labs-bike-light")
        page.add_item_to_cart("sauce-labs-bolt-t-shirt")
        assert page.get_cart_count() == 3

    def test_sort_by_name_z_to_a(self):
        page = self.inventory_page
        page.sort_by("za")
        names = page.get_product_names()
        expected = sorted([p["name"] for p in EXPECTED_PRODUCTS], reverse=True)
        assert names == expected

    def test_sort_by_price_low_to_high(self):
        page = self.inventory_page
        page.sort_by("lohi")
        prices = page.get_product_prices()
        price_values = [float(p.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values)

    def test_sort_by_price_high_to_low(self):
        page = self.inventory_page
        page.sort_by("hilo")
        prices = page.get_product_prices()
        price_values = [float(p.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values, reverse=True)

    def test_open_and_close_menu(self):
        page = self.inventory_page
        page.open_menu()
        assert page.is_menu_open()
        page.close_menu()

    def test_logout_redirects_to_login(self):
        self.inventory_page.logout()
        expect(self.inventory_page.page).to_have_url(re.compile(r".*\/$"))

    def test_reset_app_state_clears_cart(self):
        page = self.inventory_page
        page.add_item_to_cart("sauce-labs-backpack")
        page.add_item_to_cart("sauce-labs-bike-light")
        assert page.get_cart_count() == 2
        page.reset_app_state()
        assert page.get_cart_count() == 0

    def test_navigate_to_cart(self):
        self.inventory_page.go_to_cart()
        expect(self.inventory_page.page).to_have_url(re.compile(r".*cart\.html"))

    def test_sort_by_name_a_to_z(self):
        page = self.inventory_page
        page.sort_by("za")
        page.sort_by("az")
        names = page.get_product_names()
        expected = sorted([p["name"] for p in EXPECTED_PRODUCTS])
        assert names == expected

    def test_menu_displays_correct_items(self):
        page = self.inventory_page
        page.open_menu()
        expect(page.all_items_link).to_have_text("All Items")
        expect(page.about_link).to_have_text("About")
        expect(page.logout_link).to_have_text("Logout")
        expect(page.reset_link).to_have_text("Reset App State")

    def test_add_to_cart_button_changes_to_remove(self):
        page = self.inventory_page
        page.add_item_to_cart("sauce-labs-backpack")
        remove_btn = page.page.locator('[data-test="remove-sauce-labs-backpack"]')
        expect(remove_btn).to_be_visible()
        expect(remove_btn).to_have_text("Remove")

    def test_cart_page_shows_added_item_with_details(self):
        page = self.inventory_page
        page.add_item_to_cart("sauce-labs-backpack")
        page.go_to_cart()
        cart = CartPage(page.page)
        expect(cart.title).to_have_text("Your Cart")
        assert cart.get_item_count() == 1
        assert cart.get_item_names() == ["Sauce Labs Backpack"]
        assert cart.get_item_quantities() == ["1"]
        price = cart.get_item_prices()[0]
        assert float(price.replace("$", "")) > 0

    def test_cart_page_shows_all_added_items(self):
        page = self.inventory_page
        added = [
            ("sauce-labs-backpack", "Sauce Labs Backpack"),
            ("sauce-labs-bike-light", "Sauce Labs Bike Light"),
        ]
        for item_id, _ in added:
            page.add_item_to_cart(item_id)
        page.go_to_cart()
        cart = CartPage(page.page)
        assert cart.get_item_count() == len(added)
        expected_names = [name for _, name in added]
        assert cart.get_item_names() == expected_names
        assert cart.get_item_quantities() == ["1"] * len(added)
