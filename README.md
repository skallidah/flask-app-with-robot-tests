# Python Robot Framework Demo

A Flask web app with rich DOM elements, designed as a test target for Robot Framework browser automation.

## Mac Setup (from scratch)

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3

```bash
brew install python
```

Verify:

```bash
python3 --version
pip3 --version
```

### 3. Install Google Chrome

Download from https://www.google.com/chrome/ or:

```bash
brew install --cask google-chrome
```

### 4. Install ChromeDriver

```bash
brew install --cask chromedriver
```

On first run, macOS may block ChromeDriver. Allow it:

```bash
xattr -d com.apple.quarantine $(which chromedriver)
```

Verify ChromeDriver matches your Chrome version:

```bash
chromedriver --version
google-chrome --version   # or check Chrome > About Google Chrome
```

If versions don't match, `brew upgrade --cask chromedriver`.

### 5. Create a virtual environment (recommended)

```bash
cd python-robot-demo
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** — web framework
- **gunicorn** — production WSGI server (used by Railway)
- **robotframework** — test automation framework
- **robotframework-seleniumlibrary** — browser automation for Robot Framework
- **selenium** — WebDriver bindings for Python

## Running the App Locally

```bash
python app.py
```

Open http://localhost:5000 in your browser. You should see the test target page with all interactive elements.

## Running Robot Framework Tests Locally

With the app running in one terminal, open another terminal and run:

```bash
source venv/bin/activate   # if using a virtual environment
robot --variable URL:http://localhost:5000 tests/
```

Test results are written to the current directory:
- `report.html` — human-readable report (open in browser)
- `log.html` — detailed execution log
- `output.xml` — machine-readable results

To write results to a separate directory:

```bash
robot --variable URL:http://localhost:5000 --outputdir results tests/
```

## Running Tests Against Deployed App

```bash
robot --variable URL:https://your-app.up.railway.app tests/
```

## Deploy to Railway

### Prerequisites

```bash
brew install railway
railway login
```

### Deploy

1. Push this repo to GitHub
2. Connect the repo in [Railway](https://railway.app)
3. Railway auto-detects the `Procfile` and deploys
4. Set `APP_URL` as a GitHub Actions variable to your Railway URL

Or deploy directly via CLI:

```bash
railway init
railway up
```

## CI/CD

GitHub Actions runs Robot Framework tests on every push to `main`. Test results are uploaded as artifacts.

## Troubleshooting

**ChromeDriver version mismatch**: Chrome and ChromeDriver must be the same major version. Update both:
```bash
brew upgrade --cask google-chrome chromedriver
```

**macOS blocks ChromeDriver**: Run:
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```

**Port 5000 already in use**: macOS Monterey+ uses port 5000 for AirPlay Receiver. Either disable it in System Settings > General > AirDrop & Handoff, or run the app on a different port:
```bash
python app.py  # edit app.py to change port, or:
flask run --port 5001
```

**`pip` not found**: Use `pip3` instead, or make sure your virtual environment is activated.
