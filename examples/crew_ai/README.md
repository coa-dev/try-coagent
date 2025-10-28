## Getting Started

1. Fill up the `.env` file with your OpenAI API key.

```
MODEL=<model-name>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
OPENAI_API_KEY=<your-openai-api-key>
```

2. Install dependencies

```bash
crewai install
```

3. Run the CrewAI app

```bash
crewai run
```

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
