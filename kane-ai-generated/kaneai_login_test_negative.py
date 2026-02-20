
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
import time,requests,re,os, traceback
try:
    from condition import Condition, ResolvedCondition, ConcatenationOperator
except Exception as e:
    pass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lambdatest_selenium_driver import smartui_snapshot
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
try:

    actions = ActionChains(driver)
    def get_element(driver,locators):
        driver.implicitly_wait(6)
        if isinstance(locators[0], str):
            for locator in locators:
                try:
                    element = driver.find_element(By.XPATH, locator)
                    if element.is_displayed() and element.is_enabled():
                        return element
                except:
                    continue
        else:
            for locator in locators:
                by_method = By.XPATH if str(locator['isXPath']).lower() == "true" else By.CSS_SELECTOR
                try:
                    element = driver.find_element(by_method, locator['selector'])
                    if element.is_displayed() and element.is_enabled():
                        return element
                except:
                    continue
        return None

    class element_to_be_input_and_text(object):
        def __call__(self, driver):
            focused_element = driver.execute_script("return document.activeElement;")
            if focused_element.tag_name == "input" or focused_element.tag_name == "textarea" or focused_element.get_attribute("contenteditable") == "true":
                return focused_element
            else:
                return False

    def select_option(select_element, option):
        select = Select(select_element)
        select.select_by_value(option)
    driver.implicitly_wait(6)

    # Step - 1 : Go to https://web-production-f7853.up.railway.app/
    driver.get("https://web-production-f7853.up.railway.app/")
    driver.implicitly_wait(6)

    # Step - 2 : Check main heading text → {{page_heading}}
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 3 : Assert {{page_heading}} equals Robot Framework Test Target
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 4 : Type invaliduser in Username input field
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
    driver.execute_script("arguments[0].value = '';", element)
    if element.get_attribute("pattern") and '[0-9]{2}' in element.get_attribute("pattern"):
        for char in 'invaliduser':
            element.send_keys(char)
    else:
        element.send_keys('invaliduser')
    driver.implicitly_wait(6)

    # Step - 5 : Check Username field value → {{username_value}}
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 6 : Assert {{username_value}} equals invaliduser
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 7 : type ******** in Password input field
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
    driver.execute_script("arguments[0].value = '';", element)
    if element.get_attribute("pattern") and '[0-9]{2}' in element.get_attribute("pattern"):
        for char in 'password':
            element.send_keys(char)
    else:
        element.send_keys('password')
    driver.implicitly_wait(6)

    # Step - 8 : type  in 
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 9 : Assert {{password_filled}} equals true
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 10 : Click Login button
    try:
        actions.move_to_element(element).click().perform()
    except:
        element.click()
    driver.implicitly_wait(6)

    # Step - 11 : Check Invalid credentials error visibility → {{login_submitted}}
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 12 : Assert {{login_submitted}} equals true
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 13 : Get error message text under Login form → {{login_error_text}}
    'This Instruction Is Carried Out By The Vision Model'
    driver.implicitly_wait(6)

    # Step - 14 : Assert {{login_error_text}} equals Invalid credentials
    'This Instruction Is Carried Out By The Vision Model'

    driver.quit()
except Exception as e:
    driver.quit()
