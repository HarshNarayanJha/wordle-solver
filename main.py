from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service()
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get("https://www.nytimes.com/games/wordle/index.html")

wait = WebDriverWait(browser, 10)

try:
    agree_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "purr-blocker-card__button")))
    agree_button.click()
except TimeoutException:
    print("Agree button not there, passing")
    pass

play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="Play"]')))
play_button.click()

_modal_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")))
_modal_close.click()

board = browser.find_element(By.CLASS_NAME, "Board-module_board__jeoPS")

rows = browser.find_elements(By.CLASS_NAME, "Row-module_row__pwpBq")

first_guess = "hello"
guess = first_guess

print("Starting in 3")
sleep(3)

for i in range(6):
    for letter in guess:
        browser.find_element(By.TAG_NAME, "body").send_keys(letter)
    browser.find_element(By.TAG_NAME, "body").send_keys("\ue007")

    sleep(5)

    curr = rows[i]

    letters = curr.find_elements(By.CLASS_NAME, "Tile-module_tile__UWEHN")
    states = [letter.get_attribute("data-state") for letter in letters]

    result = []
    for s in states:
        match s:
            case "present":
                result.append("+")
            case "absent":
                result.append("-")
            case "correct":
                result.append("=")

    print(result, states)

    sleep(3)
