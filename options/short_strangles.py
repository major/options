#!/usr/bin/env python
import os

from playwright.sync_api import Playwright, sync_playwright

USERNAME = os.environ.get("BC_USERNAME")
PASSWORD = os.environ.get("BC_PASSWORD")
SCREENER_ID = os.environ.get("BC_SCREENER_ID")


def run(playwright: Playwright) -> None:
    """Get a list of short strangles from barchart."""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        timezone_id="America/Chicago", viewport={"width": 1980, "height": 1020}
    )
    page = context.new_page()
    page.goto("https://www.barchart.com/")
    page.get_by_label("Log in").click()
    page.get_by_placeholder("Login with email").click()
    page.get_by_placeholder("Login with email").fill(USERNAME)
    page.get_by_placeholder("Login with email").press("Tab")
    page.get_by_placeholder("Password").fill(PASSWORD)
    page.get_by_role("button", name="Log In").click()
    page.goto(
        "https://www.barchart.com/options/short-strangle?"
        f"orderBy=percentOfStock&orderDir=desc&viewName=main&screener={SCREENER_ID}"
    )
    with page.expect_download() as download_info:
        page.get_by_title("Download page to .csv file").click()
    download = download_info.value
    download.save_as("short_strangles.csv")
    page.close()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
    run(playwright)
