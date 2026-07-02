import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from data.test_data import (
    EXPECTED_PRODUCTS,
    USER_STANDARD,
    INVENTORY_TITLE,
    CART_TITLE,
    MENU_ALL_ITEMS,
    MENU_ABOUT,
    MENU_LOGOUT,
    MENU_RESET,
    BTN_REMOVE,
    PRODUCT_COUNT,
    SORT_ZA,
    SORT_LOHI,
    SORT_HILO,
    SORT_AZ,
    URL_INVENTORY,
    URL_CART,
    URL_ROOT,
)
from utils.helpers import load_users


P = EXPECTED_PRODUCTS


class TestInventory:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        user = self.users[USER_STANDARD]
        login_page.login(user["username"], user["password"])
        self.inventory_page = InventoryPage(page)

    def test_p_display_inventory_page(self):
        expect(self.inventory_page.title).to_have_text(INVENTORY_TITLE)

    def test_p_display_six_products(self):
        expect(self.inventory_page.inventory_items).to_have_count(PRODUCT_COUNT)

    def test_p_display_all_product_names(self):
        names = self.inventory_page.get_product_names()
        expected_names = [p["name"] for p in P]
        assert names == expected_names

    def test_p_add_to_cart_badge(self):
        assert self.inventory_page.get_cart_count() == 0
        self.inventory_page.add_item_to_cart(P[0]["item_id"])
        assert self.inventory_page.get_cart_count() == 1

    def test_p_add_and_remove_from_cart(self):
        self.inventory_page.add_item_to_cart(P[0]["item_id"])
        assert self.inventory_page.get_cart_count() == 1
        self.inventory_page.remove_item_from_cart(P[0]["item_id"])
        assert self.inventory_page.get_cart_count() == 0

    def test_p_add_multiple_items(self):
        for i in range(3):
            self.inventory_page.add_item_to_cart(P[i]["item_id"])
        assert self.inventory_page.get_cart_count() == 3

    def test_p_sort_name_z_to_a(self):
        self.inventory_page.sort_by(SORT_ZA)
        names = self.inventory_page.get_product_names()
        expected = sorted([p["name"] for p in P], reverse=True)
        assert names == expected

    def test_p_sort_price_low_to_high(self):
        self.inventory_page.sort_by(SORT_LOHI)
        prices = self.inventory_page.get_product_prices()
        price_values = [float(p.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values)

    def test_p_sort_price_high_to_low(self):
        self.inventory_page.sort_by(SORT_HILO)
        prices = self.inventory_page.get_product_prices()
        price_values = [float(p.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values, reverse=True)

    def test_p_open_and_close_menu(self):
        self.inventory_page.open_menu()
        assert self.inventory_page.is_menu_open()
        self.inventory_page.close_menu()

    def test_p_logout(self):
        self.inventory_page.logout()
        expect(self.inventory_page.page).to_have_url(re.compile(URL_ROOT))

    def test_p_reset_app_state(self):
        for i in range(2):
            self.inventory_page.add_item_to_cart(P[i]["item_id"])
        assert self.inventory_page.get_cart_count() == 2
        self.inventory_page.reset_app_state()
        assert self.inventory_page.get_cart_count() == 0

    def test_p_navigate_to_cart(self):
        self.inventory_page.go_to_cart()
        expect(self.inventory_page.page).to_have_url(re.compile(URL_CART))

    def test_p_sort_name_a_to_z(self):
        self.inventory_page.sort_by(SORT_ZA)
        self.inventory_page.sort_by(SORT_AZ)
        names = self.inventory_page.get_product_names()
        expected = sorted([p["name"] for p in P])
        assert names == expected

    def test_p_menu_items(self):
        self.inventory_page.open_menu()
        expect(self.inventory_page.all_items_link).to_have_text(MENU_ALL_ITEMS)
        expect(self.inventory_page.about_link).to_have_text(MENU_ABOUT)
        expect(self.inventory_page.logout_link).to_have_text(MENU_LOGOUT)
        expect(self.inventory_page.reset_link).to_have_text(MENU_RESET)

    def test_p_add_to_cart_button_changes(self):
        self.inventory_page.add_item_to_cart(P[0]["item_id"])
        remove_btn = self.inventory_page.page.locator(
            f'[data-test="remove-{P[0]["item_id"]}"]'
        )
        expect(remove_btn).to_be_visible()
        expect(remove_btn).to_have_text(BTN_REMOVE)

    def test_p_cart_item_details(self):
        self.inventory_page.add_item_to_cart(P[0]["item_id"])
        self.inventory_page.go_to_cart()
        cart = CartPage(self.inventory_page.page)
        expect(cart.title).to_have_text(CART_TITLE)
        assert cart.get_item_count() == 1
        assert cart.get_item_names() == [P[0]["name"]]
        assert cart.get_item_quantities() == ["1"]
        price = cart.get_item_prices()[0]
        assert float(price.replace("$", "")) > 0

    def test_p_cart_shows_all_added(self):
        items = P[:2]
        for item in items:
            self.inventory_page.add_item_to_cart(item["item_id"])
        self.inventory_page.go_to_cart()
        cart = CartPage(self.inventory_page.page)
        assert cart.get_item_count() == len(items)
        assert cart.get_item_names() == [item["name"] for item in items]
        assert cart.get_item_quantities() == ["1"] * len(items)
