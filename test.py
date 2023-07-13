from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import pyautogui

def setup():
    global driver
    global action_chain
    global debugging_url

    debugging_url = "about:debugging#/runtime/this-firefox"

    # create firefox instance
    driver = webdriver.Firefox()
    # create actionChain
    action_chain = ActionChains(driver)
    # install project as add-on
    install_temporary_addon(Path.cwd().joinpath('src'))


def install_temporary_addon(addon_path):
    global driver
    # install temporary add-on
    driver.install_addon(str(addon_path), temporary=True)


def decideWhetherToShowDebuggingPageOrNot():
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
def selectTextAndClickContextMenuEntry():
    url = "https://www.dwds.de"

    global driver
    global action_chain

    decideWhetherToShowDebuggingPageOrNot()

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
    pyautogui.moveTo(x + 450, y + 340, duration=1)
    pyautogui.leftClick()

    action_chain.pause(2).perform()

def searchSuggestionsTest():
    global driver

def run_tests():
    # determine working directory
    cwd_path = Path.cwd()
    print("\tCurrent Working Directory (CWD): ", cwd_path)

    # global driver
    setup()
    selectTextAndClickContextMenuEntry()
    # driver.quit()


run_tests()