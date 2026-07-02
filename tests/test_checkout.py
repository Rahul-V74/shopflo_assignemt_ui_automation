import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from data.test_data import (
    EXPECTED_PRODUCTS,
    USER_STANDARD,
    CHECKOUT_INFO_TITLE,
    CHECKOUT_OVERVIEW_TITLE,
    ERR_FIRST_NAME,
    ERR_LAST_NAME,
    ERR_POSTAL_CODE,
    FIRST_NAME,
    LAST_NAME,
    POSTAL_CODE,
    PAYMENT_INFO,
    SHIPPING_INFO,
    SUBTOTAL,
    TAX,
    TOTAL,
    URL_CHECKOUT_STEP_TWO,
    URL_CHECKOUT_COMPLETE,
    URL_CART,
    URL_INVENTORY,
)
from utils.helpers import load_users


P = EXPECTED_PRODUCTS


class TestCheckout:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users[USER_STANDARD]["username"], self.users[USER_STANDARD]["password"])
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart(P[0]["item_id"])
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        cart_page.checkout()
        self.checkout_page = CheckoutPage(page)

    def test_p_display_checkout_page(self):
        expect(self.checkout_page.title).to_have_text(CHECKOUT_INFO_TITLE)

    def test_p_display_form_fields(self):
        expect(self.checkout_page.first_name_input).to_be_visible()
        expect(self.checkout_page.last_name_input).to_be_visible()
        expect(self.checkout_page.postal_code_input).to_be_visible()
        expect(self.checkout_page.continue_btn).to_be_visible()
        expect(self.checkout_page.cancel_btn).to_be_visible()

    def test_p_continue_checkout(self):
        self.checkout_page.fill_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        self.checkout_page.continue_checkout()
        expect(self.checkout_page.page).to_have_url(re.compile(URL_CHECKOUT_STEP_TWO))

    def test_p_cancel_to_cart(self):
        self.checkout_page.cancel()
        expect(self.checkout_page.page).to_have_url(re.compile(URL_CART))

    def test_n_error_empty_first_name(self):
        self.checkout_page.fill_details("", LAST_NAME, POSTAL_CODE)
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert ERR_FIRST_NAME in error

    def test_n_error_empty_last_name(self):
        self.checkout_page.fill_details(FIRST_NAME, "", POSTAL_CODE)
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert ERR_LAST_NAME in error

    def test_n_error_empty_postal_code(self):
        self.checkout_page.fill_details(FIRST_NAME, LAST_NAME, "")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert ERR_POSTAL_CODE in error

    def test_n_error_all_fields_empty(self):
        self.checkout_page.fill_details("", "", "")
        self.checkout_page.continue_checkout()
        error = self.checkout_page.get_error_message()
        assert ERR_FIRST_NAME in error


class TestCheckoutOverview:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users[USER_STANDARD]["username"], self.users[USER_STANDARD]["password"])
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart(P[1]["item_id"])
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        cart_page.checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.fill_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.continue_checkout()
        self.overview_page = CheckoutOverviewPage(page)

    def test_p_display_overview_page(self):
        expect(self.overview_page.title).to_have_text(CHECKOUT_OVERVIEW_TITLE)

    def test_p_display_item_in_summary(self):
        assert self.overview_page.get_item_count() == 1
        names = self.overview_page.get_item_names()
        assert P[1]["name"] in names

    def test_p_item_details_match_cart(self, page):
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(self.users[USER_STANDARD]["username"], self.users[USER_STANDARD]["password"])
        inventory = InventoryPage(page)
        inventory.reset_app_state()
        names = inventory.add_items_by_index([0, 1])
        inventory.go_to_cart()
        cart = CartPage(page)
        assert cart.get_item_names() == names
        cart.checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.fill_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.continue_checkout()
        overview = CheckoutOverviewPage(page)
        assert overview.get_item_names() == names

    def test_p_display_payment_info(self):
        expect(self.overview_page.payment_info_label).to_be_visible()
        expect(self.overview_page.payment_info_value).to_have_text(PAYMENT_INFO)

    def test_p_display_shipping_info(self):
        expect(self.overview_page.shipping_info_label).to_be_visible()
        expect(self.overview_page.shipping_info_value).to_have_text(SHIPPING_INFO)

    def test_p_display_price_total(self):
        subtotal = self.overview_page.get_subtotal()
        tax = self.overview_page.get_tax()
        total = self.overview_page.get_total()
        assert SUBTOTAL in subtotal
        assert TAX in tax
        assert TOTAL in total

    def test_p_finish_order(self):
        self.overview_page.finish()
        expect(self.overview_page.page).to_have_url(re.compile(URL_CHECKOUT_COMPLETE))

    def test_p_cancel_to_inventory(self):
        self.overview_page.cancel()
        expect(self.overview_page.page).to_have_url(re.compile(URL_INVENTORY))
