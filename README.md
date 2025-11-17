# Try Coagent - AI Model and Agent Evals, Tests, and Logs

Quick start guide to try the Coagent AI Agent Framework using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- At least 4GB of available RAM
- Internet connection to download images

## Quick Start

1. **Clone or download this directory**
   ```bash
   git clone <repository-url>
   cd try-coagent
   ```

2. **Start the demo**
   ```bash
   docker-compose up -d
   ```

> [!NOTE]
> If you already have a CoAgent Demo running, stop it first.
> Run `docker-compose pull` and then run `docker-compose up`.

> [!TIP]
> If you want to cleanup storage you can run the following command,
> be mindful when running it as CoAgent storage will be deleted.
> `docker-compose down -v --remove-orphans`.

3. **Access the application**

   Once the containers are running, open your browser to:
   - **Main UI**: http://localhost:3000

## Shutting Down

Once you are done using CoAgent, you can stop services with:

```bash
docker-compose down
```

Data will remain stored, so you can restart later with `docker-compose up`.

## What's Included

The demo starts two main services:

- **coagent-core** (port 3000): Main API server with embedded web UI

Your data is stored locally in the `./coagent_demo_storage` directory.

## Optional Services

The docker-compose.yml includes optional services that are commented out:

### Ollama (Local LLM)
Uncomment the `ollama` service to run local language models. This will:
- Download and run Ollama
- Pull `all-minilm` and `qwen3:4b` models
- Require significant disk space and memory

## Common Commands

```bash
# Start the demo
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the demo
docker-compose down

# Update to latest version
docker-compose pull
docker-compose up

# Use specific version
IMAGE_TAG='v0.7.3' docker-compose up
```

## Learning Resources

### Interactive Tutorial
- **[Logging API Tutorial](examples/logging-api-tutorial.hurl)** - Hands-on, executable tutorial teaching the complete Logging API through real examples. Run with [Hurl](https://hurl.dev/) to learn interactively.

### Integration Examples
- **[LangChain](https://github.com/coa-dev/try-coagent/tree/main/examples/langchain-simple)** - Integrate CoAgent with LangChain agents
- **[Smolagents](https://github.com/coa-dev/try-coagent/tree/main/examples/smolagents)** - Integrate CoAgent with HuggingFace Smolagents
- **[ADK](https://github.com/coa-dev/try-coagent/tree/main/examples/adk)** - Build agents with CoAgent's native framework

## Troubleshooting

### Services won't start
- Ensure port 3000 is not in use by other applications
- Check Docker has sufficient resources allocated

### Can't access the UI
- Wait 30-60 seconds after `docker-compose up` for services to fully start
- Check logs with `docker-compose logs coagent-core`

### Need to reset data
```bash
docker-compose down
rm -rf coagent_demo_storage
docker-compose up
```

## Documentation

### Getting Started
- **[Logging API Tutorial](examples/logging-api-tutorial.hurl)** - Interactive HTTP API tutorial - best way to learn the logging API regardless of which language/client you'll use
- **[Event Logging Reference](docs/reference.md)** - Complete API reference for logging agent events, monitoring performance, and tracking behavior

### Client Libraries
- **Python Client** - Use the `coagent` Python package for easy integration (see examples above)
- **Direct HTTP API** - Call the REST API directly from any language (see the Hurl tutorial for examples)

## Support

For issues or questions:
- Contact us via the `Feedback` link in the ui
- Visit the main repository for documentation
- File issues in the project's issue tracker
