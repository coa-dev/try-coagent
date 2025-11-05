# CoAgent + ADK Example

This example demonstrates how to create and run a simple ADK Agent using CoAgent as the monitoring backend.

## Requisites

1. Install `google-adk`

```bash
pip install google-adk
```

2. Run CoAgent as per the [main README](../../README.md)

3.a. Run Agent in Terminal Interface

```bash
adk run src
```

3.b. Run Agent in Web UI

```bash
adk web --port 8000
```

## Approach

To monitor ADK, the CoAgentADKPlugin is provided taking advantage of ADK's plugin system
which allows us to intercept Agent Lifecycle events and send them to CoAgent.

Read more here: https://google.github.io/adk-docs/plugins/
