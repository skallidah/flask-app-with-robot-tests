*** Settings ***
Library    SeleniumLibrary
Library    String

*** Variables ***
${URL}             http://localhost:5000
${BROWSER}         chrome
${DELAY}           0.1s

*** Keywords ***
Open Test Browser
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${options}    add_argument    --headless
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Call Method    ${options}    add_argument    --disable-gpu
    Open Browser    ${URL}    ${BROWSER}    options=${options}
    Set Selenium Speed    ${DELAY}
    Maximize Browser Window

Close Test Browser
    Close All Browsers

Login With Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id:username    ${username}
    Input Text    id:password    ${password}
    Click Button    id:login-btn

Wait And Verify Text
    [Arguments]    ${locator}    ${expected_text}
    Wait Until Element Is Visible    ${locator}    timeout=5s
    Element Should Contain    ${locator}    ${expected_text}
