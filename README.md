# PR Guardian : AI-Powered Pull Request Review Assistant

**PR Guardian** is a successfully implemented AI-powered code review automation system that analyzes GitHub Pull Request (PR) diffs using Anthropic's Claude API and delivers structured, evidence-backed review findings directly to Slack.

The system integrates GitHub Actions, GitHub REST APIs, Claude, and Slack to automate preliminary code reviews. It identifies potential defects in code changes, highlights affected lines, assigns severity levels, and provides actionable suggestions for improvement.

PR Guardian streamlines the code review process by providing developers with automated feedback whenever an eligible pull request is opened.

## 1. Motivation

Code reviews are an essential part of software development, helping teams maintain code quality, identify defects, and prevent regressions. However, manually reviewing every change can become time-consuming as development activity increases.

PR Guardian was developed to automate the initial stage of this process by integrating Large Language Models (LLMs) into an existing GitHub development workflow.

The system addresses three key engineering requirements:

- **Automated Code Analysis:** Analyzes pull request diffs using Claude to identify potential bugs and problematic code changes.
- **Evidence-Based Feedback:** Generates structured findings containing affected file paths, line references, supporting evidence, severity levels, and suggested fixes.
- **Secure Workflow Automation:** Processes untrusted pull request changes without executing contributor-supplied code, while maintaining restricted GitHub permissions.

## 2. System Architecture

PR Guardian implements an event-driven architecture using GitHub Actions as the workflow orchestration layer.

When an eligible pull request event occurs, the workflow retrieves the associated changes through GitHub's REST API, passes textual patches to Claude for analysis, validates the generated findings, and publishes the final review to Slack.

### Architecture Flow

<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/32994cd5-bb16-45f2-9868-c8ca551716ec" />

### Component Responsibilities

| Component | Implementation |
|---|---|
| GitHub Actions | Automates and orchestrates the review workflow |
| GitHub REST API | Retrieves pull request metadata and paginated file patches |
| Diff Processing | Extracts textual changes and enforces input size constraints |
| Anthropic Claude API | Analyzes code changes and generates structured findings |
| Pydantic | Validates review output and enforces evidence requirements |
| Slack Webhooks | Delivers formatted code review reports |

## 3. Implementation Highlights

- Implemented an automated pull request review pipeline triggered through GitHub Actions.
- Integrated GitHub REST APIs to retrieve pull request metadata and paginated file-level diffs.
- Integrated Anthropic Claude for AI-assisted code analysis and structured review generation.
- Implemented Pydantic-based validation to enforce response schemas and verify findings against actual patch evidence.
- Added changed-line validation to ensure reported findings reference relevant added lines.
- Integrated Slack Incoming Webhooks to deliver review summaries and actionable recommendations.
- Implemented configurable diff-size limits to control the amount of code submitted for analysis.

## Screenshot
<img width="1860" height="845" alt="image" src="https://github.com/user-attachments/assets/a1fba96c-ec86-415f-9a12-40438b4ae97a" />

## 4. Security and Reliability

Security was incorporated into the workflow design to ensure that automated reviews do not require executing untrusted pull request code.

Key safeguards include:

- **Trusted Base Checkout:** Checks out the trusted base revision rather than executing contributor-supplied pull request code.
- **Read-Only Permissions:** Restricts GitHub Actions permissions to the access required for retrieving pull request information.
- **Restricted Trigger Conditions:** Limits automated execution to eligible same-repository pull requests opened by the repository owner.
- **Credential Management:** Uses GitHub Actions Secrets for API credentials and webhook URLs.
- **Input Constraints:** Enforces configurable patch-size limits before submitting content for AI analysis.
- **Evidence Validation:** Checks generated findings against the actual pull request patch before delivering review results.

The system operates as a review assistant and does not automatically approve, reject, or merge pull requests.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Application development and review orchestration |
| Anthropic Claude API | AI-powered code analysis |
| GitHub REST API | Pull request data retrieval |
| GitHub Actions | Event-driven workflow automation |
| Pydantic | Structured data and evidence validation |
| Slack Incoming Webhooks | Review report delivery |

## 6. Review Output

PR Guardian generates concise and actionable review reports containing identified issues, severity classifications, affected source locations, and suggested fixes.

Example:

```text
PR Guardian review: Guard averages

An empty list can fail.

HIGH — src/maths.py:2

Division by zero is possible.

Suggested fix:
Return early for an empty list.

Complexity: low
```

## 7. Project Limitations

The implemented system has the following limitations:

- Reviews are based on textual patches retrieved through GitHub's API. Binary and oversized diffs are not analyzed.
- Analysis is primarily patch-based and may not identify issues requiring extensive repository-wide context.
- Evidence and changed-line requirements can exclude valid findings involving unchanged code.
- Pull request content is processed through Anthropic's API, and review reports are delivered through Slack.
- AI-generated findings require human verification and are not guaranteed to identify every defect correctly.

## 8. Engineering Skills Demonstrated

- Backend application development using Python.
- REST API integration and paginated data retrieval.
- LLM integration and structured AI response handling.
- Data validation and evidence verification using Pydantic.
- Event-driven automation and CI/CD workflows.
- Secure handling of untrusted external inputs.
- API credential management and least-privilege access control.
- Third-party service integration using Slack Webhooks.

**Project:** PR Guardian  
**Domain:** AI-Assisted Developer Tools  
**Language:** Python  
**AI Model Provider:** Anthropic Claude  
**Automation:** GitHub Actions
