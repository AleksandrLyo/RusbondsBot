import time
import asyncio
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

from app.bot import bot


async def sending_results(title, text, url):
    result = (f"<b>{title}</b>\n\n"
              f"{text}\n\n"
              f"<a href='{url}'>Подробнее</a>")
    await bot.send_message(-1002113327787, result, parse_mode="HTML", disable_web_page_preview=True)


async def full_search():
    options = FirefoxOptions()
    options.add_argument("--width=1280")
    options.add_argument("--height=720")
    options.set_preference("dom.webnotifications.enabled", False)
    browser = webdriver.Remote(command_executor='http://selenium:4444', options=options)
    browser.get("https://rusbonds.ru/news/")
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "banner-container").find_element(By.CLASS_NAME, "icon.close").click()
    time.sleep(2)
    title_check = ""
    while True:
        browser.find_element(By.CLASS_NAME, "news-wrapper").click()
        time.sleep(2)
        new = browser.find_element(By.CLASS_NAME, "news-content.news-view.sticky")
        title = new.find_element(By.TAG_NAME, "headline").text
        if title != title_check:
            title_check = title
            try:
                text = new.find_element(By.TAG_NAME, "p").text.split(" - ")
            except:
                text = new.find_element(By.TAG_NAME, "p").text.split(" – ")
            text.pop(0)
            text = ' '.join(text)
            url = new.find_element(By.TAG_NAME, "a").get_attribute("href")
            await sending_results(title, text, url)
        time.sleep(2)


if __name__ == "__main__":
    asyncio.run(full_search())
