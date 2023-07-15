from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import pyautogui
from platform import system


def setup():
    global driver
    global action_chain
    global debugging_url
    global sys

    sys = system()

    debugging_url = "about:debugging#/runtime/this-firefox"

    # create firefox instance
    driver = webdriver.Firefox()
    driver.maximize_window()
    # create actionChain
    action_chain = ActionChains(driver)
    # install project as add-on
    install_temporary_addon(Path.cwd().joinpath('src'))


def tear_down():
    global driver
    driver.quit()


def install_temporary_addon(addon_path):
    global driver
    # install temporary add-on
    driver.install_addon(str(addon_path), temporary=True)


def decide_whether_to_show_debugging_page_or_not():
    global driver
    global action_chain
    global debugging_url

    try:
        with open('skip-about-debugging-page.txt', 'r') as file:
            skip_debugging_page = file.read()
    except FileNotFoundError as e:
        with open('skip-about-debugging-page.txt', 'x') as file:
            file.write('true')
            driver.get(debugging_url)
            action_chain.pause(5).perform()


# This test navigates to the dwds website, selects text and clicks the context menu entry for redirection to dwds again,
# but with a search term provided.
def select_text_and_click_context_menu_entry():
    global driver
    global action_chain
    url = "https://www.dwds.de"

    decide_whether_to_show_debugging_page_or_not()

    driver.get(url)
    claim = driver.find_element(By.ID, "navbar").find_element(By.CLASS_NAME, "dwds-claim")

    x = driver.get_window_position().get('x')
    y = driver.get_window_position().get('y')
    print("\tWindow upper left position: ({0}, {1})".format(x, y))

    # select text and open context menu
    action_chain.move_to_element(claim)\
        .click_and_hold()\
        .move_by_offset(10, 0)\
        .release()\
        .context_click()\
        .perform()

    action_chain.pause(1).perform()

    # move mouse caret to last element in context menu (dwds search) and click the entry
    sys = system()
    if sys == 'Windows':
        pyautogui.moveTo(x + 450, y + 360, duration=1)
    else:
        pyautogui.moveTo(x + 450, y + 310, duration=1)
    pyautogui.leftClick()

    action_chain.pause(2).perform()


def focus_address_bar_and_search_with_omnibox_api():
    global driver
    global action_chain

    decide_whether_to_show_debugging_page_or_not()

    x = driver.get_window_position().get('x')
    y = driver.get_window_position().get('y')

    # move mouse caret to last element in context menu (dwds search) and click the entry
    pyautogui.moveTo(x + 350, y + 65, duration=1)
    pyautogui.leftClick()

    pyautogui.write('dwds', interval=0.2)
    pyautogui.press('space')
    pyautogui.write('test', interval=0.2)

    action_chain.pause(2).perform()

    pyautogui.press('down')
    action_chain.pause(0.5).perform()
    pyautogui.press('enter')

    action_chain.pause(4).perform()


def run_tests():
    # determine working directory
    cwd_path = Path.cwd()
    print("\tCurrent Working Directory (CWD): ", cwd_path)

    setup()

    select_text_and_click_context_menu_entry()
    focus_address_bar_and_search_with_omnibox_api()

    tear_down()


run_tests()
