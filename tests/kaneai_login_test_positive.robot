*** Settings ***
Resource    resources.robot
Suite Setup    Open Test Browser
Suite Teardown    Close Test Browser

*** Test Cases ***

KaneAI Login Valid Credentials
    [Documentation]    Migrated from KaneAI: tests login with valid admin/password credentials
    # Step 1: Go to https://web-production-f7853.up.railway.app/
    Go To    ${URL}
    # Step 2: Check main page heading text → {{page_heading}}
    Element Should Be Visible    id:page-title
    # Step 3: Assert {{page_heading}} equals Robot Framework Test Target
    Element Should Contain    id:page-title    Robot Framework Test Target
    # Step 4: Type admin in Username input field
    Input Text    id:username    admin
    # Step 5: Get text in Username input field → {{username_value}}
    # Verify: Get text in Username input field → {{username_value}}
    # Step 6: Assert {{username_value}} equals admin
    Textfield Value Should Be    id:username    admin
    # Step 7: type ******** in Password input field
    Input Text    id:password    password
    # Step 10: Click Login button
    Click Button    id:login-btn
    # Step 11: Check Welcome, admin! success banner visibility → {{login_success}}
    Wait Until Element Is Visible    id:login-message    timeout=5s
    # Step 12: Assert {{login_success}} equals true
    Wait And Verify Text    id:login-message    Welcome, admin!
    # Step 13: Check success message visibility → {{success_message_visible}}
    Wait Until Element Is Visible    id:login-message    timeout=5s
    # Step 14: Assert {{success_message_visible}} equals true
    Element Should Be Visible    id:login-message
