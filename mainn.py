import time
import asyncio
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

from app.bot import bot


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
    await bot.send_message(-1002113327787, result, parse_mode="HTML", disable_web_page_preview=True)


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
    browser.find_element(By.CLASS_NAME, "el-date-editor.date-input.el-input.el-input--mini.el-input--prefix.el-input--suffix.el-date-editor--date").click()
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "el-picker-panel__shortcut").click()
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "bg--red.t--white.rounded.btn").click()
    time.sleep(2)
    chk_pat_pass = '(?:ВТБ|RusBonds|События на рынке|ожидаются выплаты)'
    chk_pat_pass_1 = '(?:погашения)'
    chk_pat_pass_2 = '(?:облигаций)'
    new_placements = []
    chk_pat_1 = '(?:размест|размещ|зарегистрир|сбор|выпуск)'
    changing_ratings = []
    chk_pat_2 = '(?:рейтинг)'
    coupons = []
    chk_pat_3 = '(?:купон)'
    events = []
    news = browser.find_elements(By.CLASS_NAME, "news-title")
    for new in news:
        if bool(re.search(chk_pat_pass, new.text, flags=re.I)):
            pass
        elif bool(re.search(chk_pat_pass_1, new.text, flags=re.I)) and bool(re.search(chk_pat_pass_2, new.text, flags=re.I)):
            pass
        elif bool(re.search(chk_pat_1, new.text, flags=re.I)):
            new_placements.append(new.text)
        elif bool(re.search(chk_pat_2, new.text, flags=re.I)):
            changing_ratings.append(new.text)
        elif bool(re.search(chk_pat_3, new.text, flags=re.I)):
            coupons.append(new.text)
        else:
            events.append(new.text)
    await sending_results(new_placements, changing_ratings, coupons, events)
    browser.quit()


if __name__ == "__main__":
    asyncio.run(full_search())