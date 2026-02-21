# AI-Powered Test Automation Pipeline: Complete Guide

| | |
|---|---|
| **Author** | Generated with Claude Code |
| **Date** | February 20, 2026 |
| **Version** | 1.0 |
| **Repository** | [flask-app-with-robot-tests](https://github.com/skallidah/flask-app-with-robot-tests) |
| **Live App** | [web-production-f7853.up.railway.app](https://web-production-f7853.up.railway.app) |
| **Status** | Complete |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Phase 1: Build the Flask Web Application](#3-phase-1-build-the-flask-web-application)
4. [Phase 2: Write Robot Framework Tests](#4-phase-2-write-robot-framework-tests)
5. [Phase 3: Deploy to Railway](#5-phase-3-deploy-to-railway)
6. [Phase 4: Set Up GitHub Actions CI/CD](#6-phase-4-set-up-github-actions-cicd)
7. [Phase 5: Write Requirements for KaneAI](#7-phase-5-write-requirements-for-kaneai)
8. [Phase 6: Generate Tests with KaneAI](#8-phase-6-generate-tests-with-kaneai)
9. [Phase 7: Build the MCP Server](#9-phase-7-build-the-mcp-server)
10. [Phase 8: Migrate KaneAI Scripts to Robot Framework](#10-phase-8-migrate-kaneai-scripts-to-robot-framework)
11. [Phase 9: Validate Everything End-to-End](#11-phase-9-validate-everything-end-to-end)
12. [Appendix A: Project File Reference](#appendix-a-project-file-reference)
13. [Appendix B: MCP Server Tool Reference](#appendix-b-mcp-server-tool-reference)
14. [Appendix C: Troubleshooting](#appendix-c-troubleshooting)
15. [Appendix D: Glossary](#appendix-d-glossary)

---

## 1. Introduction

### 1.1 Purpose

This guide walks through building a complete AI-assisted test automation pipeline. It demonstrates how multiple AI tools can work together in a modern QA workflow:

- **Claude Code** generates the application, tests, infrastructure, and tooling
- **TestMu AI's KaneAI** generates additional test scripts from natural-language requirements
- A custom **MCP Server** bridges the gap between KaneAI's output format and Robot Framework
- **GitHub Actions** automates continuous testing against a cloud-deployed app

### 1.2 What You Will Build

```
┌──────────────────────────────────────────────────────────────────┐
│                    Complete Pipeline Overview                      │
│                                                                    │
│  Claude Code ──► Flask App ──► Railway (Cloud Deploy)             │
│       │                              │                             │
│       ├──► Robot Framework Tests ────┼──► GitHub Actions CI       │
│       │                              │                             │
│       ├──► Requirements Doc ──► KaneAI ──► Selenium Scripts       │
│       │                                        │                   │
│       └──► MCP Server ────────────── Migrates ─┘                  │
│                                        │                           │
│                                  Robot Tests (22 total, all pass) │
└──────────────────────────────────────────────────────────────────┘
```

### 1.3 Time Estimate

| Phase | Estimated Time |
|-------|---------------|
| Prerequisites & setup | 15–20 min |
| Build Flask app (with Claude Code) | 5 min |
| Write Robot tests (with Claude Code) | 5 min |
| Deploy to Railway | 10 min |
| GitHub Actions setup | 5 min |
| KaneAI test generation | 10–15 min |
| Build MCP server (with Claude Code) | 5 min |
| Migration & validation | 5 min |
| **Total** | **~60–70 min** |

---

## 2. Prerequisites

### 2.1 Hardware & OS

- macOS (tested on macOS Sequoia / Darwin 24.6.0)
- Apple Silicon (M1/M2/M3/M4) or Intel Mac

### 2.2 Software Installation

Run the following commands in your terminal. Each step verifies the installation.

#### Step 1: Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify:
```bash
brew --version
# Expected: Homebrew 4.x.x
```

#### Step 2: Install Python 3

```bash
brew install python
```

Verify:
```bash
python3 --version
# Expected: Python 3.12+ (we used 3.14.0)

pip3 --version
# Expected: pip 25.x+
```

#### Step 3: Install Google Chrome

```bash
brew install --cask google-chrome
```

Or download from [google.com/chrome](https://www.google.com/chrome/).

#### Step 4: Install ChromeDriver

```bash
brew install --cask chromedriver
```

**Important — macOS Gatekeeper fix:**
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```

Verify versions match:
```bash
chromedriver --version
# Must match Chrome's major version
```

#### Step 5: Install Git & GitHub CLI

```bash
brew install git gh
```

Authenticate GitHub CLI:
```bash
gh auth login --web --scopes workflow
```

> **Why `--scopes workflow`?** GitHub's OAuth requires the `workflow` scope to push files under `.github/workflows/`. Without it, `git push` will be rejected.

#### Step 6: Install Railway CLI

```bash
brew install railway
railway login
```

#### Step 7: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

### 2.3 Accounts Needed

| Service | URL | Purpose |
|---------|-----|---------|
| GitHub | [github.com](https://github.com) | Source code & CI/CD |
| Railway | [railway.app](https://railway.app) | Cloud deployment |
| LambdaTest / TestMu AI | [lambdatest.com](https://www.lambdatest.com) | KaneAI test generation |
| Anthropic | [console.anthropic.com](https://console.anthropic.com) | Claude Code API key |

---

## 3. Phase 1: Build the Flask Web Application

### 3.1 Overview

We build a single-page Flask app that serves as a **test target** — a page packed with interactive DOM elements that exercise common web automation patterns.

### 3.2 Project Initialization

```bash
mkdir -p python-robot-demo && cd python-robot-demo
```

### 3.3 Using Claude Code

Start Claude Code and describe what you want:

```bash
claude
```

Prompt:
> Create a Flask web app with rich, testable DOM elements: login form, counter, dropdowns, checkboxes, radio buttons, tabs, accordion, data table with sorting, dynamic AJAX content, modal dialog, toast notifications, alerts, file upload, and drag-and-drop. Include API endpoints for login, greeting, and search.

Claude Code will generate:

| File | Purpose |
|------|---------|
| `app.py` | Flask application with 3 API endpoints (`/api/login`, `/api/greet`, `/api/search`) |
| `templates/index.html` | Single page with 16 interactive sections, all with unique HTML IDs |
| `static/style.css` | Clean, modern styling for all components |

### 3.4 Application Structure

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

### 3.5 Verify Locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 and interact with every section.

> **Note:** macOS Monterey+ uses port 5000 for AirPlay Receiver. If the port is busy, either disable AirPlay in System Settings or modify `app.py` to use a different port.

---

## 4. Phase 2: Write Robot Framework Tests

### 4.1 Overview

Robot Framework is a keyword-driven test automation framework. We use it with SeleniumLibrary to write browser tests in a human-readable syntax.

### 4.2 Test Architecture

```
tests/
├── resources.robot        # Shared settings, variables, and keywords
└── web_tests.robot        # 20 test cases covering all UI sections
```

### 4.3 Shared Resources (`tests/resources.robot`)

This file defines:
- **Settings**: Import SeleniumLibrary
- **Variables**: `${URL}` (configurable), `${BROWSER}` (chrome), `${DELAY}` (0.1s)
- **Keywords**:
  - `Open Test Browser` — launches headless Chrome with standard flags
  - `Close Test Browser` — tears down all browser sessions
  - `Login With Credentials` — reusable login keyword accepting username/password
  - `Wait And Verify Text` — waits for element visibility then checks text content

### 4.4 Test Cases (`tests/web_tests.robot`)

| # | Test Case | What It Verifies |
|---|-----------|-----------------|
| 1 | Page Should Load Successfully | Title, heading text |
| 2 | Login With Valid Credentials | admin/password → "Welcome, admin!" |
| 3 | Login With Invalid Credentials | wrong/wrong → "Invalid credentials" |
| 4 | Remember Me Checkbox | Check/uncheck toggle |
| 5 | Counter Increment And Decrement | +++ = 3, then - = 2, reset = 0 |
| 6 | Color Dropdown Selection | Select "blue" → preview appears |
| 7 | Checkboxes | Multi-select, independent toggle |
| 8 | Radio Buttons | Mutual exclusion |
| 9 | Tab Switching | Tab 1 → Tab 2 → Tab 3 visibility |
| 10 | Accordion Toggle | Expand/collapse sections |
| 11 | Data Table Row Count | Initial count = 5 |
| 12 | Data Table Row Deletion | Delete row → count decreases |
| 13 | Greeting API | "Robot" → "Hello, Robot!" |
| 14 | Toggle Hidden Content | Show/hide toggle |
| 15 | Delayed Content Loading | 2s delay → content appears |
| 16 | Open And Close Modal | Open → close via X button |
| 17 | Modal Confirm | Input value → confirm → toast |
| 18 | Alerts Are Visible | All 3 alerts visible on load |
| 19 | Dismiss Alert | Warning alert hidden after click |
| 20 | Search Fruits | "app" → "Apple" in results |

### 4.5 Running Tests

```bash
# Against local app
robot --variable URL:http://localhost:5000 tests/

# Against deployed app
robot --variable URL:https://web-production-f7853.up.railway.app tests/

# With output directory
robot --variable URL:http://localhost:5000 --outputdir results tests/
```

**Test output files:**
- `report.html` — summary dashboard (open in browser)
- `log.html` — step-by-step execution log with screenshots on failure
- `output.xml` — machine-readable results for CI integration

---

## 5. Phase 3: Deploy to Railway

### 5.1 Overview

[Railway](https://railway.app) is a cloud platform that auto-detects Python apps and deploys them with minimal configuration.

### 5.2 Deployment Files

**`Procfile`** — tells Railway how to start the app:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

**`railway.json`** — deployment configuration:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**`requirements.txt`** — Python dependencies (Railway installs these automatically):
```
flask==3.1.0
gunicorn==23.0.0
robotframework==7.2
robotframework-seleniumlibrary==6.8.0
selenium==4.27.1
```

### 5.3 Deploy Steps

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   gh repo create flask-app-with-robot-tests --public --source=. --push
   ```

2. **Connect to Railway:**
   - Go to https://railway.app/new
   - Click **"Deploy from GitHub Repo"**
   - If your repo doesn't appear, go to GitHub Settings → Integrations → Applications → Railway → Configure, and grant access to the repo
   - Select **flask-app-with-robot-tests**
   - Railway auto-detects the Procfile and starts building

3. **Generate public URL:**
   - In Railway dashboard → click your service → Settings → Networking → Public Networking
   - Click **"Generate Domain"**
   - Your app is now live (e.g., `https://web-production-f7853.up.railway.app`)

4. **Verify deployment:**
   ```bash
   curl -s https://web-production-f7853.up.railway.app | head -5
   ```

### 5.4 Common Railway Issues

| Issue | Solution |
|-------|----------|
| Repo not visible in Railway | Grant Railway access in GitHub Settings → Applications → Railway → Configure |
| Build fails | Check Railway build logs; ensure `requirements.txt` is in the repo root |
| App crashes on start | Verify `Procfile` uses `gunicorn` and references `app:app` correctly |
| No public URL | Must manually generate a domain in Settings → Networking |

---

## 6. Phase 4: Set Up GitHub Actions CI/CD

### 6.1 Overview

GitHub Actions runs Robot Framework tests automatically on every push to `main`, against the deployed Railway app.

### 6.2 Workflow File (`.github/workflows/test.yml`)

```yaml
name: Robot Framework Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:          # Manual trigger

env:
  APP_URL: ${{ vars.APP_URL || 'http://localhost:5000' }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - uses: browser-actions/setup-chrome@v1
      - uses: nanasess/setup-chromedriver@v2
      - name: Start app (if testing locally)
        if: env.APP_URL == 'http://localhost:5000'
        run: python app.py & sleep 3
      - name: Run Robot Framework tests
        run: robot --variable URL:${{ env.APP_URL }} --outputdir results tests/
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: robot-results
          path: results/
```

### 6.3 Configuration

Set the `APP_URL` variable so tests run against Railway instead of localhost:

```bash
gh variable set APP_URL \
  --body "https://web-production-f7853.up.railway.app" \
  --repo skallidah/flask-app-with-robot-tests
```

### 6.4 Trigger and Monitor

```bash
# Trigger manually
gh workflow run test.yml --repo skallidah/flask-app-with-robot-tests

# Check status
gh run list --repo skallidah/flask-app-with-robot-tests --limit 1

# View in browser
open https://github.com/skallidah/flask-app-with-robot-tests/actions
```

### 6.5 Accessing Test Artifacts

After a CI run completes:
1. Go to the workflow run page in GitHub
2. Scroll to the **Artifacts** section
3. Download `robot-results` — contains `report.html`, `log.html`, and `output.xml`

---

## 7. Phase 5: Write Requirements for KaneAI

### 7.1 Overview

To use KaneAI for test generation, we need a structured requirements document that describes each feature and its acceptance criteria. This document (`REQUIREMENTS.md`) serves as the input for KaneAI's AI test generation.

### 7.2 Requirements Structure

Each feature follows this template:

```markdown
## Feature N: Feature Name

**Section:** UI section identifier

### Elements
- List of interactive elements

### Acceptance Criteria
- **AC-N.1:** When [action], then [expected result]
- **AC-N.2:** ...
```

### 7.3 Coverage

The requirements document covers all 16 features with 50+ acceptance criteria:

| Feature | ACs | Key Test Scenarios |
|---------|-----|--------------------|
| Login Form | 4 | Valid login, invalid login, remember me, required fields |
| Counter | 5 | Increment, decrement, reset, compound operations |
| Dropdowns | 3 | Single select with preview, multi-select |
| Checkboxes & Radios | 5 | Multi-check, independent toggle, radio exclusion |
| Tabs | 5 | Default state, switching, content visibility |
| Accordion | 4 | Collapse/expand, independent operation |
| Data Table | 5 | Row count, sorting (name/age), deletion, count update |
| Greeting API | 3 | Hidden initially, AJAX call, server response |
| Fruit Search | 4 | Live search, case-insensitive, result display |
| Toggle Content | 4 | Show/hide, button text change |
| Delayed Loading | 2 | Loading state, 2s delay completion |
| Modal Dialog | 7 | Open, close (3 ways), input, confirm with toast |
| Toasts | 5 | 3 types, animation, auto-dismiss |
| Alerts | 3 | Visibility, dismiss warning |
| File Upload | 2 | Hidden initially, file info display |
| Drag and Drop | 4 | Draggable items, drop zone, visual feedback |

### 7.4 Document Reference

Full document: [`REQUIREMENTS.md`](REQUIREMENTS.md)

---

## 8. Phase 6: Generate Tests with KaneAI

### 8.1 What is KaneAI?

KaneAI is TestMu AI's (by LambdaTest) AI-powered test generation tool. It can:
- Accept natural-language test scenarios
- Generate Selenium/Python test scripts
- Include vision-model-based assertions for visual validation
- Target LambdaTest's HyperExecute infrastructure

### 8.2 Steps to Generate Tests

1. **Log in** to [LambdaTest](https://www.lambdatest.com) and navigate to KaneAI
2. **Create a new test** and provide:
   - The application URL: `https://web-production-f7853.up.railway.app`
   - Test scenarios from `REQUIREMENTS.md` (e.g., AC-1.1 for valid login)
3. **KaneAI generates** Selenium/Python scripts with:
   - Step-by-step comments (`# Step - N : description`)
   - Selenium WebDriver interactions (`driver.get()`, `send_keys()`, `click()`)
   - Vision model placeholders for visual assertions
   - LambdaTest-specific helpers (`smartui_snapshot`, `get_element`)

### 8.3 Generated Scripts

KaneAI produced two scripts in this exercise:

**`kaneai_login_test_positive.py`** — 14 steps:
1. Navigate to the app URL
2. Verify page heading
3. Assert heading equals "Robot Framework Test Target"
4. Type "admin" in username field
5. Verify username field value
6. Assert username equals "admin"
7. Type "password" in password field
8–9. Vision model password verification
10. Click Login button
11–12. Check "Welcome, admin!" success banner
13–14. Verify success message visibility

**`kaneai_login_test_negative.py`** — 14 steps:
1–3. Same page load and heading verification
4–6. Type "invaliduser" in username field + verify
7–9. Type password + verify
10. Click Login button
11–14. Check "Invalid credentials" error message

### 8.4 KaneAI Script Characteristics

Understanding these patterns is critical for the migration:

| Pattern | Example | Handling |
|---------|---------|----------|
| Step comments | `# Step - 4 : Type admin in Username input field` | Parsed as test step metadata |
| Vision model placeholders | `'This Instruction Is Carried Out By The Vision Model'` | Replaced with SeleniumLibrary assertions |
| LambdaTest imports | `from lambdatest_selenium_driver import smartui_snapshot` | Removed (not needed for Robot Framework) |
| Multi-locator helpers | `get_element(driver, locators)` | Replaced with Robot Framework's built-in locator strategies |
| Action chains | `actions.move_to_element(element).click().perform()` | Replaced with `Click Button` keyword |

---

## 9. Phase 7: Build the MCP Server

### 9.1 What is MCP?

**Model Context Protocol (MCP)** is an open standard created by Anthropic that allows AI assistants to connect to external tools and data sources. It works like a plugin system for AI.

**Key concepts:**

| Concept | Description |
|---------|-------------|
| **MCP Host** | The AI application (e.g., Claude Code) that needs external capabilities |
| **MCP Server** | A lightweight program that exposes tools, resources, and prompts |
| **Tools** | Functions the AI can call (like API endpoints for the AI) |
| **Resources** | Data the AI can read (like a virtual filesystem) |
| **Transport** | Communication channel — **stdio** (local) or **SSE** (HTTP) |

**How it works:**
```
Claude Code                    MCP Server
    │                              │
    │──── Initialize ────────────►│
    │◄─── Capabilities ──────────│
    │                              │
    │──── Call Tool ─────────────►│
    │     (JSON-RPC request)       │
    │◄─── Tool Result ───────────│
    │     (JSON-RPC response)      │
```

### 9.2 Server Implementation

**File:** `mcp-server/server.py`

Built using the `FastMCP` framework from the official MCP Python SDK:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kaneai-to-robot")

@mcp.tool()
def analyze_kaneai_script(file_path: str) -> str:
    """Analyze a KaneAI script and extract structured test steps."""
    # ... parsing logic
```

### 9.3 Tools Provided

#### Tool 1: `list_kaneai_scripts`

Lists all KaneAI Python scripts available for migration.

**Input:** `scripts_dir` (optional, defaults to `kane-ai-generated/`)
**Output:** List of scripts with step counts and summaries

#### Tool 2: `analyze_kaneai_script`

Deep-analyzes a single KaneAI script.

**Input:** `file_path` (path to KaneAI .py file)
**Output:** Structured JSON with:
- Total steps and actionable steps count
- Step classification (navigate, input, click, assert, verify)
- Extracted data (URLs, field values, expected assertions)
- Vision model placeholder identification

#### Tool 3: `migrate_to_robot`

Converts a KaneAI script to a Robot Framework `.robot` file.

**Input:** `file_path`, optional `test_name`, `documentation`, `output_path`
**Output:** Generated `.robot` file + metadata

**Migration pipeline:**
1. Parse step comments (`# Step - N : description`)
2. Classify each step (navigate, input, click, assert, verify)
3. Extract data values (URLs, input text, expected values)
4. Map field descriptions → HTML ID locators
5. Map button descriptions → HTML ID locators
6. Map Selenium operations → SeleniumLibrary keywords
7. Map assertions → Robot Framework assertion keywords
8. Reuse `resources.robot` shared keywords
9. Write `.robot` file with proper formatting

**Mapping examples:**

| KaneAI Step | Robot Framework Keyword |
|-------------|------------------------|
| `driver.get("https://...")` | `Go To    ${URL}` |
| `element.send_keys('admin')` on Username | `Input Text    id:username    admin` |
| `actions.move_to_element(element).click()` on Login | `Click Button    id:login-btn` |
| Vision model: heading equals "X" | `Element Should Contain    id:page-title    X` |
| Vision model: success banner visible | `Wait Until Element Is Visible    id:login-message` |
| Vision model: error text equals "X" | `Wait And Verify Text    id:login-message    X` |

#### Tool 4: `list_robot_tests`

Lists all existing Robot Framework tests for context.

**Input:** `tests_dir` (optional, defaults to `tests/`)
**Output:** List of `.robot` files with their test case names and counts

### 9.4 Installation & Configuration

**Install dependencies:**
```bash
pip install "mcp[cli]"
```

**Claude Code configuration (`.mcp.json`):**
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

Place this file in the project root. Claude Code will automatically discover and connect to the MCP server when started in this directory.

**Global installation** (optional — available in all projects):
Add the same `mcpServers` block to `~/.claude/settings.json`.

### 9.5 Testing the Server Standalone

You can test the migration logic without Claude Code:

```python
python -c "
import sys; sys.path.insert(0, 'mcp-server')
from server import migrate_to_robot
result = migrate_to_robot('kane-ai-generated/kaneai_login_test_positive.py')
print(result)
"
```

---

## 10. Phase 8: Migrate KaneAI Scripts to Robot Framework

### 10.1 Running the Migration

Using the MCP server tools (or directly via Python):

```python
from server import migrate_to_robot

# Migrate positive login test
migrate_to_robot(
    'kane-ai-generated/kaneai_login_test_positive.py',
    test_name='KaneAI Login Valid Credentials',
    documentation='Migrated from KaneAI: tests login with valid admin/password credentials',
)

# Migrate negative login test
migrate_to_robot(
    'kane-ai-generated/kaneai_login_test_negative.py',
    test_name='KaneAI Login Invalid Credentials',
    documentation='Migrated from KaneAI: tests login with invalid credentials shows error',
)
```

### 10.2 Migration Results

**Input: `kaneai_login_test_positive.py` (132 lines of Selenium/Python)**

**Output: `tests/kaneai_login_test_positive.robot` (33 lines of Robot Framework)**

```robot
*** Settings ***
Resource    resources.robot
Suite Setup    Open Test Browser
Suite Teardown    Close Test Browser

*** Test Cases ***

KaneAI Login Valid Credentials
    [Documentation]    Migrated from KaneAI: tests login with valid admin/password credentials
    Go To    ${URL}
    Element Should Be Visible    id:page-title
    Element Should Contain    id:page-title    Robot Framework Test Target
    Input Text    id:username    admin
    Textfield Value Should Be    id:username    admin
    Input Text    id:password    password
    Click Button    id:login-btn
    Wait Until Element Is Visible    id:login-message    timeout=5s
    Wait And Verify Text    id:login-message    Welcome, admin!
    Element Should Be Visible    id:login-message
```

**Key transformations applied:**
- 132 lines of Selenium boilerplate → 33 lines of clean Robot Framework
- LambdaTest-specific code removed
- Vision model placeholders → concrete SeleniumLibrary assertions
- Hardcoded URL → `${URL}` variable (configurable)
- Reuses `resources.robot` keywords (`Wait And Verify Text`, `Open Test Browser`)

### 10.3 Before vs After Comparison

| Aspect | KaneAI (Selenium/Python) | Robot Framework |
|--------|--------------------------|-----------------|
| Lines of code | 132 | 33 |
| Readability | Low (boilerplate-heavy) | High (keyword-driven) |
| Portability | LambdaTest-specific | Any Selenium Grid / local |
| Maintainability | Inline helpers, try/except blocks | Shared keywords in `resources.robot` |
| Configuration | Hardcoded URL | Variable `${URL}` |
| Browser setup | Manual ChromeOptions | Handled by `Open Test Browser` keyword |
| Assertions | Vision model placeholders | Concrete SeleniumLibrary keywords |

---

## 11. Phase 9: Validate Everything End-to-End

### 11.1 Run All Tests Locally

```bash
# Start the app
python app.py &

# Run all 22 tests
robot --variable URL:http://localhost:5000 --outputdir results tests/
```

**Expected output:**
```
Tests                                                                 | PASS |
22 tests, 22 passed, 0 failed
```

### 11.2 Run Against Railway

```bash
robot --variable URL:https://web-production-f7853.up.railway.app --outputdir results tests/
```

### 11.3 Run GitHub Actions CI

```bash
# Trigger
gh workflow run test.yml --repo skallidah/flask-app-with-robot-tests

# Check result (wait ~90 seconds)
gh run list --repo skallidah/flask-app-with-robot-tests --limit 1
# Expected: completed  success
```

### 11.4 View Reports

```bash
open results/report.html
```

### 11.5 Final Commit & Push

```bash
git add .
git commit -m "Add MCP server and migrated KaneAI tests"
git push origin main
```

---

## Appendix A: Project File Reference

```
python-robot-demo/
├── app.py                                    # Flask application (3 API endpoints)
├── templates/
│   └── index.html                            # Single page with 16 interactive sections
├── static/
│   └── style.css                             # Styling for all components
├── tests/
│   ├── resources.robot                       # Shared keywords and variables
│   ├── web_tests.robot                       # 20 original test cases
│   ├── kaneai_login_test_positive.robot       # Migrated: valid login test
│   └── kaneai_login_test_negative.robot       # Migrated: invalid login test
├── kane-ai-generated/
│   ├── kaneai_login_test_positive.py          # KaneAI output: valid login
│   └── kaneai_login_test_negative.py          # KaneAI output: invalid login
├── mcp-server/
│   ├── server.py                             # MCP server (4 tools)
│   └── requirements.txt                      # MCP dependencies
├── .mcp.json                                 # Claude Code MCP configuration
├── .github/
│   └── workflows/
│       └── test.yml                          # GitHub Actions CI workflow
├── requirements.txt                          # Python dependencies
├── Procfile                                  # Railway deployment command
├── railway.json                              # Railway config
├── REQUIREMENTS.md                           # Feature requirements for KaneAI
├── WORKFLOW_SUMMARY.md                       # Workflow overview with diagrams
├── GUIDE.md                                  # This document
├── README.md                                 # Quick-start setup guide
└── .gitignore                                # Git ignore rules
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
| Port 5000 in use | macOS AirPlay Receiver | Disable in System Settings → General → AirDrop & Handoff |
| `pip` not found | Python not in PATH or venv not activated | Use `pip3` or activate venv: `source venv/bin/activate` |
| GitHub push rejected for workflows | OAuth token missing `workflow` scope | `gh auth login --web --scopes workflow` |
| Repo not visible in Railway | Railway GitHub app not authorized | GitHub Settings → Applications → Railway → Configure → add repo |
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

# Check Railway deployment status
railway status

# Check GitHub Actions status
gh run list --repo skallidah/flask-app-with-robot-tests --limit 5

# Test MCP server parsing
python -c "import sys; sys.path.insert(0,'mcp-server'); from server import list_kaneai_scripts; print(list_kaneai_scripts())"
```

---

## Appendix D: Glossary

| Term | Definition |
|------|-----------|
| **Claude Code** | Anthropic's CLI-based AI coding assistant that can generate, edit, and manage code |
| **Flask** | Lightweight Python web framework for building web applications |
| **GitHub Actions** | GitHub's built-in CI/CD platform for automating workflows |
| **Gunicorn** | Production-grade Python WSGI HTTP server |
| **KaneAI** | TestMu AI's (by LambdaTest) AI-powered test script generation tool |
| **MCP** | Model Context Protocol — open standard for connecting AI tools to external capabilities |
| **MCP Host** | The AI application that consumes MCP server capabilities (e.g., Claude Code) |
| **MCP Server** | A program that exposes tools, resources, and prompts over the MCP protocol |
| **Nixpacks** | Railway's build system that auto-detects project type and builds containers |
| **Railway** | Cloud platform-as-a-service (PaaS) for deploying web applications |
| **Robot Framework** | Open-source keyword-driven test automation framework |
| **Selenium** | Browser automation library for controlling web browsers programmatically |
| **SeleniumLibrary** | Robot Framework library that wraps Selenium for browser testing |
| **stdio** | Standard input/output — the communication transport used by local MCP servers |
| **Vision Model** | KaneAI's visual AI that performs assertions based on visual page analysis |

---

*This document was generated with Claude Code as part of an AI-assisted test automation pipeline exercise.*
