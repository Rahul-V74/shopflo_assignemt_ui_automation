class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, path: str):
        self.page.goto(path)

    def wait_for_element(self, locator, timeout: int = 5000):
        locator.wait_for(state="visible", timeout=timeout)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url
