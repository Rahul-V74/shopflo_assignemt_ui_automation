import json
import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def load_users():
    with open("data/users.json") as f:
        return json.load(f)


class TestLogin:
    users = load_users()

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.login_page = LoginPage(page)
        self.login_page.goto()

    def test_p_display_login_form(self):
        page = self.login_page
        expect(page.logo).to_have_text("Swag Labs")
        expect(page.username_input).to_be_visible()
        expect(page.password_input).to_be_visible()
        expect(page.login_button).to_be_visible()

    def test_p_display_login_credentials(self):
        expect(self.login_page.credentials_container).to_be_visible()

    def login_and_logout(self, user_key: str):
        user = self.users[user_key]
        self.login_page.login(user["username"], user["password"])
        expect(self.login_page.page).to_have_url(re.compile(r".*inventory\.html"))
        inventory_page = InventoryPage(self.login_page.page)
        inventory_page.logout()
        expect(self.login_page.username_input).to_be_visible()
        expect(self.login_page.password_input).to_be_visible()
        expect(self.login_page.login_button).to_be_visible()

    def test_p_login_standard_user(self):
        self.login_and_logout("validUser")

    def test_n_login_invalid_credentials(self):
        user = self.users["invalidUser"]
        self.login_page.login(user["username"], user["password"])
        error = self.login_page.get_error_message()
        assert "Username and password do not match" in error

    def test_n_login_empty_username(self):
        self.login_page.login("", self.users["validUser"]["password"])
        error = self.login_page.get_error_message()
        assert "Username is required" in error

    def test_n_login_empty_password(self):
        self.login_page.login(self.users["validUser"]["username"], "")
        error = self.login_page.get_error_message()
        assert "Password is required" in error

    def test_n_login_locked_out_user(self):
        user = self.users["lockedOutUser"]
        self.login_page.login(user["username"], user["password"])
        error = self.login_page.get_error_message()
        assert "locked out" in error

    def test_p_login_problem_user(self):
        self.login_and_logout("problemUser")

    def test_p_login_performance_glitch_user(self):
        self.login_and_logout("performanceGlitchUser")

    def test_p_login_error_user(self):
        self.login_and_logout("errorUser")

    def test_p_login_visual_user(self):
        self.login_and_logout("visualUser")
