---
name: step-dev
description: Developer guide for the Step unified automation platform. Covers keyword development (Java, .NET, JS/TS), the Keyword API, Automation Packages, the YAML descriptor, Step CLI, Maven plugin, CI/CD integration, and local/remote execution. Use when building, debugging, deploying, or reviewing Step automation code — keywords, plans, packages, or anything involving step.dev, automation-package.yaml, the Step CLI, or the Keyword API. Also use when the user mentions load testing, synthetic monitoring, or RPA in the context of Step.
---

# Step Developer Guide

Step is a unified automation platform for testing, RPA, CI/CD, load testing, and synthetic monitoring. It lets developers define automation workflows as code alongside application code, package them as self-contained Automation Packages, and execute or deploy them locally or on a Step server.

**Always verify against the latest docs before presenting API details as fact.** Step evolves across versions. The reference files in this skill are based on the v29 documentation. Check the live docs when version-specific behavior matters.

- Documentation: https://step.dev/knowledgebase/
- Developer guide: https://step.dev/knowledgebase/categories/developer-guide/
- Tutorials: https://step.dev/tutorials
- GitHub samples: https://github.com/exense/step-samples

## When to use

- Developing custom keywords in Java, .NET, JavaScript, or TypeScript
- Writing or editing `automation-package.yaml` descriptors
- Setting up Automation Packages for load testing, synthetic monitoring, E2E tests, or RPA
- Using the Step CLI or Maven plugin to execute, deploy, or package automation
- Integrating Step into a CI/CD pipeline
- Running automation packages locally with JUnit
- Working with Step plans, parameters, schedules, or alerting rules
- Debugging keyword lifecycle issues (hooks, sessions, error handling, measurements)
- Choosing between stateful and stateless keyword patterns
- Any time the user mentions Step (step.dev), Keywords, Automation Packages, or the Step CLI

## Core concepts

These are the building blocks you need to understand before diving into any reference file.

### Keywords

Keywords are the fundamental building blocks of Plans. They encapsulate automation logic — anything from a single API call to a full browser-driven workflow. Step integrates natively with Selenium, Cypress, Playwright, Appium, JMeter, K6, and others, but also supports custom keywords in Java, .NET, and JavaScript/TypeScript via the Keyword API.

Key characteristics:

- **Stateless by default** — a new instance is created per execution, released afterward
- **Stateful via sessions** — share data across keyword executions within a workflow using the session object
- **Lifecycle hooks** — optional `beforeKeyword`, `afterKeyword`, and `onError` hooks for setup, cleanup, and error handling

### Automation Packages

An Automation Package is a self-contained bundle of Plans, Keywords, Parameters, Schedules, Resources, and Alerting Rules. Defined declaratively in `automation-package.yaml`, packages can be executed locally, executed remotely in isolation, or deployed to a Step server.

Supported formats: JAR (Java), ZIP, Folder (CLI only), DLL (.NET)

### Plans

Plans define the operational logic — what Step actually executes. They are tree structures composed of controls (sequence, threadGroup, forEach, callKeyword, etc.) and can be defined in YAML, the visual editor, or as plain text.

### Step CLI and Maven plugin

The CLI (`step ap execute`, `step ap deploy`) and Maven plugin handle packaging, local/remote execution, and deployment to Step servers. The CLI works with folders, ZIPs, JARs, and Maven artifact coordinates.

## Load the right references

Read only what you need for the task at hand.

- Read `references/keywords.md` for keyword development concepts, the Keyword API across all languages, inputs/outputs, hooks, sessions, measurements, error handling, and the Keyword Proxy
  - *Triggers: keyword, AbstractKeyword, @Keyword, keyword API, beforeKeyword, afterKeyword, onError, session, output.add, OutputBuilder, measurements, startMeasure, live reporting, keyword proxy, stateful, stateless*

- Read `references/automation-packages.md` for Automation Package structure, the YAML descriptor syntax, keyword/plan/parameter/schedule/alerting-rule declarations, fragment files, and IDE setup
  - *Triggers: automation-package.yaml, automation package, YAML descriptor, plans, parameters, schedules, alerting rules, fragments, threadGroup, callKeyword, testScenario, testCase, deploy, package format, JAR layout, ZIP layout*

- Read `references/cli-and-deployment.md` for the Step CLI, Maven plugin, local/remote execution, deployment, CI/CD integration, library management, JUnit integration, and execution parameters
  - *Triggers: step CLI, step ap execute, step ap deploy, maven plugin, CI/CD, local execution, remote execution, JUnit, StepJUnit5, deploy automation package, execute automation package, stepcli.properties, artifact repository, library, filtering plans*

## Anti-patterns

- Writing keywords that create resources (browsers, connections, file handles) without cleanup — implement cleanup in `afterKeyword` or use try/finally
- Storing large objects in sessions when stateless keywords would suffice — sessions persist across a workflow group and consume memory
- Declaring all entities in Java annotations when YAML is cleaner — YAML is language-agnostic and works across all keyword types
- Hardcoding environment-specific values instead of using Step Parameters with activation scripts
- Skipping local execution — always test keywords locally (JUnit for Java, runner for Node.js) before deploying to a Step server
- Using `automation-package.yaml` without setting the `version` field — this breaks forward compatibility when Step upgrades the schema

## Response expectations

- For keyword development questions, provide language-specific examples (Java, .NET, or JS/TS) based on what the user is working with
- For YAML descriptor questions, show concrete `automation-package.yaml` snippets
- For CLI questions, show the exact command with required flags
- For architecture questions, help users decide between stateless vs stateful keywords, single vs modular keyword design, and YAML vs code-based entity declaration
- When uncertain about version-specific behavior, point the user to the relevant live doc URL
