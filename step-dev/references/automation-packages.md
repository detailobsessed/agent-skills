# Automation Packages and YAML Descriptor

> Live docs:
> - Automation Packages overview: https://step.dev/knowledgebase/devops/automation-packages-overview/
> - Automation Package Descriptor: https://step.dev/knowledgebase/devops/automation-package-yaml/
> - Automation Package in Java: https://step.dev/knowledgebase/devops/automation-package-java/
> - Automation Package Libraries: https://step.dev/knowledgebase/devops/automation-package-libraries/
> - Multi-version support: https://step.dev/knowledgebase/devops/automation-package-multi-version/
> - Getting started: https://step.dev/knowledgebase/devops/getting-started-with-automation-packages/

## Table of contents

1. [What is an Automation Package](#what-is-an-automation-package)
2. [Supported entities](#supported-entities)
3. [Package operations](#package-operations)
4. [Package formats and layout](#package-formats-and-layout)
5. [YAML descriptor](#yaml-descriptor)
6. [Keywords in YAML](#keywords-in-yaml)
7. [Plans in YAML](#plans-in-yaml)
8. [Parameters](#parameters)
9. [Schedules](#schedules)
10. [Notification presets and alerting rules](#notification-presets-and-alerting-rules)
11. [Fragment files](#fragment-files)
12. [Java-specific declarations](#java-specific-declarations)
13. [Package sources](#package-sources)
14. [Automation Package Libraries](#automation-package-libraries)
15. [IDE setup](#ide-setup)

---

## What is an Automation Package

An Automation Package is a self-contained set of Plans and their related entities (Keywords, Parameters, Resources, Schedules, Alerting Rules) that can be executed on a Step controller or deployed to it for later use.

The standard consists of:
- **Automation Package syntax** — a declarative YAML format for describing automation workflows
- **Automation Package format** — a standard for packaging entities (JAR, ZIP, Folder, DLL)
- **Automation Package CLI** — tools to build, execute, and deploy packages

---

## Supported entities

| Entity | Description |
|---|---|
| **Keywords** | Encapsulate automation logic — the building blocks of plans |
| **Plans** | Define the operational logic Step performs |
| **Parameters** | Key/value pairs for modular, environment-specific workflows |
| **Schedules** | Define periodic plan executions (cron-based) |
| **Resources** | Bundled data — Excel/CSV files, script files, etc. |
| **Notification Presets** | Define how to send notifications (email, webhook) |
| **Alerting Rules** | React to execution events with notifications or incident management |

---

## Package operations

| Operation | Description |
|---|---|
| **Package** | Create an archive from the entities (bundling step) |
| **Publish** | Upload to an artifact repository without further action |
| **Deploy** | Upload to a Step server, make all entities available, activate schedules and alerting rules |
| **Execute** | One-off execution in a temporary isolated context — content is not permanently deployed |

---

## Package formats and layout

### JAR (Java)

Standard JAR containing compiled Java classes, dependencies, and `automation-package.yaml` at the root. Built with Maven or any Java build tool.

```
META-INF/              # jar metadata
step/                  # Java classes - keywords
org/                   # Java classes - dependencies
automation-package.yaml
```

### ZIP

Standard ZIP archive with `automation-package.yaml` at the root plus any referenced resources.

```
automation-package.yaml
Demo_JMeter.jmx        # JMeter test plan
opencart-test.js        # K6 script
```

### Folder (exploded)

Raw directory structure — supported only by the Step CLI.

### DLL (.NET)

Single DLL file with keywords declared via `[Keyword]` annotation. Additional dependencies can be bundled as a ZIP library. YAML descriptors are not yet supported for .NET packages.

---

## YAML descriptor

The automation package is defined in `automation-package.yaml`. Top-level fields:

```yaml
---
version: 1.0.0          # schema version — required for forward compatibility
name: "my-package"       # unique identifier — updates existing package with same name on deploy
keywords:                # optional
plans:                   # optional
parameters:              # optional
schedules:               # optional
notificationPresets:     # optional
alertingRules:           # optional
fragments:               # optional (include modular YAML files)
```

### Schema versions

| Version | Description | Step compatibility |
|---|---|---|
| 1.2.0 | Password-protected data sources and Excel files | 29.x+ |
| 1.1.1 | K6 directory support | 28.x+ |
| 1.1.0 | Before & after sections in plans | 27.x |
| 1.0.0 | Initial version | 24.x–26.x |

Always set the `version` field explicitly to maintain forward compatibility.

---

## Keywords in YAML

All Step keyword types are supported except Astra, QF Test, and PDF Test. Java keywords declared with `@Keyword` in code are automatically included and do not need YAML declarations.

### JMeter

```yaml
keywords:
  - JMeter:
      name: "JMeter keyword from automation package"
      description: "JMeter keyword 1"
      jmeterTestplan: "jmeterProject1/jmeterProject1.xml"
```

### Cypress

```yaml
keywords:
  - Cypress:
      name: eCommerce - Typical visit
      cypressProject: cypress-test/
      spec: "opencart.cy.js"
```

### Grafana K6

```yaml
keywords:
  - K6:
      name: 'OpenCart home'
      scriptFile: "opencart-test.js"
      vus: 1
      iterations: 1
```

- `scriptFile` — relative path to the K6 script
- `scriptDirectory` (optional) — directory containing the script and local modules. All required modules must reside within this directory
- `vus` (optional) — concurrent virtual users
- `iterations` (optional) — total iterations across all VUs

### .NET

```yaml
keywords:
  - DotNet:
      name: "Open_Chrome_and_search_in_Google"
      dllFile: "DotNet/SeleniumKeywords.dll"
      librariesFile: "DotNet/AllDlls.zip"
```

### Node.js (JavaScript / TypeScript)

```yaml
keywords:
  - Node:
      name: MyNodeKeyword
      jsfile: nodejs-keywords/
```

The referenced project should contain `package.json` and keyword definitions in `keywords/`.

### Composite keywords

```yaml
keywords:
  - Composite:
      name: "Composite Keyword"
      plan:
        root:
          sequence:
            children:
              - echo:
                  text: "In Composite keyword"
              - return:
                  output:
                    - compositeOutput: "Composite Keyword output value"
```

---

## Plans in YAML

Plans are tree structures with a required `root` node defining the plan type. Common node properties:
- `nodeName` (optional) — node name
- `categories` (optional) — categories for filtering
- `description` (optional) — description text
- `children` (optional) — child nodes

### Basic plan

```yaml
plans:
  - name: "Simple plan"
    categories:
      - "FunctionalTests"
    root:
      testCase:
        children:
          - callKeyword:
              keyword: "My Keyword"
```

### Keyword call with inputs and routing

```yaml
- callKeyword:
    keyword: "My Keyword"
    inputs:
      - myInputNumber: 1
      - myInputBoolean: true
      - myInputString: "some input"
    routing:
      - agentOS: "windows"
```

### Thread group (load testing)

With literal values:
```yaml
- threadGroup:
    users: 5
    iterations: 10
    children:
      - callKeyword:
          keyword: "OpenCart home"
```

With dynamic expressions (Groovy):
```yaml
- threadGroup:
    users:
      expression: "nbUsers"
    iterations:
      expression: "nbIterations"
```

### Full load test example

```yaml
---
version: 1.0.0
name: "load-testing-k6-automation-package"
keywords:
  - K6:
      name: 'OpenCart home'
      vus: 1
      iterations: 1
      scriptFile: "opencart-test.js"
plans:
  - name: "Opencart load test plan"
    root:
      testScenario:
        children:
          - threadGroup:
              users: 5
              iterations: 10
              children:
                - callKeyword:
                    keyword: "OpenCart home"
```

### Agent provisioning (Kubernetes)

Auto-detect agents:
```yaml
plans:
  - name: "My Plan"
    agents: auto_detect
```

Manual specification:
```yaml
plans:
  - name: "My Plan"
    agents:
      - pool: java-enterprise-agent
        replicas: 2
        image: docker-dev.exense.ch/test:agent-java-custom
```

### Plain text plans

Include existing plain text plan files:
```yaml
plansPlainText:
  - file: "plans/this-is-a-plain-text-plan.plan"
    name: "this is a plain text plan"
    rootType: TestCase
    categories:
      - myTestCategory
```

### Converting between formats

- **Visual to YAML**: generate YAML from the visual plan editor in the Step UI (auto-excludes default values)
- **YAML to visual**: paste YAML source when creating a plan in the UI

---

## Parameters

Define environment-specific values with optional activation scripts (Groovy):

```yaml
parameters:
  - key: "baseURL"
    value: "http://test.com"
    activationScript: "env == 'TEST'"
  - key: "baseURL"
    value: "http://prod.com"
    activationScript: "env == 'PROD'"
  - key: "fullURL"
    value:
      expression: baseURL + "/something"
```

---

## Schedules

Define periodic executions with cron expressions:

```yaml
schedules:
  - name: "Opencart synthetic monitoring schedule"
    cron: "0 0/1 * * * ?"
    planName: "Opencart synthetic monitoring plan"
```

---

## Notification presets and alerting rules

### Notification presets

```yaml
notificationPresets:
  - EmailNotification:
      presetName: "Sample mail"
      upstreamPreset: "Mail"
      subject:
        data: "${eventSummary}"
        protection: READONLY
  - WebhookNotification:
      presetName: "Sample Webhook call"
      upstreamPreset: "Webhook"
      url:
        data: "https://example.org"
      method:
        data: "POST"
      body:
        data: '{"Hello": "World"}'
      headers:
        data:
          "X-Step-URL": "${controllerUrl}"
```

### Alerting rules

```yaml
alertingRules:
  - description: "Send email for incident"
    name: "Monitoring email alert"
    eventClass: IncidentOpenedEvent
    conditions:
      - BindingCondition:
          bindingKey: "executionParameters"
          predicate:
            BindingExistsPredicate: {}
      - BindingCondition:
          bindingKey: "executionParameters[env]"
          predicate:
            BindingValueEqualsPredicate:
              value: "PROD"
    actions:
      - NotificationAction:
          notification:
            EmailNotification:
              upstreamPreset: "Sample Mail"
              from:
                data: "me@example.org"
              to:
                data:
                  - "you@example.org"
```

Note: `BindingExistsPredicate: {}` requires explicit empty braces — omitting them produces invalid YAML.

---

## Fragment files

Fragment files enable modular automation packages. Each fragment declares entities using the same syntax and is included via the `fragments` field:

```yaml
version: 1.0.0
name: "My Automation Package"
fragments:
  - "fragment1.yml"
  - "fragment2.yml"
  - "fragments/*.yaml"    # wildcard — fragments must be in a subdirectory
```

Each fragment contains only the entity declarations (no top-level `name` or `version`):

```yaml
# plan1.yml
plans:
  - name: "Plan 1"
    root:
      testCase:
        children:
          - echo:
              text: "Hello world 1"
```

Limitation: fragments at the root of the automation package cannot be referenced by wildcards.

---

## Java-specific declarations

In addition to the YAML descriptor, Java packages support declaring entities directly in code.

### Keywords in Java

Any class extending `AbstractKeyword` with `@Keyword`-annotated methods is automatically included — no YAML entry needed.

### Plans via annotation

For single-keyword plans, annotate the keyword method with `@Plan`:

```java
@Plan()
@Keyword
public void myPlanMadeOfOneKeyword() {
    output.add("hello", "world");
}
```

### Plan categories

```java
@Plan()
@PlanCategories({"PerformanceTest", "Playwright"})
@Keyword
public void myPlanMadeOfOneKeyword() {
    output.add("hello", "world");
}
```

### Inline plans (deprecated)

Plain text plans defined via annotation. Declaring plans in YAML is now the recommended approach.

---

## Package sources

Automation Packages can be provided from three sources:

1. **Direct file upload** — via Step UI or CLI. Simplest approach for local builds.
2. **Maven artifact coordinates** — reference artifacts in any Maven-compatible repository (Artifactory, Nexus, GitHub Packages, CodeArtifact). Step creates one resource per unique coordinate per tenant. SNAPSHOT artifacts are not auto-refreshed — use explicit refresh.
3. **Existing Step resource** (libraries only) — reuse a library already deployed to Step.

---

## Automation Package Libraries

AP Libraries are reusable, versioned code artifacts that provide shared logic across multiple Automation Packages — common utilities, shared keywords, shared plans. They are deployed and referenced independently from individual packages.

Libraries can be provided as files, Maven coordinates, or managed libraries (referenced by name on the Step server).

---

## IDE setup

Download the JSON schema from your Step instance:
```
https://<your-step-instance>/rest/automation-packages/schema
```

**IntelliJ IDEA**: Settings > Languages & Frameworks > JSON Schema Mappings. Add the schema and associate it with your `automation-package.yaml` files for auto-completion and validation.

**Visual Studio**: similar JSON schema association in settings.
