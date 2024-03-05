import datetime
import time
import asyncio
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

from app.bot import bot
from core.config import settings


async def sending_result(title):
    result = (f"<b>{title}</b>")
    await bot.send_message(settings.chat_id, result, parse_mode="HTML")


async def sending_results(new_placements, changing_ratings, coupons, events):
    newline = "\n- "
    result = (f"<b>💰 Размещения:</b>\n"
              f"\n- {newline.join(new_placement for new_placement in new_placements)}\n\n"
              f"<b>📢 Рейтинги:</b>\n"
              f"\n- {newline.join(changing_rating for changing_rating in changing_ratings)}\n\n"
              f"<b>💲 Купоны:</b>\n"
              f"\n- {newline.join(coupon for coupon in coupons)}\n\n"
              f"<b>❓ События:</b>\n"
              f"\n- {newline.join(event for event in events)}\n\n"
              f"Ставьте лайк и подписывайтесь. Это мотивирует 😎"
            )
    await bot.send_message(settings.chat_id, result, parse_mode="HTML", disable_web_page_preview=True)


async def full_search():
    options = FirefoxOptions()
    options.add_argument("--width=1280")
    options.add_argument("--height=720")
    options.set_preference("dom.webnotifications.enabled", False)
    browser = webdriver.Remote(command_executor='http://selenium:4444', options=options)
    browser.get("https://rusbonds.ru/news/")
    time.sleep(2)
    try:
        browser.find_element(By.CLASS_NAME, "banner-container").find_element(By.CLASS_NAME, "icon.close").click()
    except:
        pass
    time.sleep(2)
    title_check = ""
    chk_pat_pass = '(?:ВТБ|RusBonds|События на рынке|ожидаются выплаты)'
    chk_pat_pass_1 = '(?:погашения)'
    chk_pat_pass_2 = '(?:облигаций)'
    chk_pat_1 = '(?:размест|размещ|зарегистрир|сбор|выпуск)'
    chk_pat_2 = '(?:рейтинг)'
    chk_pat_3 = '(?:купон)'
    new_placements = []
    changing_ratings = []
    coupons = []
    events = []
    while True:
        browser.find_element(By.CLASS_NAME, "news-wrapper").click()
        time.sleep(2)
        new = browser.find_element(By.CLASS_NAME, "news-content.news-view.sticky")
        title = new.find_element(By.TAG_NAME, "headline").text
        if bool(re.search(chk_pat_pass, title, flags=re.I)):
            pass
        elif bool(re.search(chk_pat_pass_1, title, flags=re.I)) and bool(re.search(chk_pat_pass_2, title, flags=re.I)):
            pass
        else: 
            if title != title_check:
                title_check = title
                if bool(re.search(chk_pat_1, title, flags=re.I)):
                    new_placements.append(title)
                elif bool(re.search(chk_pat_2, title, flags=re.I)):
                    changing_ratings.append(title)
                elif bool(re.search(chk_pat_3, title, flags=re.I)):
                    coupons.append(title)
                else:
                    events.append(title)
                await sending_result(title)
        if datetime.datetime.utcnow().time() > datetime.time(16,55,0) and datetime.datetime.utcnow().time() < datetime.time(16,55,2):
            await sending_results(new_placements, changing_ratings, coupons, events)
            new_placements = []
            changing_ratings = []
            coupons = []
            events = []
        time.sleep(2)


if __name__ == "__main__":
    asyncio.run(full_search())
