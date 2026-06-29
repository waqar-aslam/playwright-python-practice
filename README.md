# Playwright with Python - Automation Practice

A collection of Playwright automation scripts created while learning and practicing Playwright using Python.

This repository contains hands-on examples covering browser automation, UI interactions, synchronization techniques, and commonly used Playwright features. Each example focuses on a specific automation concept and serves as a quick reference for future projects and interview preparation.

## Tech Stack

- Python
- Playwright
- Pytest
- Visual Studio Code
- Git & GitHub

## Topics Covered

- Browser Launch
- Browser Contexts
- Page Navigation
- Locators
- CSS Selectors
- XPath Selectors
- Playwright Built-in Locators
- Assertions
- Synchronization
- Auto Waiting
- Handling Alerts
- Handling Child Windows / Popups
- Handling Multiple Pages
- Form Automation
- Checkboxes
- Radio Buttons
- Dropdowns
- Dynamic Elements
- Web Tables
- Frames (Iframes)
- File Upload
- Screenshots
- Test Organization with Pytest

## Repository Structure

```
PlaywrightTraining/
│
├── tests/
│   ├── basics/
│   ├── locators/
│   ├── alerts/
│   ├── windows/
│   └── waits/
│
├── requirements.txt
├── pytest.ini
├── README.md
└── conftest.py

Each Python file demonstrates one or more Playwright concepts with simple and easy-to-understand examples.

## Running the Tests

Clone the repository:

```bash
git clone https://github.com/<your-github-username>/<repository-name>.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest PlaceHolderDemo.py
```

Run in headed mode:

```bash
pytest --headed
```

## Purpose

This repository is maintained to:

- Learn Playwright with Python
- Practice UI Automation concepts
- Build reusable automation examples
- Prepare for QA Automation interviews
- Track continuous learning

## Author

**Waqar Aslam**

Lead QA Automation Engineer

Learning • Practicing • Sharing
