# CoAgent + ADK Example

This example demonstrates how to create and run a simple ADK Agent using CoAgent as the monitoring backend.

## Getting Started

1. Run CoAgent as per the [main README](../../README.md)

2. Set your API Keys in a new `.env` file, copy it from the `.env.example` and fill it with your values.

3. Run the ADK example script:

Using Justfile:

```bash
just run
```

Or using Docker directly:

```bash
docker build --tag 'coa-adk' .
docker run --network host -it 'coa-adk'
```

This will start the ADK runner as written in `examples/adk/agent/__main__.py`, an interactive
shell will be opened where you can send prompts to the agent.

## Approach

To monitor ADK, the CoAgentADKPlugin is provided taking advantage of ADK's plugin system
which allows us to intercept Agent Lifecycle events and send them to CoAgent.

Read more here: https://google.github.io/adk-docs/plugins/

The ADK crew is run using programatic approach, that means that instead of using the default runner:

```bash
adk run agent
```

We are running a Python script that creates the agent and runs it:

```bash
uv run python3 -m agent
```

Logic for the `CoagentPlugin` is available in `examples/adk/agent/coa_plugin.py`.
