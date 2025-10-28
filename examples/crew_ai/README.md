## Getting Started

1. Fill up the `.env` file with your OpenAI API key.

```
MODEL=gpt-5-nano
OPENAI_API_KEY=
```

2. Install dependencies

```bash
crewai install
```

3. Run the CrewAI app

```bash
crewai run
```

You should be able to see an output similar to this:

<div align="center">
    <img src="https://raw.githubusercontent.com/coa-dev/try-coagent/refs/heads/examples/crewai/examples/crew_ai/docs/screen1.png" alt="CrewAI Output Example" width="600"/>
</div>

### Pre-Requisites

- Python `>= v3.12`
- UV `>= v0.5`
- CrewAI `>= v0.108`

#### Install Python

```bash
# Using pyenv
pyenv install 3.12.0
pyenv virtualenv 3.12.0 crew-ai-env
pyenv activate crew-ai-env
```

#### Install UV

```bash
pip install uv
```

#### Install CrewAI

```bash
uv tool install crewai
```

### Setup

This project was generated using:

```bash
crewai create crew crew-ai
```

More details in: https://docs.crewai.com/en/installation
