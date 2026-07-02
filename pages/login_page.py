from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')
        self.logo = page.locator(".login_logo")
        self.credentials_container = page.locator(
            '[data-test="login-credentials-container"]'
        )

    def goto(self):
        self.page.goto("/")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.text_content()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
