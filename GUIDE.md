# AI-Powered Test Automation Pipeline: Complete Guide

| | |
|---|---|
| **Date** | February 20, 2026 |
| **Version** | 1.0 |
| **Repository** | [flask-app-with-robot-tests](https://github.com/skallidah/flask-app-with-robot-tests) |
| **Live App** | [web-production-f7853.up.railway.app](https://web-production-f7853.up.railway.app) |
| **Status** | Complete |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Build the Flask Web App with Robot Framework Tests](#3-step-1-build-the-flask-web-app-with-robot-framework-tests)
4. [Step 2: Test Locally and Deploy to Railway](#4-step-2-test-locally-and-deploy-to-railway)
5. [Step 3: Push to GitHub with CI/CD Pipeline](#5-step-3-push-to-github-with-cicd-pipeline)
6. [Step 4: Verify Everything Works](#6-step-4-verify-everything-works)
7. [Step 5: Add Requirements Document to JIRA](#7-step-5-add-requirements-document-to-jira)
8. [Step 6: Set Up KaneAI-to-JIRA Integration](#8-step-6-set-up-kaneai-to-jira-integration)
9. [Step 7: Generate Test Scenarios with KaneAI Agent](#9-step-7-generate-test-scenarios-with-kaneai-agent)
10. [Step 8: KaneAI Generates Scripts](#10-step-8-kaneai-generates-scripts)
11. [Step 9: Download KaneAI Scripts and Push to GitHub](#11-step-9-download-kaneai-scripts-and-push-to-github)
12. [Step 10: Build MCP Server for Script Migration](#12-step-10-build-mcp-server-for-script-migration)
13. [Step 11: Test Migrated Scripts and Push to GitHub](#13-step-11-test-migrated-scripts-and-push-to-github)
14. [Step 12: Run All Tests via GitHub Actions and Verify](#14-step-12-run-all-tests-via-github-actions-and-verify)
15. [Appendix A: Project File Reference](#appendix-a-project-file-reference)
16. [Appendix B: MCP Server Tool Reference](#appendix-b-mcp-server-tool-reference)
17. [Appendix C: Troubleshooting](#appendix-c-troubleshooting)
18. [Appendix D: Glossary](#appendix-d-glossary)

---

## 1. Introduction

### 1.1 Purpose

This guide walks through building a complete AI-assisted test automation pipeline. It demonstrates how AI-powered tools can work together in a modern QA workflow:

- A **Python Flask web application** serves as the test target
- **Robot Framework** provides keyword-driven browser automation tests
- **TestMu AI's KaneAI** generates additional test scripts from natural-language requirements in JIRA
- A custom **MCP Server** bridges KaneAI's Selenium/Python output into Robot Framework format
- **GitHub Actions** automates continuous testing against a cloud-deployed app on **Railway**

### 1.2 Workflow at a Glance

| Step | Action | Outcome |
|------|--------|---------|
| 1 | Build Python Flask web app with Robot Framework tests | Working app + 20 automated tests |
| 2 | Test locally and deploy to Railway | Publicly accessible app for KaneAI |
| 3 | Push code to GitHub with GitHub Actions CI pipeline | Automated test execution on every push |
| 4 | Verify everything works end-to-end | Confidence in the pipeline |
| 5 | Add the requirements document to JIRA | Structured acceptance criteria for AI test generation |
| 6 | Set up KaneAI-to-JIRA integration on TestMu AI | Enable AI to read requirements from JIRA |
| 7 | Link JIRA ID in KaneAI Agent and generate test scenarios | AI generates scenarios from requirements |
| 8 | KaneAI generates test scenarios, steps, and Selenium/Python scripts | Automated scripts with HyperExecute hooks |
| 9 | Download KaneAI scripts and push to GitHub | Scripts versioned in the repo |
| 10 | Build MCP server to migrate KaneAI scripts to Robot Framework | Reusable migration tooling |
| 11 | Test migrated scripts locally and push to GitHub | Validated Robot Framework tests |
| 12 | Run all Robot tests on Railway via GitHub Actions | 22/22 tests passing in CI |

### 1.3 Time Estimate

| Step | Estimated Time |
|------|---------------|
| Prerequisites & setup | 15-20 min |
| Steps 1-4 (Build, deploy, CI) | 20-25 min |
| Steps 5-9 (JIRA, KaneAI, scripts) | 15-20 min |
| Steps 10-12 (MCP, migrate, verify) | 15-20 min |
| **Total** | **~65-85 min** |

---

## 2. Prerequisites

### 2.1 Hardware & OS

- macOS (tested on macOS Sequoia / Darwin 24.6.0)
- Apple Silicon (M1/M2/M3/M4) or Intel Mac

### 2.2 Software Installation

Run the following commands in your terminal. Each step verifies the installation.

#### Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify:
```bash
brew --version
# Expected: Homebrew 4.x.x
```

#### Install Python 3

```bash
brew install python
```

Verify:
```bash
python3 --version
# Expected: Python 3.12+

pip3 --version
# Expected: pip 25.x+
```

#### Install Google Chrome

```bash
brew install --cask google-chrome
```

Or download from [google.com/chrome](https://www.google.com/chrome/).

#### Install ChromeDriver

```bash
brew install --cask chromedriver
```

**Important - macOS Gatekeeper fix:**
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```

Verify versions match:
```bash
chromedriver --version
# Must match Chrome's major version
```

#### Install Git & GitHub CLI

```bash
brew install git gh
```

Authenticate GitHub CLI:
```bash
gh auth login --web --scopes workflow
```

> **Why `--scopes workflow`?** GitHub's OAuth requires the `workflow` scope to push files under `.github/workflows/`. Without it, `git push` will be rejected.

#### Install Railway CLI

```bash
brew install railway
railway login
```

### 2.3 Accounts Needed

| Service | URL | Purpose |
|---------|-----|---------|
| GitHub | [github.com](https://github.com) | Source code & CI/CD |
| Railway | [railway.app](https://railway.app) | Cloud deployment |
| LambdaTest / TestMu AI | [testmuai.com](https://www.testmuai.com) | KaneAI test generation |
| Atlassian JIRA | [atlassian.net](https://www.atlassian.net) | Requirements management |

---

## 3. Step 1: Build the Flask Web App with Robot Framework Tests

### 3.1 Overview

Build a single-page Python Flask web application with rich, interactive DOM elements, along with a comprehensive Robot Framework test suite that validates all functionality.

### 3.2 Project Initialization

```bash
mkdir -p python-robot-demo && cd python-robot-demo
```

### 3.3 Application Structure

The web app consists of three files:

| File | Purpose |
|------|---------|
| `app.py` | Flask application with 3 API endpoints (`/api/login`, `/api/greet`, `/api/search`) |
| `templates/index.html` | Single page with 16 interactive sections, all with unique HTML IDs |
| `static/style.css` | Clean, modern styling for all components |

**API Endpoints:**

| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| POST | `/api/login` | `{"username": "admin", "password": "password"}` | `{"success": true, "message": "Welcome, admin!"}` |
| POST | `/api/greet` | `{"name": "Robot"}` | `{"greeting": "Hello, Robot!"}` |
| GET | `/api/search?q=app` | Query param `q` | `{"results": ["Apple"], "query": "app"}` |

**UI Sections (16 total):**

| # | Section | Key Elements | HTML IDs |
|---|---------|-------------|----------|
| 1 | Login Form | Text input, password, checkbox, submit | `username`, `password`, `remember-me`, `login-btn` |
| 2 | Counter | Increment, decrement, reset, display | `increment-btn`, `decrement-btn`, `reset-btn`, `counter-value` |
| 3 | Dropdowns | Single-select, multi-select, color preview | `color-select`, `multi-select`, `color-preview` |
| 4 | Checkboxes & Radios | 4 checkboxes, 3 radio buttons | `chk-coding`, `chk-music`, `radio-beginner`, etc. |
| 5 | Tabs | 3 tab buttons + content panels | `tab1`, `tab2`, `tab3` |
| 6 | Accordion | 3 collapsible sections | Accordion items with headers/bodies |
| 7 | Data Table | 5 rows, sortable columns, delete buttons | `data-table`, `row-count` |
| 8 | Greeting (AJAX) | Name input + greet button | `greet-name`, `greet-btn`, `greeting-result` |
| 9 | Fruit Search (AJAX) | Search input + live results | `search-input`, `search-results` |
| 10 | Toggle Content | Show/hide button | `toggle-btn`, `hidden-content` |
| 11 | Delayed Content | Load button + 2s delay | `delayed-btn`, `delayed-text` |
| 12 | Modal Dialog | Open/close/confirm + input | `open-modal-btn`, `modal-overlay`, `modal-input` |
| 13 | Toast Notifications | Success/error/info buttons | `toast-container` |
| 14 | Alerts | Success/warning/error + dismiss | `alert-success`, `alert-warning`, `alert-error` |
| 15 | File Upload | File input + info display | `file-input`, `file-name`, `file-size` |
| 16 | Drag and Drop | 3 draggable items + drop zone | `drag-item-1/2/3`, `drop-target` |

### 3.4 Robot Framework Tests

The test suite consists of two files:

```
tests/
├── resources.robot        # Shared settings, variables, and keywords
└── web_tests.robot        # 20 test cases covering all UI sections
```

**Shared Keywords (`resources.robot`):**
- `Open Test Browser` - launches headless Chrome with standard flags
- `Close Test Browser` - tears down all browser sessions
- `Login With Credentials` - reusable login keyword accepting username/password
- `Wait And Verify Text` - waits for element visibility then checks text content

**Test Cases (20 total):**

| # | Test Case | What It Verifies |
|---|-----------|-----------------|
| 1 | Page Should Load Successfully | Title, heading text |
| 2 | Login With Valid Credentials | admin/password -> "Welcome, admin!" |
| 3 | Login With Invalid Credentials | wrong/wrong -> "Invalid credentials" |
| 4 | Remember Me Checkbox | Check/uncheck toggle |
| 5 | Counter Increment And Decrement | +++ = 3, then - = 2, reset = 0 |
| 6 | Color Dropdown Selection | Select "blue" -> preview appears |
| 7 | Checkboxes | Multi-select, independent toggle |
| 8 | Radio Buttons | Mutual exclusion |
| 9 | Tab Switching | Tab 1 -> Tab 2 -> Tab 3 visibility |
| 10 | Accordion Toggle | Expand/collapse sections |
| 11 | Data Table Row Count | Initial count = 5 |
| 12 | Data Table Row Deletion | Delete row -> count decreases |
| 13 | Greeting API | "Robot" -> "Hello, Robot!" |
| 14 | Toggle Hidden Content | Show/hide toggle |
| 15 | Delayed Content Loading | 2s delay -> content appears |
| 16 | Open And Close Modal | Open -> close via X button |
| 17 | Modal Confirm | Input value -> confirm -> toast |
| 18 | Alerts Are Visible | All 3 alerts visible on load |
| 19 | Dismiss Alert | Warning alert hidden after click |
| 20 | Search Fruits | "app" -> "Apple" in results |

---

## 4. Step 2: Test Locally and Deploy to Railway

### 4.1 Local Testing

Install dependencies and start the app:
```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 and interact with all sections to verify functionality.

> **Note:** macOS Monterey+ uses port 5000 for AirPlay Receiver. If the port is busy, disable AirPlay in System Settings or change the port in `app.py`.

Run the Robot Framework tests:
```bash
robot --variable URL:http://localhost:5000 --outputdir results tests/
```

**Expected:** 20 tests, 20 passed, 0 failed.

### 4.2 Deploy to Railway

Railway is a cloud platform that auto-detects Python apps and deploys them with minimal configuration.

**Deployment files required:**

| File | Purpose |
|------|---------|
| `Procfile` | `web: gunicorn app:app --bind 0.0.0.0:$PORT` |
| `railway.json` | Build and deploy configuration |
| `requirements.txt` | Python dependencies (auto-installed by Railway) |

**Deploy steps:**

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub Repo"**
3. If your repo doesn't appear, go to GitHub Settings -> Integrations -> Applications -> Railway -> Configure, and grant access
4. Select the repository; Railway auto-detects the Procfile and builds
5. In the Railway dashboard, click your service -> Settings -> Networking -> Public Networking -> **Generate Domain**
6. Your app is now publicly accessible (e.g., `https://web-production-f7853.up.railway.app`)

**Verify:**
```bash
curl -s -o /dev/null -w "%{http_code}" https://web-production-f7853.up.railway.app
# Expected: 200
```

---

## 5. Step 3: Push to GitHub with CI/CD Pipeline

### 5.1 Initialize Git and Push

```bash
git init
git add .
git commit -m "Initial commit"
gh repo create flask-app-with-robot-tests --public --source=. --push
```

> You may need to run `gh auth setup-git` first if push fails with authentication errors.

### 5.2 GitHub Actions Workflow

The workflow file (`.github/workflows/test.yml`) runs Robot Framework tests on every push to `main`:

- Installs Python 3.12, Chrome, and ChromeDriver
- Installs project dependencies
- Runs all Robot Framework tests against the deployed Railway URL
- Uploads test reports (`report.html`, `log.html`, `output.xml`) as artifacts

### 5.3 Configure the Railway URL

Set the `APP_URL` variable so CI runs against the deployed app:

```bash
gh variable set APP_URL \
  --body "https://web-production-f7853.up.railway.app" \
  --repo <your-username>/flask-app-with-robot-tests
```

---

## 6. Step 4: Verify Everything Works

### 6.1 Trigger the CI Pipeline

```bash
gh workflow run test.yml --repo <your-username>/flask-app-with-robot-tests
```

### 6.2 Monitor Results

```bash
# Check status (wait ~90 seconds)
gh run list --repo <your-username>/flask-app-with-robot-tests --limit 1
# Expected: completed  success
```

### 6.3 View Reports

Download the `robot-results` artifact from the GitHub Actions run page, or view locally:
```bash
open results/report.html
```

At this point you should have:
- 20 Robot Framework tests passing locally
- 20 tests passing against the Railway-deployed app
- GitHub Actions CI running tests automatically on every push

---

## 7. Step 5: Add Requirements Document to JIRA

### 7.1 Create the Requirements Document

Create a structured requirements document (`REQUIREMENTS.md`) that describes every feature of the web application with acceptance criteria. This document serves as the input for KaneAI's AI test generation.

**Structure for each feature:**
```
Feature N: Feature Name
  Section: UI section identifier
  Elements: List of interactive elements
  Acceptance Criteria:
    AC-N.1: When [action], then [expected result]
    AC-N.2: ...
```

The full document covers all 16 features with 50+ acceptance criteria.

**Reference:** [`REQUIREMENTS.md`](REQUIREMENTS.md)

### 7.2 Add to JIRA

1. Create a new JIRA Story in your project
2. Copy the requirements content into the story description
3. Note down the **JIRA ID** (e.g., `PROJ-123`) - you will need this for KaneAI

---

## 8. Step 6: Set Up KaneAI-to-JIRA Integration

### 8.1 Access TestMu AI

1. Log in to [testmuai.com](https://www.testmuai.com)
2. Navigate to the KaneAI section

### 8.2 Configure JIRA Integration

1. In KaneAI settings, locate the **JIRA Integration** section
2. Connect your Atlassian account by providing:
   - JIRA instance URL (e.g., `https://yourteam.atlassian.net`)
   - API token or OAuth credentials
3. Verify the integration is active and can read your JIRA projects
4. Confirm the JIRA story with your requirements is accessible from KaneAI

---

## 9. Step 7: Generate Test Scenarios with KaneAI Agent

### 9.1 Link JIRA and Generate

1. In KaneAI, navigate to **Agent**
2. **Link the JIRA ID** that contains your web app requirements
3. Provide the following instruction:

   > Generate test scenarios and test cases
   >
   > URL: https://web-production-f7853.up.railway.app

4. KaneAI's Agent will read the requirements from JIRA, access the live application URL, and begin generating test scenarios

---

## 10. Step 8: KaneAI Generates Scripts

### 10.1 What KaneAI Produces

KaneAI generates the following artifacts:

| Artifact | Description |
|----------|-------------|
| **Test Scenarios** | High-level descriptions of what to test |
| **Test Steps** | Detailed step-by-step instructions for each scenario |
| **Automated Scripts** | Selenium/Python scripts with HyperExecute hooks |

### 10.2 Script Characteristics

KaneAI-generated scripts include:

| Pattern | Description |
|---------|-------------|
| Step comments | `# Step - 4 : Type admin in Username input field` |
| Vision model assertions | `'This Instruction Is Carried Out By The Vision Model'` |
| LambdaTest imports | `from lambdatest_selenium_driver import smartui_snapshot` |
| Multi-locator helpers | `get_element(driver, locators)` for resilient element finding |
| Action chains | `actions.move_to_element(element).click().perform()` |

These scripts are optimized for LambdaTest's HyperExecute infrastructure and include customizations specific to that platform.

### 10.3 Example: Generated Login Test

**`kaneai_login_test_positive.py`** - 14 steps:
1. Navigate to the app URL
2-3. Verify page heading equals "Robot Framework Test Target"
4-6. Type "admin" in username field and verify
7-9. Type password and verify
10. Click Login button
11-14. Verify "Welcome, admin!" success message appears

---

## 11. Step 9: Download KaneAI Scripts and Push to GitHub

### 11.1 Download Scripts

Download the generated Python scripts from KaneAI's interface.

### 11.2 Add to Repository

Place the scripts in a dedicated folder:

```bash
mkdir -p kane-ai-generated
# Copy downloaded scripts into kane-ai-generated/
```

### 11.3 Push to GitHub

```bash
git add kane-ai-generated/
git commit -m "Add KaneAI-generated test scripts"
git push origin main
```

---

## 12. Step 10: Build MCP Server for Script Migration

### 12.1 What is MCP?

**Model Context Protocol (MCP)** is an open standard that allows AI assistants to connect to external tools and data sources. It works like a plugin system for AI applications.

| Concept | Description |
|---------|-------------|
| **MCP Host** | The AI application that needs external capabilities |
| **MCP Server** | A lightweight program that exposes tools over a standard protocol |
| **Tools** | Functions the AI can call (like API endpoints for the AI) |
| **Transport** | Communication channel - **stdio** (local) or **SSE** (HTTP) |

**How it works:**
```
AI Assistant                   MCP Server
    |                              |
    |---- Initialize ------------>|
    |<--- Capabilities -----------|
    |                              |
    |---- Call Tool ------------->|
    |     (JSON-RPC request)       |
    |<--- Tool Result ------------|
    |     (JSON-RPC response)      |
```

### 12.2 MCP Server Implementation

The MCP server (`mcp-server/server.py`) provides 4 tools:

| Tool | Description |
|------|-------------|
| `list_kaneai_scripts` | Lists all KaneAI Python scripts available for migration |
| `analyze_kaneai_script` | Parses a script and extracts structured test steps with classifications |
| `migrate_to_robot` | Converts a KaneAI Selenium/Python script to a Robot Framework `.robot` file |
| `list_robot_tests` | Lists all existing Robot Framework tests for context |

### 12.3 Migration Pipeline

The `migrate_to_robot` tool performs the following transformations:

1. Parse step comments (`# Step - N : description`)
2. Classify each step (navigate, input, click, assert, verify)
3. Extract data values (URLs, input text, expected values)
4. Map field descriptions to HTML ID locators
5. Map Selenium operations to SeleniumLibrary keywords
6. Map assertions to Robot Framework assertion keywords
7. Reuse `resources.robot` shared keywords
8. Write `.robot` file with proper formatting

**Mapping examples:**

| KaneAI (Selenium/Python) | Robot Framework |
|--------------------------|-----------------|
| `driver.get("https://...")` | `Go To    ${URL}` |
| `element.send_keys('admin')` on Username | `Input Text    id:username    admin` |
| `actions.move_to_element(element).click()` on Login | `Click Button    id:login-btn` |
| Vision model: heading equals "X" | `Element Should Contain    id:page-title    X` |
| Vision model: error text equals "X" | `Wait And Verify Text    id:login-message    X` |

### 12.4 Install and Configure

```bash
pip install "mcp[cli]"
```

**MCP configuration (`.mcp.json` in project root):**
```json
{
  "mcpServers": {
    "kaneai-to-robot": {
      "command": "python",
      "args": ["mcp-server/server.py"],
      "env": {
        "PROJECT_ROOT": "/path/to/python-robot-demo"
      }
    }
  }
}
```

### 12.5 Before vs After

| Aspect | KaneAI (Selenium/Python) | Robot Framework |
|--------|--------------------------|-----------------|
| Lines of code | 132 | 33 |
| Readability | Low (boilerplate-heavy) | High (keyword-driven) |
| Portability | LambdaTest-specific | Any Selenium Grid / local |
| Maintainability | Inline helpers, try/except | Shared keywords in `resources.robot` |
| Configuration | Hardcoded URL | Variable `${URL}` |
| Assertions | Vision model placeholders | Concrete SeleniumLibrary keywords |

---

## 13. Step 11: Test Migrated Scripts and Push to GitHub

### 13.1 Run Migration

```python
from server import migrate_to_robot

migrate_to_robot(
    'kane-ai-generated/kaneai_login_test_positive.py',
    test_name='KaneAI Login Valid Credentials',
    documentation='Migrated from KaneAI: valid login test',
)

migrate_to_robot(
    'kane-ai-generated/kaneai_login_test_negative.py',
    test_name='KaneAI Login Invalid Credentials',
    documentation='Migrated from KaneAI: invalid login test',
)
```

### 13.2 Test Locally

```bash
# Run all tests (original + migrated)
robot --variable URL:http://localhost:5000 --outputdir results tests/
```

**Expected:** 22 tests, 22 passed, 0 failed.

### 13.3 Push to GitHub

```bash
git add tests/kaneai_login_test_positive.robot tests/kaneai_login_test_negative.robot mcp-server/
git commit -m "Add MCP server and migrated KaneAI tests"
git push origin main
```

---

## 14. Step 12: Run All Tests via GitHub Actions and Verify

### 14.1 Trigger the Pipeline

```bash
gh workflow run test.yml --repo <your-username>/flask-app-with-robot-tests
```

### 14.2 Monitor Results

```bash
gh run list --repo <your-username>/flask-app-with-robot-tests --limit 1
# Expected: completed  success  (22 tests, 22 passed)
```

### 14.3 Final Verification Checklist

| Check | Expected Result |
|-------|----------------|
| Local tests against localhost | 22 passed, 0 failed |
| Local tests against Railway URL | 22 passed, 0 failed |
| GitHub Actions CI | completed, success |
| Robot report.html | All tests green |
| Railway app accessible | HTTP 200 |

### 14.4 View Reports

```bash
open results/report.html
```

Or download the `robot-results` artifact from the GitHub Actions run page.

---

## Appendix A: Project File Reference

```
python-robot-demo/
|-- app.py                                    # Flask application (3 API endpoints)
|-- templates/
|   +-- index.html                            # Single page with 16 interactive sections
|-- static/
|   +-- style.css                             # Styling for all components
|-- tests/
|   |-- resources.robot                       # Shared keywords and variables
|   |-- web_tests.robot                       # 20 original test cases
|   |-- kaneai_login_test_positive.robot      # Migrated: valid login test
|   +-- kaneai_login_test_negative.robot      # Migrated: invalid login test
|-- kane-ai-generated/
|   |-- kaneai_login_test_positive.py         # KaneAI output: valid login
|   +-- kaneai_login_test_negative.py         # KaneAI output: invalid login
|-- mcp-server/
|   |-- server.py                             # MCP server (4 tools)
|   +-- requirements.txt                      # MCP dependencies
|-- .mcp.json                                 # MCP configuration
|-- .github/
|   +-- workflows/
|       +-- test.yml                          # GitHub Actions CI workflow
|-- requirements.txt                          # Python dependencies
|-- Procfile                                  # Railway deployment command
|-- railway.json                              # Railway config
|-- REQUIREMENTS.md                           # Feature requirements for KaneAI
|-- WORKFLOW_SUMMARY.md                       # Workflow overview with diagrams
|-- GUIDE.md                                  # This document
|-- README.md                                 # Quick-start setup guide
+-- .gitignore                                # Git ignore rules
```

---

## Appendix B: MCP Server Tool Reference

### `list_kaneai_scripts`

```
Description: List all KaneAI-generated Python scripts available for migration
Parameters:
  - scripts_dir (optional): Path to scripts directory. Default: kane-ai-generated/
Returns: JSON with script names, step counts, and step summaries
```

### `analyze_kaneai_script`

```
Description: Analyze a KaneAI script and extract structured test steps
Parameters:
  - file_path (required): Path to the KaneAI Python script
Returns: JSON with step details, classifications, extracted data, vision step counts
```

### `migrate_to_robot`

```
Description: Convert a KaneAI Selenium/Python script to a Robot Framework .robot file
Parameters:
  - file_path (required): Path to the KaneAI Python script
  - test_name (optional): Name for the Robot test case
  - documentation (optional): Documentation string for the test
  - output_path (optional): Where to save the .robot file. Default: tests/<filename>.robot
Returns: JSON with generated file path and Robot Framework content
```

### `list_robot_tests`

```
Description: List all existing Robot Framework test files and their test cases
Parameters:
  - tests_dir (optional): Path to tests directory. Default: tests/
Returns: JSON with file names, test case names, and counts
```

---

## Appendix C: Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `chromedriver` blocked by macOS | Gatekeeper quarantine | `xattr -d com.apple.quarantine $(which chromedriver)` |
| ChromeDriver version mismatch | Chrome updated but ChromeDriver didn't | `brew upgrade --cask google-chrome chromedriver` |
| Port 5000 in use | macOS AirPlay Receiver | Disable in System Settings -> General -> AirDrop & Handoff |
| `pip` not found | Python not in PATH or venv not activated | Use `pip3` or activate venv: `source venv/bin/activate` |
| GitHub push rejected for workflows | OAuth token missing `workflow` scope | `gh auth login --web --scopes workflow` |
| Repo not visible in Railway | Railway GitHub app not authorized | GitHub Settings -> Applications -> Railway -> Configure -> add repo |
| MCP server not connecting | Wrong Python path or PROJECT_ROOT | Verify paths in `.mcp.json`, ensure `mcp[cli]` is installed |
| Robot tests timeout | App not running or URL incorrect | Verify app is accessible: `curl -s <URL>` |
| `robotframework-seleniumlibrary` install fails | Python version incompatibility | Use version 6.8.0+ for Python 3.13+ |

### Debug Commands

```bash
# Check if app is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000

# Check Chrome/ChromeDriver versions
google-chrome --version
chromedriver --version

# Check GitHub Actions status
gh run list --repo <your-username>/flask-app-with-robot-tests --limit 5

# Test MCP server parsing
python -c "import sys; sys.path.insert(0,'mcp-server'); from server import list_kaneai_scripts; print(list_kaneai_scripts())"
```

---

## Appendix D: Glossary

| Term | Definition |
|------|-----------|
| **Flask** | Lightweight Python web framework for building web applications |
| **GitHub Actions** | GitHub's built-in CI/CD platform for automating workflows |
| **Gunicorn** | Production-grade Python WSGI HTTP server |
| **HyperExecute** | LambdaTest's high-performance test execution infrastructure |
| **JIRA** | Atlassian's project management and issue tracking tool |
| **KaneAI** | TestMu AI's (by LambdaTest) AI-powered test script generation tool |
| **MCP** | Model Context Protocol - open standard for connecting AI tools to external capabilities |
| **MCP Host** | The AI application that consumes MCP server capabilities |
| **MCP Server** | A program that exposes tools and resources over the MCP protocol |
| **Nixpacks** | Railway's build system that auto-detects project type and builds containers |
| **Railway** | Cloud platform-as-a-service (PaaS) for deploying web applications |
| **Robot Framework** | Open-source keyword-driven test automation framework |
| **Selenium** | Browser automation library for controlling web browsers programmatically |
| **SeleniumLibrary** | Robot Framework library that wraps Selenium for browser testing |
| **TestMu AI** | AI-powered testing platform by LambdaTest |
| **Vision Model** | KaneAI's visual AI that performs assertions based on visual page analysis |
