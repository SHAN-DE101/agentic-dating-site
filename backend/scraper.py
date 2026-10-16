import asyncio
from playwright.async_api import async_playwright

async def scrape_linkedin(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            title = await page.title()
            text_content = await page.inner_text("body")
        except Exception as e:
            title = "profile"
            text_content = f"sample profile text for {url}: {str(e)}"
        finally:
            await browser.close()
        return {"raw_text": text_content[:4000], "title": title}

async def scrape_instagram(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            text_content = await page.inner_text("body")
        except Exception as e:
            text_content = f"sample bio and posts for {url}: {str(e)}"
        finally:
            await browser.close()
        return {"raw_text": text_content[:4000]}
