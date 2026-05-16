# Keywords — Development and API

> Live docs:
> - Keyword Development: https://step.dev/knowledgebase/devdocs/keyword-development/
> - Keyword API: https://step.dev/knowledgebase/devdocs/keywordapi/
> - Tutorials: https://step.dev/tutorials/basic-keyword-development/
> - Java samples: https://github.com/exense/step-samples/tree/master/keywords/java
> - JS samples: https://github.com/exense/step-node/tree/master/examples
> - .NET samples: https://github.com/exense/step-samples/tree/master/keywords/dotnet80

## Table of contents

1. [What is a custom keyword](#what-is-a-custom-keyword)
2. [Keyword declaration by language](#keyword-declaration-by-language)
3. [Keyword inputs](#keyword-inputs)
4. [Keyword outputs](#keyword-outputs)
5. [Keyword lifecycle and hooks](#keyword-lifecycle-and-hooks)
6. [Stateless vs stateful keywords](#stateless-vs-stateful-keywords)
7. [Error handling](#error-handling)
8. [Measurements](#measurements)
9. [Keyword Proxy (plans as code)](#keyword-proxy-plans-as-code)
10. [Live reporting](#live-reporting)
11. [Best practices](#best-practices)

---

## What is a custom keyword

A custom keyword is a user-defined block of automation logic implemented in code. Unlike plugin-based keywords (Cypress, JMeter, K6, etc.), custom keywords let you integrate any tool, framework, or library into Step workflows.

The Keyword API provides the interface to:
- Define and configure keywords using annotations and class extensions
- Access keyword inputs, session objects, and report data
- Implement hooks for pre/post execution and error management

---

## Keyword declaration by language

### Java

Extend `AbstractKeyword` and annotate keyword methods with `@Keyword`:

```java
public class MyKeywords extends AbstractKeyword {
    @Keyword
    public void myKeyword() {
        // automation logic
    }
}
```

The `@Keyword` annotation supports these attributes:
- `name` — custom keyword name (defaults to method name)
- `schema` — JSON schema for inputs
- `description` — description shown in Step UI
- `properties` — additional configuration properties

### .NET

Extend `AbstractScript` and annotate with `[Keyword]`:

```csharp
namespace STEP {
    public class Keywords : StepApi.AbstractScript {
        [Keyword(name = "My Keyword")]
        public void MyKeyword() {
            // your implementation
        }
    }
}
```

### JavaScript / TypeScript (Node.js)

Export async functions from CommonJS `.js` files in the `keywords/` directory (configurable via `step.keywords` in `package.json`). The export name becomes the keyword name in Step.

```javascript
exports.MyKeyword = async (input, output, session, properties) => {
    const result = await doSomething(input['param'])
    output.add('result', result)
}
```

Each keyword receives four arguments:
- **input** — input parameters from the Step plan, as a plain object
- **output** — an `OutputBuilder` for return values, errors, and attachments
- **session** — a Map scoped to the token's lifetime for sharing state between keyword calls
- **properties** — flat key/value map of agent and token properties configured in Step

Three optional module-level hooks can be exported alongside keywords:
- `beforeKeyword(functionName)` — called before each keyword execution
- `afterKeyword(functionName)` — called after each keyword execution, even on failure
- `onError(exception, input, output, session, properties)` — called on error; return `true` to propagate, `false` to suppress

---

## Keyword inputs

Keyword inputs are passed as a JSON object with open types. The developer chooses argument types but must read them accordingly.

### Reading inputs in code

**Java** (via inherited `input` object):
```java
String homeUrl = input.getString("url");
int elementIndex = input.getInt("index", 1);
```

**Java** (via method arguments with `@Input` annotation — recommended):
```java
@Keyword
public void myKeyword(
    @Input(name = "myRequiredInput", required = true) int myRequiredInput,
    @Input(name = "myOptionalInput", defaultValue = "3") int myOptionalInput,
    @Input(name = "myString", defaultValue = "hello") String myString
) {
    // inputs are directly available as method parameters
}
```

Supported `@Input` types: `String`, `Integer`/`int`, `Long`/`long`, `Double`/`double`, `BigDecimal`, `BigInteger`, arrays/collections of supported types, Maps of strings to supported types, and POJOs with accessible fields.

**.NET**:
```csharp
string homeUrl = (string)input["url"];
```

**JavaScript**:
```javascript
var homeUrl = input['url'];
```

### Passing inputs from code (for testing)

**Java** (with `KeywordRunner`):
```java
ExecutionContext ctx = KeywordRunner.getExecutionContext(properties, this.getClass());
Output<JsonObject> output = ctx.run("MyKeyword", "{\"url\":\"http://www.example.com\", \"index\": 3}");
```

**JavaScript** (with `runner`):
```javascript
const runner = require('step-node-agent/api/runner/runner')({
    myProperty: 'value'  // equivalent to agent properties
})
try {
    const output = await runner.run('MyKeyword', { param: 'value' })
    console.log(output.payload)
} finally {
    runner.close()  // releases the session
}
```

---

## Keyword outputs

Use the inherited `output` object (an `OutputBuilder`) to define keyword results.

### Adding output data

```java
output.add("status", "success");
output.add("count", 42);
```

```javascript
output.add('status', 'success')
output.add('count', 42)
```

### Adding attachments

```java
output.addAttachment(AttachmentHelper.generateAttachmentForException(e));
```

```javascript
output.attach({
    name: 'screenshot.png',
    description: 'Page screenshot',
    hexContent: Buffer.from(imageData).toString('base64')
})
```

### Setting errors

```java
output.setBusinessError("Login failed: invalid credentials");
```

```javascript
// Simplest approach — sets message AND attaches stack trace
output.setError(e)

// With custom message
output.setError('Custom message', e)
```

---

## Keyword lifecycle and hooks

The execution flow of a keyword:

1. **Initialization** — keyword class is instantiated, inputs and properties are set, session context is attached
2. **beforeKeyword** (optional) — pre-execution setup (validate inputs, establish connections)
3. **Keyword function** — the annotated method executes
4. **onError** (optional) — triggered if an error occurs during execution
5. **afterKeyword** (optional) — always called after the keyword function, regardless of success or failure (cleanup)
6. **Instance release** — keyword instance is released, no data retained between executions

### Implementing hooks

**Java**:
```java
@Override
public void beforeKeyword(String keywordName, Keyword annotation) {
    System.out.println("Calling " + keywordName);
}

@Override
public void afterKeyword(String keywordName, Keyword annotation) {
    takeScreenshot();
}

@Override
public boolean onError(Exception e) {
    output.addAttachment(AttachmentHelper.generateAttachmentForException(e));
    return true;  // propagate the error
}
```

**JavaScript** (module-level exports):
```javascript
exports.beforeKeyword = async (functionName) => {
    console.log('Before:', functionName)
}

exports.afterKeyword = async (functionName) => {
    console.log('After:', functionName)
}

exports.onError = async (exception, input, output, session, properties) => {
    output.setError(exception)
    return true  // propagate
}
```

---

## Stateless vs stateful keywords

| Feature | Stateless | Stateful |
|---|---|---|
| Instance lifecycle | New instance per execution | Data shared via session |
| Data persistence | None between executions | Persists in session across workflow |
| Use case | Idempotent, isolated operations | Workflows needing shared state |

### When to use stateful keywords

Use the session when keywords within a workflow need to share state — for example, storing authentication tokens, browser instances, or database connections.

The session is only available when keyword calls are grouped using the `Session` control in a plan. Objects stored in the session must implement `Closeable` or `AutoCloseable` to be cleaned up when the session is released.

**Java**:
```java
// Store in session
session.put("browser", browser);

// Retrieve from session
WebDriver browser = (WebDriver) session.get("browser");
```

**JavaScript**:
```javascript
// Store in session
session.set('browser', browser)

// Retrieve from session
const browser = session.get('browser')
```

---

## Error handling

### Business errors vs technical errors

- **Business errors** — expected failures in the system under test (login failed, assertion failed). Use `output.setBusinessError()`. Sets keyword status to `FAILED`.
- **Technical errors** — unexpected exceptions (null pointer, connection timeout). Any uncaught exception is reported as a technical error. Catch and categorize them explicitly when possible.

**Java**:
```java
try {
    // automation logic
} catch (BusinessException e) {
    output.setBusinessError(e.getMessage());
    output.addAttachment(AttachmentHelper.generateAttachmentForException(e));
} catch (Exception e) {
    output.setError(e.getMessage());
    output.addAttachment(AttachmentHelper.generateAttachmentForException(e));
}
```

**JavaScript**:
```javascript
try {
    // automation logic
} catch (e) {
    output.setError(e)  // sets message + attaches stack trace
}
```

---

## Measurements

Measurements track execution timing for analytics. A default measurement is created automatically per keyword execution. Custom measurements provide finer granularity.

Measurements work in a stack — `stopMeasure()` closes the most recently opened one.

**Java**:
```java
output.startMeasure("NavigateToPage");
// do navigation
output.startMeasure("FillForm");
// fill the form
output.stopMeasure();  // stops FillForm

Map<String, String> data = new HashMap<>();
data.put("username", "Smith");
output.stopMeasure(data);  // stops NavigateToPage with analytics data
```

**JavaScript**:
```javascript
output.startMeasure('Navigate')
// do something
output.stopMeasure()

output.startMeasure('Submit')
// do something
output.stopMeasure({ status: 'FAILED' })

// Pre-timed measures
output.addMeasure('Pre-timed measure', 50)
output.addMeasure('Pre-timed measure 2', 150, {
    status: 'TECHNICAL_ERROR',
    begin: Date.now() - 150,
    data: { info: 'test' }
})
```

Starting with Keyword API version 1.5.0 (Step 29), you can assign an explicit status to individual measurements.

---

## Keyword Proxy (plans as code)

The Keyword Proxy lets a parent keyword invoke child keywords directly from code, creating workflows without using Step plans. Java only.

Key features:
- Automatically shares the parent keyword's context (session, properties)
- Manages output propagation (merge all outputs or set manually)
- Creates measurements for all individual keyword calls

```java
@Plan
@Keyword
public void WorkflowAsCode() {
    KeywordProxy keywordProxy = new KeywordProxy(this, true);  // true = merge outputs
    KeywordExample proxy = keywordProxy.getProxy(KeywordExample.class);

    String myInput = getInputOrProperty("myInputString");
    proxy.myFirstKeyword(3, false, myInput);

    Output<JsonObject> lastOutput = keywordProxy.getLastOutput();
    if (lastOutput.getPayload().getBoolean("shouldFail")) {
        output.appendError("The call to myFirstKeyword returned a failure");
        return;
    }

    proxy.mySecondKeyword();
    proxy.myThirdKeyword(List.of("value1", "value2"), Map.of("key1", "val1"));
}
```

---

## Live reporting

Live Reporting streams data (log files, measurements) in real time while the keyword runs, as opposed to returning them only after completion. Java API only. Both live and traditional reporting can be combined.

> Live Reporting is under active development and planned for finalization in Step 30. Fully supported on Step infrastructure; local execution support is limited.

See the Keyword API javadoc for streaming file upload and advanced features.

---

## Best practices

### General

- **Minimize dependencies** — keep keywords lightweight
- **Use meaningful names** — keyword names should clearly reflect their functionality

### Modularity

- Single-purpose keywords increase reusability across workflows but require more development effort
- Larger keywords wrapping entire workflows are faster to develop but lose modularity
- Choose based on how many different plans will reuse the keyword

### Resource management

Clean up all resources explicitly — browsers, WebDriver instances, database connections, file handles, downloaded files. Approaches:
1. Try/finally in the keyword function itself (simplest)
2. `afterKeyword` hook (always runs, even on failure)
3. Store resources in session with `Closeable`/`AutoCloseable` — cleaned up when session closes

### Session usage

- Use session properties sparingly to avoid memory overhead
- Objects stored in session must implement `Closeable` or `AutoCloseable` if they need cleanup
- Sessions are scoped to the `Session` control in a plan — not globally available

### Accessing Automation Package resources

Java keywords deployed via Automation Packages can retrieve and extract the archive at runtime:

```java
if (isInAutomationPackage()) {
    File extractedArchiveFolder = retrieveAndExtractAutomationPackage();
    // access bundled resources
}
```
