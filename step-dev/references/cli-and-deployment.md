# Step CLI, Maven Plugin, and Deployment

> Live docs:
>
> - Step CLI: https://step.dev/knowledgebase/devops/automation-package-cli/step-cli/
> - Local execution: https://step.dev/knowledgebase/devops/automation-package-cli/step-cli/local-execution/
> - Step Studio: https://step.dev/knowledgebase/devops/step-studio/
> - Maven plugin: https://step.dev/knowledgebase/devops/automation-package-cli/ap-maven-plugin/
> - Automation as Code (CI/CD context): https://step.dev/knowledgebase/devops/automation-as-code/
> - Automation Package in Java (JUnit): https://step.dev/knowledgebase/devops/automation-package-java/

## Table of contents

1. [Step CLI overview](#step-cli-overview)
2. [Getting the CLI](#getting-the-cli)
3. [CLI usage and help](#cli-usage-and-help)
4. [Automation Package location](#automation-package-location)
5. [Local execution](#local-execution)
6. [Remote execution](#remote-execution)
7. [Deploying packages](#deploying-packages)
8. [Deploying libraries](#deploying-libraries)
9. [Multi-version deployment](#multi-version-deployment)
10. [Filtering plans](#filtering-plans)
11. [Execution reports](#execution-reports)
12. [CLI configuration files](#cli-configuration-files)
13. [Maven plugin](#maven-plugin)
14. [Local execution with JUnit](#local-execution-with-junit)
15. [CI/CD integration](#cicd-integration)

---

## Step CLI overview

The Step CLI handles all Automation Package operations:

- Execute packages locally or remotely on a Step server
- Deploy packages to a Step server (full installation with schedule activation)
- Deploy libraries independently
- Open packages in Step Studio, a local visual editor (`step studio`, beta since Step 31)
- Works with folders, ZIPs, JARs, an `automation-package.yaml` path, and Maven artifact coordinates

---

## Getting the CLI

- **Step Open Source**: download `step` / `step.exe` from the [step-distribution releases](https://github.com/exense/step-distribution/releases). The `exense/step` releases carry no CLI binaries.
- **Step Enterprise**: download from the Enterprise download section
- **Docker** (Step 31+): `docker.exense.ch/step/cli:<version>` (open source, also for Step SaaS) or `docker.exense.ch/step-enterprise/cli:<version>`; the tag is the Step version, e.g. `3.31.0`

Requirements:

- Use the same CLI version as your Step server
- Java JRE 21+ (since Step 30; it was 11+ before)

---

## CLI usage and help

```bash
step                        # top-level help: ap, library, studio
step ap --help              # automation package operations
step ap execute --help      # detailed help for execute
step ap deploy --help       # detailed help for deploy
step studio --help          # Step Studio
```

---

## Automation Package location

`-p` takes a folder, a ZIP or JAR, the path to an `automation-package.yaml`, or `mvn:` coordinates. Without the `-p` option, it treats the current directory as the package root.

```bash
# Explicit path
step ap execute --local -p /path/to/automation-package/

# Current directory (must contain automation-package.yaml)
step ap execute --local
```

### Excluding files with .apignore

Add a `.apignore` file to the package root to exclude files during packaging. Same syntax as `.gitignore`.

```text
/ignored-folder
/ignoredFile.yml
```

Only supported for folder-based packages deployed or executed via the Step CLI (not Maven JAR packaging).

---

## Local execution

Execute all plans locally without a Step server:

```bash
step ap execute --local
step ap execute --local -p /path/to/package/
```

Since Step 31, local execution starts real agents for every keyword type, so it is the package-level check before a deploy, not only a Java one:

| Keyword type | Needs locally |
| --- | --- |
| Composite, Java, Groovy, JavaScript | nothing extra |
| Node.js | `node` on `PATH` (npm for the project's dependencies) |
| C#/.NET (Enterprise) | the Step .NET agent, via `--localAgentDotNet` or `STEP_DOTNET_AGENT_HOME` |
| JMeter, SoapUI, k6, Cypress, … | the tool's runtime, via its env var (`JMETER_HOME`, `SOAP_UI_HOME`, …) |

**Not supported locally:** Silk Performer and QFTest (not yet), and PDF Compare, whose keyword is provided by the Step server. Package libraries work locally: `--library=./my-library.jar`.

Local-only options: `--localAgentJava`, `--localAgentNode`, `--localAgentDotNet`, `--localAgentWorkDir`, `--localAgentMaxTokens` (default 5), `--localAgentStartTimeout` (default 60 s), and `--localAgentVmArgs` (repeatable; pass a JDWP string to attach a debugger to the Java agent). `--verbose` and `--debug` raise the log level.

**`--reportType` does not apply to local runs** — reports are generated for remote executions only, and passing it with `--local` is an error.

---

## Remote execution

Execute packages on a Step server in isolation (one-off, temporary context):

```bash
step ap execute \
  --stepUrl=http://localhost:8080 \
  --token=<API_KEY> \
  --projectName=JMeter_Tests
```

Remote executions are ephemeral — the package exists only during execution and is not permanently deployed.

### Execute from artifact repository

```bash
step ap execute \
  --stepUrl=http://localhost:8080 \
  -p "mvn:groupId:artefactId:version[:classifier:type]"
```

Classifier and type are optional. For type without classifier: `mvn:groupId:artefactId:version::type`

### Execute with libraries

```bash
# Library as file
step ap execute -p ./package.jar -l ./library.jar

# Library from Maven
step ap execute -p ./package.jar -l mvn:ch.exense.step.testing.libraries:java-keyword-library:1.0.0

# Managed library (deployed on Step server)
step ap execute -p ./package.jar -l managed:MyCommonJavaLib -c cli.properties
```

### Wrap plans into a TestSet

By default, each plan runs as a separate execution. Use `--wrapIntoTestSet` to run all plans in a single TestSet:

```bash
step ap execute --stepUrl=http://localhost:8080 --wrapIntoTestSet
# Optionally control parallelism:
step ap execute --stepUrl=http://localhost:8080 --wrapIntoTestSet --numberOfThreads=4
```

---

## Deploying packages

Deploy makes all entities available on the Step server and activates schedules and alerting rules:

```bash
step ap deploy \
  --stepUrl=http://localhost:8080 \
  --token=<API_KEY> \
  --projectName=Common
```

### Deploy from artifact repository

```bash
step ap deploy \
  --stepUrl=http://localhost:8080 \
  -p "mvn:groupId:artefactId:version"
```

### Deployment options

| Option | Effect |
| --- | --- |
| `--async` | return without waiting for the deployment to finish |
| `--deployment-timeout` | how long to wait for it (default 300 s) |
| `--tokenSelectionCriteria="k=v\|k=v"` | agent token routing for the package's keywords |
| `--executeKeywordsOnController` | run the keywords on the controller instead of agents |
| `--plansAttributes`, `--keywordsAttributes` | pipe-delimited attributes added to every plan / keyword (package values win over keyword-level ones) |

`step ap execute` also takes `--executionTimeoutS` (default 3600). Confirm names with `step ap deploy --help`; the Maven plugin has camel-case equivalents (`async`, `deploymentTimeout`, …).

### Deploy with libraries

Same syntax as execute:

```bash
step ap deploy -p ./package.jar -l ./library.jar
step ap deploy -p ./package.jar -l mvn:group:artifact:version
step ap deploy -p ./package.jar -l managed:MyCommonJavaLib
```

### Force refresh of SNAPSHOT artifacts

When other packages in the same tenant use the same SNAPSHOT coordinate:

```bash
step ap deploy -p ./package-SNAPSHOT.jar -l mvn:group:artifact:version-SNAPSHOT --forceRefreshOfSnapshots
```

---

## Deploying libraries

Deploy libraries independently (useful for shared libraries across multiple packages and projects):

```bash
# Deploy a library
step library deploy -l mvn:ch.exense.step.testing.libraries:java-keyword-library:1.0.0

# Deploy as managed library (referenceable by name)
step library deploy -l mvn:ch.exense.step.testing.libraries:java-keyword-library:1.0.0 --managed="MyCommonJavaLib"
```

---

## Multi-version deployment

Deploy multiple versions of the same package for different environments:

```bash
step ap deploy --versionName="PROD" --activationExpression="env == \"PROD\""
step ap deploy --versionName="TEST" --activationExpression="env == \"TEST\""
```

The activation expression (Groovy) determines which version is selected at runtime.

---

## Filtering plans

Select which plans to execute:

### By name

```bash
step ap execute --includePlans=PlanA,PlanB
step ap execute --excludePlans=SkipThisPlan
```

### By category

```bash
step ap execute --includeCategories=FunctionalTest,Playwright
step ap execute --excludeCategories=PerformanceTest
```

These options can be combined.

---

## Execution reports

Remote executions only; see [Local execution](#local-execution).

```bash
# JUnit XML report (written to file by default)
step ap execute --reportType=junit

# Aggregated report (printed to stdout by default)
step ap execute --reportType=aggregated

# Custom output destination
step ap execute --reportType="junit;output=file,stdout"

# Custom report directory
step ap execute --reportType=junit --reportDir=./reports
```

---

## CLI configuration files

All CLI options can be defined in configuration files.

### Resolution order (last wins)

1. `~/stepcli.properties` (home folder — auto-loaded if present)
2. Configuration files passed with `-c` (left to right)
3. Command-line arguments

### Example

`~/stepcli.properties`:

```properties
stepUrl=https://my-step-server.example.com
token=<API_KEY>
projectName=Common
```

`jmeter_cli.properties` (project-specific):

```properties
projectName=JMeter_Tests
```

```bash
step ap execute -c jmeter_cli.properties
# Uses stepUrl and token from home config, projectName from jmeter_cli.properties
```

### Execution parameters

Use the `|` delimiter for multiple parameters in config files:

```properties
executionParameters=myParam1=myValue1|myParam2=myValue2
```

On the command line, use `-ep` for each parameter:

```bash
step ap execute -ep myParam1=myValue1 -ep myParam2=myValue2
```

Parameters from all sources are merged. When a key is defined multiple times, the same resolution order applies (last wins).

---

## Maven plugin

For Java projects, the Maven plugin provides the same operations as the CLI.

**Since Step 30.5 the plugin is not on Maven Central.** Versions 3.30.5 and later live in Exense's open source repository; without it Maven fails with "plugin not found". Earlier versions remain on Central. Enterprise uses `https://nexus-enterprise.exense.ch/repository/exense/`.

```xml
<pluginRepositories>
    <pluginRepository>
        <id>exense-oss</id>
        <url>https://repository.exense.ch/maven-oss/</url>
    </pluginRepository>
</pluginRepositories>
```

### Execute remotely

```bash
mvn package step:execute-automation-package \
  "-Dstep.url=https://your.step.server/" \
  "-Dstep.step-project-name=Common" \
  "-Dstep.auth-token=your_token"
```

### Deploy

```bash
mvn package step:deploy-automation-package \
  "-Dstep.url=https://your.step.server/" \
  "-Dstep.step-project-name=Common" \
  "-Dstep.auth-token=your_token"
```

See the [Maven plugin documentation](https://step.dev/knowledgebase/devops/automation-package-cli/ap-maven-plugin/) for full plugin configuration and goals.

---

## Local execution with JUnit

For Java packages, use JUnit to execute packages locally without a Step server.

### JUnit 4

```java
import org.junit.runner.RunWith;
import step.junit.runner.Step;

@RunWith(Step.class)
public class RunAutomationPackageTest {}
```

### JUnit 5

```java
import step.junit5.runner.StepJUnit5;

public class RunAutomationPackageTest extends StepJUnit5 {}
```

### Running

```bash
mvn test -Dtest="RunAutomationPackageTest"
```

The Step runner executes all plans in the Automation Package.

### Filtering plans in JUnit

```java
@RunWith(Step.class)
@IncludePlanCategories({"Playwright", "JMeter", "FunctionalTest"})
@ExcludePlanCategories({"PerformanceTest"})
@ExcludePlans({"My Plan name to be excluded"})
public class RunAutomationPackageTest {}
```

### Execution parameters for local execution

Three approaches:

**1. Annotation:**

```java
@RunWith(Step.class)
@ExecutionParameters({"MyParam1", "Value of param 1", "MyParam2", "Value of param 2"})
public class RunAutomationPackageTest {}
```

**2. Environment variables:** any `STEP_*` variable maps to the parameter name without the prefix (e.g., `STEP_MyParam` becomes `MyParam`)

**3. System properties:** same mapping as environment variables (`-DSTEP_MyParam=value`)

### Required dependencies

The JUnit artifacts moved off Maven Central with the plugin (Step 30.5+): declare the same `exense-oss` URL under `<repositories>`. The Keyword API (`step-api-keyword`) is still on Central.

```xml
<!-- Step OS, JUnit 4 -->
<dependency>
    <groupId>ch.exense.step</groupId>
    <artifactId>step-automation-packages-junit</artifactId>
    <version>${step.version}</version>
    <scope>provided</scope> <!-- use test scope for local-only -->
</dependency>

<!-- Step OS, JUnit 5 -->
<dependency>
    <groupId>ch.exense.step</groupId>
    <artifactId>step-automation-packages-junit5</artifactId>
    <version>${step.version}</version>
    <scope>provided</scope>
</dependency>

<!-- Step Enterprise equivalents use groupId: ch.exense.step-enterprise -->
<!-- and artifactId: step-automation-packages-junit-ee / step-automation-packages-junit5-ee -->
```

---

## CI/CD integration

The typical CI/CD integration pattern:

1. **Store automation code** alongside application code in the same repository
2. **Build the package** in the CI/CD pipeline together with the application
3. **Publish** to an artifact repository (optional, for multi-server deployments)
4. **Execute or deploy** at different pipeline stages:
   - **Test phase**: execute plans after deploying the app to test environment (load tests, E2E tests, smoke tests)
   - **Operate phase**: deploy for self-service RPA tasks and recurring automation
   - **Monitor phase**: deploy for synthetic monitoring with scheduled plan execution

The Step CLI and Maven plugin integrate naturally with any CI/CD tool (Jenkins, GitLab CI, GitHub Actions, etc.) since they are standard command-line operations.
