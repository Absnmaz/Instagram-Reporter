import os
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pystyle import Colors, Colorate

# Config
REPORT_COUNT = 5
DELAY_BETWEEN_REPORTS = (5, 10)  # seconds


def load_config():
    if not os.path.exists("config.json"):
        raise FileNotFoundError("Missing config.json with Instagram credentials.")

    with open("config.json", "r") as f:
        return json.load(f)


def init_driver():
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--log-level=OFF")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)

    # Initialize normal Chrome WebDriver (make sure chromedriver is installed and in PATH)
    driver = webdriver.Chrome(options=options)
    return driver


def login_instagram(driver, wait, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    print(Colorate.Horizontal(Colors.green_to_white, "Logging into Instagram..."))

    try:
        cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Only allow essential cookies']")))
        cookies_button.click()
    except:
        pass  # Cookie banner might not show in some regions

    user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    user_input.clear()
    user_input.send_keys(username)

    pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    pass_input.clear()
    pass_input.send_keys(password)

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    # Optional: Skip "Save Your Login Info?" dialog
    try:
        not_now_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
        )
        not_now_btn.click()
    except:
        pass


def report_account(driver, wait, username_report):
    print(Colorate.Horizontal(Colors.red_to_white, f"Reporting user: {username_report}"))
    driver.get(f'https://www.instagram.com/{username_report}/')

    try:
        # Click the "More options" button (3 dots)
        more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'More options')]")))
        more_btn.click()

        report_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Report']")))
        report_btn.click()

        report_acc_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Report Account')]")))
        report_acc_btn.click()

        # Example: Select "It's pretending to be someone else"
        reason_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(), 'It’s pretending to be someone else')]")))
        reason_btn.click()

        me_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Me')]")))
        me_btn.click()

        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit report')]")))
        submit_btn.click()

        print(Colorate.Horizontal(Colors.green_to_white, "Report submitted."))
        time.sleep(random.uniform(*DELAY_BETWEEN_REPORTS))

    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f"Error reporting user: {e}"))


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Vertical(Colors.blue_to_white, "Instagram Auto Reporter (Educational Use Only)\n"))

    config = load_config()
    username = config.get("username")
    password = config.get("password")

    if not username or not password:
        print("Missing 'username' or 'password' in config.json")
        return

    username_report = input("Enter username to report: ")

    driver = init_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login_instagram(driver, wait, username, password)

        for i in range(REPORT_COUNT):
            print(f"\n[+] Report #{i + 1}")
            report_account(driver, wait, username_report)

        print(Colorate.Horizontal(Colors.green_to_white, "\nFinished all reports."))

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
