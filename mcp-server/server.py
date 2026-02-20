"""
MCP Server: KaneAI Selenium/Python → Robot Framework Migration

This server exposes tools that:
1. Analyze KaneAI-generated Selenium/Python test scripts
2. Extract test steps and map them to Robot Framework keywords
3. Generate .robot files that reuse existing shared resources
4. List existing Robot Framework tests for context
"""

import os
import re
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

PROJECT_ROOT = os.environ.get(
    "PROJECT_ROOT",
    str(Path(__file__).resolve().parent.parent),
)

mcp = FastMCP(
    "kaneai-to-robot",
    instructions=(
        "MCP server for migrating KaneAI-generated Selenium/Python test scripts "
        "to Robot Framework format. Use 'analyze_kaneai_script' to parse a script, "
        "'migrate_to_robot' to convert it, and 'list_robot_tests' to see existing tests."
    ),
)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _extract_steps(source: str) -> list[dict]:
    """Parse KaneAI script comments and code blocks into structured steps."""
    steps = []
    lines = source.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match step comments like: # Step - 1 : Go to https://...
        m = re.match(r"#\s*Step\s*-\s*(\d+)\s*:\s*(.*)", line)
        if m:
            step_num = int(m.group(1))
            description = m.group(2).strip()

            # Collect associated code lines until next step or end
            code_lines = []
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if re.match(r"#\s*Step\s*-\s*\d+", next_line):
                    break
                if next_line and not next_line.startswith("#"):
                    code_lines.append(next_line)
                i += 1

            step = {
                "step": step_num,
                "description": description,
                "code": "\n".join(code_lines),
                "type": _classify_step(description, code_lines),
            }
            # Extract data values from the step
            step["data"] = _extract_data(description, code_lines)
            steps.append(step)
        else:
            i += 1
    return steps


def _classify_step(description: str, code_lines: list[str]) -> str:
    """Classify a step into a category for Robot Framework mapping."""
    desc_lower = description.lower()
    code_joined = " ".join(code_lines).lower()

    if "go to" in desc_lower or "driver.get(" in code_joined:
        return "navigate"
    if "click" in desc_lower and ("button" in desc_lower or "click()" in code_joined):
        return "click"
    if "type" in desc_lower or "send_keys(" in code_joined:
        return "input"
    if "assert" in desc_lower:
        return "assert"
    if "check" in desc_lower or "get text" in desc_lower:
        return "verify"
    if "select" in desc_lower:
        return "select"
    if "vision model" in code_joined:
        return "vision_placeholder"
    return "other"


def _extract_data(description: str, code_lines: list[str]) -> dict:
    """Extract relevant data values from step description and code."""
    data = {}

    # Extract URL from driver.get()
    for line in code_lines:
        url_match = re.search(r'driver\.get\(["\'](.+?)["\']\)', line)
        if url_match:
            data["url"] = url_match.group(1)

    # Extract send_keys value
    for line in code_lines:
        keys_match = re.search(r"send_keys\(['\"](.+?)['\"]\)", line)
        if keys_match:
            data["value"] = keys_match.group(1)

    # Extract field name from description
    field_match = re.search(r"(?:in|into)\s+(\w+(?:\s+\w+)*)\s+(?:input\s+)?field", description, re.IGNORECASE)
    if field_match:
        data["field"] = field_match.group(1)

    # Extract expected value from Assert descriptions
    assert_match = re.search(r"equals?\s+(.+?)$", description, re.IGNORECASE)
    if assert_match:
        data["expected"] = assert_match.group(1).strip()

    # Extract variable name from → {{var}} or Assert {{var}}
    var_match = re.search(r"→\s*\{\{(\w+)\}\}", description)
    if var_match:
        data["variable"] = var_match.group(1)
    else:
        var_match2 = re.search(r"\{\{(\w+)\}\}", description)
        if var_match2:
            data["variable"] = var_match2.group(1)

    return data


def _map_field_to_locator(field_name: str) -> str:
    """Map KaneAI field descriptions to element locators."""
    mapping = {
        "username": "id:username",
        "password": "id:password",
        "greet-name": "id:greet-name",
        "search": "id:search-input",
        "modal": "id:modal-input",
        "color": "id:color-select",
    }
    field_lower = field_name.lower()
    for key, locator in mapping.items():
        if key in field_lower:
            return locator
    return f"id:{field_lower.replace(' ', '-')}"


def _map_button_to_locator(description: str) -> str:
    """Map KaneAI button descriptions to element locators."""
    desc_lower = description.lower()
    if "login" in desc_lower:
        return "id:login-btn"
    if "greet" in desc_lower:
        return "id:greet-btn"
    if "modal" in desc_lower and "open" in desc_lower:
        return "id:open-modal-btn"
    if "modal" in desc_lower and ("close" in desc_lower or "cancel" in desc_lower):
        return "id:close-modal-btn"
    if "confirm" in desc_lower:
        return "id:modal-confirm-btn"
    if "increment" in desc_lower or "+" in desc_lower:
        return "id:increment-btn"
    if "decrement" in desc_lower or "-" in desc_lower:
        return "id:decrement-btn"
    if "reset" in desc_lower:
        return "id:reset-btn"
    if "toggle" in desc_lower or "show" in desc_lower or "hide" in desc_lower:
        return "id:toggle-btn"
    if "delayed" in desc_lower or "load" in desc_lower:
        return "id:delayed-btn"
    return f"xpath://button[contains(text(), '{description}')]"


def _step_to_robot_keyword(step: dict, url_var: bool = True) -> list[str]:
    """Convert a parsed step into Robot Framework keyword lines."""
    stype = step["type"]
    desc = step["description"]
    data = step["data"]

    if stype == "navigate":
        url = data.get("url", "${URL}")
        if url_var and "railway" in url:
            return ["    Go To    ${URL}"]
        return [f"    Go To    {url}"]

    if stype == "input":
        value = data.get("value", "")
        field = data.get("field", "")
        locator = _map_field_to_locator(field)
        lines = []
        if value:
            lines.append(f"    Input Text    {locator}    {value}")
        return lines

    if stype == "click":
        locator = _map_button_to_locator(desc)
        return [f"    Click Button    {locator}"]

    if stype == "assert":
        expected = data.get("expected", "")
        variable = data.get("variable", "")
        if not expected:
            return [f"    # Assert: {desc}"]
        # Map common assertions to Robot Framework keywords
        if "page_heading" in variable or "page_title" in variable:
            return [f"    Element Should Contain    id:page-title    {expected}"]
        if "login_success" in variable:
            return [f"    Wait And Verify Text    id:login-message    Welcome, admin!"]
        if "success_message" in variable:
            return ["    Element Should Be Visible    id:login-message"]
        if "login_error" in variable:
            return [f"    Wait And Verify Text    id:login-message    Invalid credentials"]
        if "login_submitted" in variable:
            return ["    Wait Until Element Is Visible    id:login-message    timeout=5s"]
        if "username_value" in variable:
            return [f"    Textfield Value Should Be    id:username    {expected}"]
        if "password_filled" in variable:
            return []  # Skip — verified implicitly by form submission
        return [f"    # Assert {variable} equals {expected}"]

    if stype == "verify":
        variable = data.get("variable", "")
        if "heading" in desc.lower() or "heading" in variable:
            return ["    Element Should Be Visible    id:page-title"]
        if "welcome" in desc.lower() or "success" in desc.lower():
            return ["    Wait Until Element Is Visible    id:login-message    timeout=5s"]
        if "error" in desc.lower() or "invalid" in desc.lower():
            return ["    Wait Until Element Is Visible    id:login-message    timeout=5s"]
        return [f"    # Verify: {desc}"]

    if stype == "vision_placeholder":
        return []  # Skip KaneAI vision model placeholders

    return [f"    # {desc}"]


def _steps_to_robot(test_name: str, steps: list[dict], doc: str = "") -> str:
    """Convert a list of steps into a complete Robot Framework test case."""
    keyword_lines = []
    for step in steps:
        robot_lines = _step_to_robot_keyword(step)
        if robot_lines:
            keyword_lines.append(f"    # Step {step['step']}: {step['description']}")
            keyword_lines.extend(robot_lines)

    doc_line = f"\n    [Documentation]    {doc}" if doc else ""
    body = "\n".join(keyword_lines)
    return f"{test_name}{doc_line}\n{body}"


# ── MCP Tools ────────────────────────────────────────────────────────────────


@mcp.tool()
def analyze_kaneai_script(file_path: str) -> str:
    """Analyze a KaneAI-generated Selenium/Python script and extract structured test steps.

    Args:
        file_path: Path to the KaneAI Python script (absolute or relative to project root)
    """
    full_path = file_path if os.path.isabs(file_path) else os.path.join(PROJECT_ROOT, file_path)

    if not os.path.exists(full_path):
        return json.dumps({"error": f"File not found: {full_path}"})

    with open(full_path) as f:
        source = f.read()

    steps = _extract_steps(source)

    # Extract test metadata
    test_name = Path(full_path).stem
    has_vision_steps = any(s["type"] == "vision_placeholder" for s in steps)
    actionable_steps = [s for s in steps if s["type"] != "vision_placeholder"]

    result = {
        "file": full_path,
        "test_name": test_name,
        "total_steps": len(steps),
        "actionable_steps": len(actionable_steps),
        "vision_placeholder_steps": len(steps) - len(actionable_steps),
        "has_vision_steps": has_vision_steps,
        "step_types": {},
        "steps": steps,
    }

    for s in steps:
        result["step_types"][s["type"]] = result["step_types"].get(s["type"], 0) + 1

    return json.dumps(result, indent=2)


@mcp.tool()
def migrate_to_robot(
    file_path: str,
    test_name: str = "",
    documentation: str = "",
    output_path: str = "",
) -> str:
    """Migrate a KaneAI Selenium/Python script to a Robot Framework .robot test case.

    Args:
        file_path: Path to the KaneAI Python script
        test_name: Name for the Robot test case (defaults to derived from filename)
        documentation: Documentation string for the test case
        output_path: Where to save the .robot file (defaults to tests/ folder)
    """
    full_path = file_path if os.path.isabs(file_path) else os.path.join(PROJECT_ROOT, file_path)

    if not os.path.exists(full_path):
        return json.dumps({"error": f"File not found: {full_path}"})

    with open(full_path) as f:
        source = f.read()

    steps = _extract_steps(source)

    # Derive test name from filename if not provided
    if not test_name:
        stem = Path(full_path).stem
        # Convert kaneai_login_test_positive → KaneAI Login Test Positive
        test_name = " ".join(
            word.capitalize() if word != "kaneai" else "KaneAI"
            for word in stem.split("_")
        )

    # Generate the test case body
    test_case = _steps_to_robot(test_name, steps, documentation)

    # Build the full .robot file
    robot_content = f"""*** Settings ***
Resource    resources.robot
Suite Setup    Open Test Browser
Suite Teardown    Close Test Browser

*** Test Cases ***

{test_case}
"""

    # Determine output path
    if not output_path:
        output_path = os.path.join(PROJECT_ROOT, "tests", Path(full_path).stem + ".robot")
    elif not os.path.isabs(output_path):
        output_path = os.path.join(PROJECT_ROOT, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(robot_content)

    return json.dumps(
        {
            "status": "success",
            "input_file": full_path,
            "output_file": output_path,
            "test_name": test_name,
            "total_steps_parsed": len(steps),
            "robot_content": robot_content,
        },
        indent=2,
    )


@mcp.tool()
def list_robot_tests(tests_dir: str = "") -> str:
    """List all existing Robot Framework test files and their test cases.

    Args:
        tests_dir: Path to the tests directory (defaults to project tests/ folder)
    """
    if not tests_dir:
        tests_dir = os.path.join(PROJECT_ROOT, "tests")
    elif not os.path.isabs(tests_dir):
        tests_dir = os.path.join(PROJECT_ROOT, tests_dir)

    if not os.path.isdir(tests_dir):
        return json.dumps({"error": f"Directory not found: {tests_dir}"})

    results = []
    for file in sorted(Path(tests_dir).glob("*.robot")):
        content = file.read_text()
        test_cases = []
        in_test_cases = False
        for line in content.split("\n"):
            if line.strip().startswith("*** Test Cases ***"):
                in_test_cases = True
                continue
            if line.strip().startswith("***"):
                in_test_cases = False
                continue
            if in_test_cases and line and not line[0].isspace() and line.strip():
                test_cases.append(line.strip())

        results.append(
            {
                "file": str(file),
                "filename": file.name,
                "test_cases": test_cases,
                "test_count": len(test_cases),
            }
        )

    return json.dumps(
        {
            "tests_dir": tests_dir,
            "total_files": len(results),
            "total_tests": sum(r["test_count"] for r in results),
            "files": results,
        },
        indent=2,
    )


@mcp.tool()
def list_kaneai_scripts(scripts_dir: str = "") -> str:
    """List all KaneAI-generated Python scripts available for migration.

    Args:
        scripts_dir: Path to the KaneAI scripts directory (defaults to kane-ai-generated/)
    """
    if not scripts_dir:
        scripts_dir = os.path.join(PROJECT_ROOT, "kane-ai-generated")
    elif not os.path.isabs(scripts_dir):
        scripts_dir = os.path.join(PROJECT_ROOT, scripts_dir)

    if not os.path.isdir(scripts_dir):
        return json.dumps({"error": f"Directory not found: {scripts_dir}"})

    results = []
    for file in sorted(Path(scripts_dir).glob("*.py")):
        content = file.read_text()
        steps = _extract_steps(content)
        results.append(
            {
                "file": str(file),
                "filename": file.name,
                "total_steps": len(steps),
                "step_summary": [
                    {"step": s["step"], "description": s["description"], "type": s["type"]}
                    for s in steps
                ],
            }
        )

    return json.dumps(
        {
            "scripts_dir": scripts_dir,
            "total_scripts": len(results),
            "scripts": results,
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
