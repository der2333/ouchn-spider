from playwright.sync_api import Page


def init_page(page: Page):
    page.add_init_script(
        """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
    )
