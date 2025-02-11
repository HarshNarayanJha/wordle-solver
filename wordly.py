import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from solver import WordleSolver

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service()
browser = webdriver.Chrome(service=service, options=chrome_options)

WORDLY = "https://wordly.org/"
browser.get(WORDLY)

wait = WebDriverWait(browser, 10)

rows = browser.find_elements(By.CLASS_NAME, "Row")

first_guess = "hello"
guess = first_guess

print("Starting in 3")
sleep(3)

solver = WordleSolver(6, 5)
solver.load_data()

for i in range(6):
    print(f"Attempt {i + 1} with {len(solver.possible_words)} possible words")

    guess = solver.sort_by_commonality(solver.possible_words)[0][0]

    for letter in guess:
        browser.find_element(By.TAG_NAME, "body").send_keys(letter)
    browser.find_element(By.TAG_NAME, "body").send_keys("\ue007")

    print(f"Trying {guess}")

    sleep(3.5)

    curr = rows[i]
    letters = curr.find_elements(By.CLASS_NAME, "Row-letter")
    states = [str(letter.get_attribute("class")).split()[-1] for letter in letters]

    result = ""
    pat = re.compile(r'letter-(elsewhere|absent|correct)')
    for s in states:
        if m := re.match(pat, s):
            match m.group(1):
                case "elsewhere":
                    result += "+"
                case "absent":
                    result += "-"
                case "correct":
                    result += "="

    print(f"Result: {result}")

    if result == "=" * solver.WORD_LENGTH:
        print(f'\nToday\'s Wordle Solution is: "{guess}", solved in {i + 1} guesses')
        browser.quit()
        break

    solver.update_possible_words(guess, result)
    sleep(1)
