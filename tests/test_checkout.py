import json
import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def load_users():
    with open("data/users.json") as f:
        return json.load(f)


class TestCheckout:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users["validUser"]["username"], self.users["validUser"]["password"])
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        cart_page.checkout()
        self.checkout_page = CheckoutPage(page)

    def test_p_display_checkout_page(self):
        expect(self.checkout_page.title).to_have_text("Checkout: Your Information")

    def test_p_display_form_fields(self):
        page = self.checkout_page
        expect(page.first_name_input).to_be_visible()
        expect(page.last_name_input).to_be_visible()
        expect(page.postal_code_input).to_be_visible()
        expect(page.continue_btn).to_be_visible()
        expect(page.cancel_btn).to_be_visible()

    def test_p_continue_checkout(self):
        self.checkout_page.fill_details("John", "Doe", "12345")
        self.checkout_page.continue_checkout()
        expect(self.checkout_page.page).to_have_url(re.compile(r".*checkout-step-two\.html"))

    def test_p_cancel_to_cart(self):
        self.checkout_page.cancel()
        expect(self.checkout_page.page).to_have_url(re.compile(r".*cart\.html"))

    def test_n_error_empty_first_name(self):
        self.checkout_page.fill_details("", "Doe", "12345")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert "First Name" in error

    def test_n_error_empty_last_name(self):
        self.checkout_page.fill_details("John", "", "12345")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert "Last Name" in error

    def test_n_error_empty_postal_code(self):
        self.checkout_page.fill_details("John", "Doe", "")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert "Postal Code" in error

    def test_n_error_all_fields_empty(self):
        self.checkout_page.fill_details("", "", "")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert "First Name" in error


class TestCheckoutOverview:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users["validUser"]["username"], self.users["validUser"]["password"])
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart("sauce-labs-bike-light")
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        cart_page.checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.fill_details("John", "Doe", "12345")
        checkout_page.continue_checkout()
        self.overview_page = CheckoutOverviewPage(page)

    def test_p_display_overview_page(self):
        expect(self.overview_page.title).to_have_text("Checkout: Overview")

    def test_p_display_item_in_summary(self):
        assert self.overview_page.get_item_count() == 1
        names = self.overview_page.get_item_names()
        assert "Sauce Labs Bike Light" in names

    def test_p_item_details_match_cart(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users["validUser"]["username"], self.users["validUser"]["password"])
        inventory = InventoryPage(page)
        inventory.reset_app_state()
        names = inventory.add_items_by_index([0, 1])
        inventory.go_to_cart()
        cart = CartPage(page)
        assert cart.get_item_names() == names
        cart.checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.fill_details("John", "Doe", "12345")
        checkout_page.continue_checkout()
        overview = CheckoutOverviewPage(page)
        assert overview.get_item_names() == names

    def test_p_display_payment_info(self):
        expect(self.overview_page.payment_info_label).to_be_visible()
        expect(self.overview_page.payment_info_value).to_have_text("SauceCard #31337")

    def test_p_display_shipping_info(self):
        expect(self.overview_page.shipping_info_label).to_be_visible()
        expect(self.overview_page.shipping_info_value).to_have_text("Free Pony Express Delivery!")

    def test_p_display_price_total(self):
        subtotal = self.overview_page.get_subtotal()
        tax = self.overview_page.get_tax()
        total = self.overview_page.get_total()
        assert "9.99" in subtotal
        assert "0.80" in tax
        assert "10.79" in total

    def test_p_finish_order(self):
        self.overview_page.finish()
        expect(self.overview_page.page).to_have_url(re.compile(r".*checkout-complete\.html"))

    def test_p_cancel_to_inventory(self):
        self.overview_page.cancel()
        expect(self.overview_page.page).to_have_url(re.compile(r".*inventory\.html"))
