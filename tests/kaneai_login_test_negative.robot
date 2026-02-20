*** Settings ***
Resource    resources.robot
Suite Setup    Open Test Browser
Suite Teardown    Close Test Browser

*** Test Cases ***

KaneAI Login Invalid Credentials
    [Documentation]    Migrated from KaneAI: tests login with invalid credentials shows error
    # Step 1: Go to https://web-production-f7853.up.railway.app/
    Go To    ${URL}
    # Step 2: Check main heading text → {{page_heading}}
    Element Should Be Visible    id:page-title
    # Step 3: Assert {{page_heading}} equals Robot Framework Test Target
    Element Should Contain    id:page-title    Robot Framework Test Target
    # Step 4: Type invaliduser in Username input field
    Input Text    id:username    invaliduser
    # Step 5: Check Username field value → {{username_value}}
    # Verify: Check Username field value → {{username_value}}
    # Step 6: Assert {{username_value}} equals invaliduser
    Textfield Value Should Be    id:username    invaliduser
    # Step 7: type ******** in Password input field
    Input Text    id:password    password
    # Step 10: Click Login button
    Click Button    id:login-btn
    # Step 11: Check Invalid credentials error visibility → {{login_submitted}}
    Wait Until Element Is Visible    id:login-message    timeout=5s
    # Step 12: Assert {{login_submitted}} equals true
    Wait Until Element Is Visible    id:login-message    timeout=5s
    # Step 14: Assert {{login_error_text}} equals Invalid credentials
    Wait And Verify Text    id:login-message    Invalid credentials
