# CoAgent Examples

This directory contains examples and tutorials for integrating CoAgent into your AI applications.

## Quick Start Tutorial

### 📚 Logging API Tutorial (HTTP API)

**[logging-api-tutorial.hurl](./logging-api-tutorial.hurl)** - An interactive, executable tutorial that teaches you the complete CoAgent Logging API through hands-on HTTP examples.

**Who is this for?**
- Anyone learning the CoAgent Logging API (recommended starting point)
- Developers using the **Python client** (learn the concepts first, then use the client)
- Developers using the **direct HTTP API** from any language (JavaScript, Rust, Go, etc.)
- Those who want to understand the API internals

**What you'll learn:**
- How to log AI agent sessions from start to finish
- Tracking LLM calls and responses with token usage
- Logging tool/function calls and their results
- Error handling and recovery tracking
- Performance metrics and custom metadata
- Retrieving and filtering logs for analysis

**Note:** While this tutorial shows raw HTTP requests, the same concepts apply when using the Python client library. The Python client wraps these HTTP calls for convenience.

**Prerequisites:**
1. CoAgent server running (see main [README.md](../README.md))
2. [Hurl](https://hurl.dev/) installed:
   ```bash
   # macOS
   brew install hurl

   # Linux (Ubuntu/Debian)
   curl -LO https://github.com/Orange-OpenSource/hurl/releases/latest/download/hurl_x.x.x_amd64.deb
   sudo dpkg -i hurl_x.x.x_amd64.deb

   # Other platforms: https://hurl.dev/docs/installation.html
   ```

**How to run:**
```bash
# Navigate to the try-coagent directory
cd try-coagent

# Start the CoAgent server
docker-compose up -d

# Run the tutorial
hurl --test examples/logging-api-tutorial.hurl

# Run with verbose output to see all requests/responses
hurl --test --verbose examples/logging-api-tutorial.hurl
```

**What is Hurl?**

Hurl is a command-line tool that runs HTTP requests defined in a simple plain text format. The tutorial file is both documentation and executable tests - you can read it to learn the API, and run it to see everything in action.

## Integration Examples

### Python Integrations

#### LangChain
**[examples/langchain-simple](./langchain-simple/)** - Integrate CoAgent logging with LangChain agents

Learn how to:
- Add CoAgent logging to existing LangChain applications
- Track agent chains and tool usage
- Monitor performance and costs

#### Smolagents
**[examples/smolagents](./smolagents/)** - Integrate CoAgent logging with HuggingFace Smolagents

Learn how to:
- Log Smolagents execution
- Track model calls and tool usage
- Analyze agent behavior

#### Agent Development Kit (ADK)
**[examples/adk](./adk/)** - Build agents using CoAgent's native ADK framework

Learn how to:
- Build agents from scratch using the ADK
- Automatic logging integration
- Advanced agent patterns

## Documentation

- **[Event Logging Reference](../docs/reference.md)** - Complete API reference documentation
- **[Main README](../README.md)** - Getting started with CoAgent

## Support

Need help?
- Use the "Feedback" link in the CoAgent UI
- Check the [Event Logging Reference](../docs/reference.md)
- Review the tutorial file comments for detailed explanations

## Contributing

Have an example to share? Contributions are welcome! Please ensure your examples:
- Include clear documentation
- Work with the latest CoAgent release
- Follow the existing example structure
