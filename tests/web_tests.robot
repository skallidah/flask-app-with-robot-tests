*** Settings ***
Resource    resources.robot
Suite Setup    Open Test Browser
Suite Teardown    Close Test Browser

*** Test Cases ***

Page Should Load Successfully
    [Documentation]    Verify the page loads and has the correct title
    Title Should Be    Robot Framework Test Target
    Element Should Be Visible    id:page-title
    Element Should Contain    id:page-title    Robot Framework Test Target

Login With Valid Credentials
    [Documentation]    Test login form with valid credentials
    Login With Credentials    admin    password
    Wait And Verify Text    id:login-message    Welcome, admin!
    Element Should Be Visible    id:login-message

Login With Invalid Credentials
    [Documentation]    Test login form with invalid credentials
    Clear Element Text    id:username
    Clear Element Text    id:password
    Login With Credentials    wrong    wrong
    Wait And Verify Text    id:login-message    Invalid credentials

Remember Me Checkbox
    [Documentation]    Test the remember me checkbox
    Checkbox Should Not Be Selected    id:remember-me
    Select Checkbox    id:remember-me
    Checkbox Should Be Selected    id:remember-me
    Unselect Checkbox    id:remember-me
    Checkbox Should Not Be Selected    id:remember-me

Counter Increment And Decrement
    [Documentation]    Test the counter buttons
    Element Should Contain    id:counter-value    0
    Click Button    id:increment-btn
    Click Button    id:increment-btn
    Click Button    id:increment-btn
    Element Should Contain    id:counter-value    3
    Click Button    id:decrement-btn
    Element Should Contain    id:counter-value    2
    Click Button    id:reset-btn
    Element Should Contain    id:counter-value    0

Color Dropdown Selection
    [Documentation]    Test the color select dropdown
    Element Should Not Be Visible    id:color-preview
    Select From List By Value    id:color-select    blue
    Wait Until Element Is Visible    id:color-preview    timeout=3s
    Element Should Contain    id:color-name    blue

Checkboxes
    [Documentation]    Test checking and unchecking checkboxes
    Select Checkbox    id:chk-coding
    Select Checkbox    id:chk-music
    Checkbox Should Be Selected    id:chk-coding
    Checkbox Should Be Selected    id:chk-music
    Checkbox Should Not Be Selected    id:chk-sports
    Unselect Checkbox    id:chk-coding

Radio Buttons
    [Documentation]    Test radio button selection
    Click Element    id:radio-beginner
    Radio Button Should Be Set To    level    beginner
    Click Element    id:radio-expert
    Radio Button Should Be Set To    level    expert

Tab Switching
    [Documentation]    Test tab navigation
    Element Should Be Visible    id:tab1
    Element Should Not Be Visible    id:tab2
    Click Element    xpath://button[@data-tab='tab2']
    Element Should Not Be Visible    id:tab1
    Element Should Be Visible    id:tab2
    Element Should Contain    id:tab2    Tab 2 Content
    Click Element    xpath://button[@data-tab='tab3']
    Element Should Be Visible    id:tab3
    Element Should Contain    id:tab3    Tab 3 Content

Accordion Toggle
    [Documentation]    Test accordion expand and collapse
    Element Should Not Be Visible    xpath://div[@class='accordion-item'][1]//div[@class='accordion-body']
    Click Element    xpath://div[@class='accordion-item'][1]//button
    Wait Until Element Is Visible    xpath://div[contains(@class,'accordion-item')][1]//div[@class='accordion-body']    timeout=3s

Data Table Row Count
    [Documentation]    Verify initial table row count
    Element Should Contain    id:row-count    Rows: 5

Data Table Row Deletion
    [Documentation]    Test deleting a row from the data table
    ${rows_before}=    Get Element Count    xpath://table[@id='data-table']/tbody/tr
    Click Button    xpath://table[@id='data-table']/tbody/tr[1]//button
    ${rows_after}=    Get Element Count    xpath://table[@id='data-table']/tbody/tr
    Should Be Equal As Numbers    ${rows_after}    ${rows_before - 1}

Greeting API
    [Documentation]    Test the greeting dynamic content
    Input Text    id:greet-name    Robot
    Click Button    id:greet-btn
    Wait And Verify Text    id:greeting-result    Hello, Robot!

Toggle Hidden Content
    [Documentation]    Test show/hide toggle functionality
    Element Should Not Be Visible    id:hidden-content
    Click Button    id:toggle-btn
    Wait Until Element Is Visible    id:hidden-content    timeout=3s
    Element Should Contain    id:hidden-content    This content was hidden
    Click Button    id:toggle-btn
    Wait Until Element Is Not Visible    id:hidden-content    timeout=3s

Delayed Content Loading
    [Documentation]    Test content that loads after a delay
    Click Button    id:delayed-btn
    Wait Until Element Is Visible    id:delayed-text    timeout=5s
    Element Should Contain    id:delayed-text    Delayed content loaded!

Open And Close Modal
    [Documentation]    Test opening and closing the modal dialog
    Element Should Not Be Visible    id:modal-overlay
    Click Button    id:open-modal-btn
    Wait Until Element Is Visible    id:modal-overlay    timeout=3s
    Element Should Be Visible    id:modal-input
    Click Button    id:close-modal-btn
    Wait Until Element Is Not Visible    id:modal-overlay    timeout=3s

Modal Confirm
    [Documentation]    Test modal confirmation with input
    Click Button    id:open-modal-btn
    Wait Until Element Is Visible    id:modal-overlay    timeout=3s
    Input Text    id:modal-input    Test Value
    Click Button    id:modal-confirm-btn
    Wait Until Element Is Not Visible    id:modal-overlay    timeout=3s

Alerts Are Visible
    [Documentation]    Verify alert elements are visible
    Element Should Be Visible    id:alert-success
    Element Should Be Visible    id:alert-warning
    Element Should Be Visible    id:alert-error

Dismiss Alert
    [Documentation]    Test dismissing an alert
    Element Should Be Visible    id:alert-warning
    Click Button    xpath://section[@id='alert-section']//button
    Wait Until Element Is Not Visible    id:alert-warning    timeout=3s

Search Fruits
    [Documentation]    Test the fruit search functionality
    Input Text    id:search-input    app
    Sleep    0.5s
    ${results}=    Get Element Count    xpath://ul[@id='search-results']/li
    Should Be True    ${results} >= 1
    Element Should Contain    id:search-results    Apple
