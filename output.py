from playwright.sync_api import Playwright, expect, sync_playwright


def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            timezone_id="America/Chicago", viewport={"width": 1980, "height": 1020}
        )
        page = context.new_page()
        page.goto("https://www.barchart.com/login")
        page.get_by_placeholder("Login with email").click()
        page.get_by_placeholder("Login with email").fill("username")
        page.get_by_placeholder("Login with email").press("Tab")
        page.get_by_placeholder("Password").fill("password")
        page.get_by_role("button", name="Log In").click()
        page.close()

        # ---------------------
        context.close()
        browser.close()
