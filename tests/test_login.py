import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from data.test_data import (
    LOGIN_LOGO_TEXT,
    ERR_INVALID_CREDENTIALS,
    ERR_USERNAME_REQUIRED,
    ERR_PASSWORD_REQUIRED,
    ERR_LOCKED_OUT,
    USER_STANDARD,
    USER_LOCKED,
    USER_PROBLEM,
    USER_PERF_GLITCH,
    USER_ERROR,
    USER_VISUAL,
    USER_INVALID,
    URL_INVENTORY,
)
from utils.helpers import load_users


class TestLogin:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.login_page = LoginPage(page)
        self.login_page.goto()

    def test_p_display_login_form(self):
        page = self.login_page
        expect(page.logo).to_have_text(LOGIN_LOGO_TEXT)
        expect(page.username_input).to_be_visible()
        expect(page.password_input).to_be_visible()
        expect(page.login_button).to_be_visible()

    def test_p_display_login_credentials(self):
        expect(self.login_page.credentials_container).to_be_visible()

    def login_and_logout(self, user_key: str):
        user = self.users[user_key]
        self.login_page.login(user["username"], user["password"])
        expect(self.login_page.page).to_have_url(re.compile(URL_INVENTORY))
        inventory_page = InventoryPage(self.login_page.page)
        inventory_page.logout()
        expect(self.login_page.username_input).to_be_visible()
        expect(self.login_page.password_input).to_be_visible()
        expect(self.login_page.login_button).to_be_visible()

    def test_p_login_standard_user(self):
        self.login_and_logout(USER_STANDARD)

    def test_n_login_invalid_credentials(self):
        user = self.users[USER_INVALID]
        self.login_page.login(user["username"], user["password"])
        error = self.login_page.get_error_message()
        assert ERR_INVALID_CREDENTIALS in error

    def test_n_login_empty_username(self):
        self.login_page.login("", self.users[USER_STANDARD]["password"])
        error = self.login_page.get_error_message()
        assert ERR_USERNAME_REQUIRED in error

    def test_n_login_empty_password(self):
        self.login_page.login(self.users[USER_STANDARD]["username"], "")
        error = self.login_page.get_error_message()
        assert ERR_PASSWORD_REQUIRED in error

    def test_n_login_locked_out_user(self):
        user = self.users[USER_LOCKED]
        self.login_page.login(user["username"], user["password"])
        error = self.login_page.get_error_message()
        assert ERR_LOCKED_OUT in error

    def test_p_login_problem_user(self):
        self.login_and_logout(USER_PROBLEM)

    def test_p_login_performance_glitch_user(self):
        self.login_and_logout(USER_PERF_GLITCH)

    def test_p_login_error_user(self):
        self.login_and_logout(USER_ERROR)

    def test_p_login_visual_user(self):
        self.login_and_logout(USER_VISUAL)
