In Smolagents, `step_callbacks` are functions that can be defined to execute
specific actions or logging at each step of an agent's process. This feature
allows developers to monitor the agent's progress and manage its behavior
during execution.

## Getting Started

1. Run CoAgent as per the [main README](../../README.md)

2. Set your API Keys in a new `.env` file, copy it from the `.env.example` and fill it with your values.

3. Run the Smolagents example script:

Using Justfile:

```bash
just run
```

Or using Docker directly:

```bash
docker build --tag 'coa-smolagents' .
docker run --network host 'coa-smolagents'
```

4. Access the Space at: http://localhost:7860

## Development

### Setup

- Copy the `.env.example` into `.env` and pass a Read Only Access HuggingFace Token

> Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## Datasets

- Flights Dataset borrowed from https://www.kaggle.com/datasets/viveksharmar/flight-price-data

> Some data is synthesized for demonstration purposes.
