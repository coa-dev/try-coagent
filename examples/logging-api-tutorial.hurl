################################################################################
# CoAgent Logging API Tutorial
################################################################################
#
# This file demonstrates how to use the CoAgent Logging API to track AI agent
# execution, monitor performance, and analyze behavior. It serves as both
# documentation and a working test suite.
#
# WHAT IS THIS?
# -------------
# This is a Hurl file - an executable test/tutorial that sends HTTP requests
# and validates responses. You can run it to learn the API interactively.
#
# PREREQUISITES:
# --------------
# 1. CoAgent server running at http://localhost:3000
#    Start with: docker-compose up
#
# 2. Hurl installed: https://hurl.dev/docs/installation.html
#    macOS: brew install hurl
#    Linux: See https://hurl.dev
#
# HOW TO RUN:
# -----------
# Run this tutorial:
#   hurl --test examples/logging-api-tutorial.hurl
#
# Run with verbose output to see all requests/responses:
#   hurl --test --verbose examples/logging-api-tutorial.hurl
#
# WHAT YOU'LL LEARN:
# ------------------
# 1. How to log different event types (session start/end, LLM calls, tools, errors)
# 2. How to structure log entries correctly
# 3. How to retrieve and filter logs for analysis
# 4. How to track performance metrics and custom metadata
# 5. Best practices for agent logging
#
################################################################################

################################################################################
# PART 1: SESSION LIFECYCLE - Start to Finish
################################################################################
#
# Every agent run is organized as a "session" identified by a unique session_id.
# A typical session follows this pattern:
#   1. SessionStart - Initialize the session
#   2. User interactions, LLM calls, tool usage (multiple events)
#   3. SessionEnd - Close the session
#
# Let's create a complete session...

# ------------------------------------------------------------------------------
# Test 1: POST SessionStart - Begin an Agent Session
# ------------------------------------------------------------------------------
#
# SessionStart marks the beginning of an agent execution run. Use this to:
# - Record when the agent started
# - Capture the initial prompt/goal
# - Track the agent software stack (frameworks, versions, etc.)
#
# KEY FIELDS:
# - session_id: Unique identifier for this run (you choose this)
# - event_type: "session_start"
# - prompt: The initial user request or goal
# - agent_stack: Array of strings describing your agent software
# - timestamp: Unix timestamp in milliseconds
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 1,
  "turn_number": 0,
  "event_id": "evt-start-001",
  "event_type": "session_start",
  "timestamp": 1725379200000,
  "meta": {
    "tutorial": "logging-api-basics",
    "environment": "development"
  },
  "prompt": "Research the latest developments in quantum computing and summarize key breakthroughs",
  "agent_stack": [
    "langchain::0.3.0",
    "openai::1.0.0",
    "python::3.11"
  ]
}

# EXPECTED RESPONSE: 200 OK with success message
HTTP 200
[Asserts]
jsonpath "$.success" == true
jsonpath "$.message" == "Log entry stored successfully"


################################################################################
# PART 2: LLM INTERACTIONS - Calls and Responses
################################################################################
#
# Track all interactions with language models to:
# - Debug prompt engineering
# - Monitor token usage and costs
# - Analyze model performance
# - Review conversation history

# ------------------------------------------------------------------------------
# Test 2: POST LlmCall - Log an LLM Request
# ------------------------------------------------------------------------------
#
# Record every time you call a language model. This helps you:
# - See what prompts were sent
# - Track conversation history
# - Monitor which agent/component made the call
#
# KEY FIELDS:
# - event_type: "llm_call"
# - prompt: The main prompt/question being asked
# - llm_call.issuer: Which agent/component made this call
# - llm_call.history: Previous conversation turns
# - llm_call.system_prompt: The system/instruction prompt
# - meta: Store model parameters (model name, temperature, max_tokens)
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 2,
  "turn_number": 1,
  "event_id": "evt-llm-call-001",
  "event_type": "llm_call",
  "timestamp": 1725379260000,
  "meta": {
    "model": "gpt-4-turbo",
    "temperature": 0.7,
    "max_tokens": 2000,
    "provider": "openai"
  },
  "prompt": "What are the most significant quantum computing breakthroughs in 2024?",
  "llm_call": {
    "issuer": "research_agent",
    "history": [
      {"role": "user", "content": "I need information about quantum computing"},
      {"role": "assistant", "content": "I'll help you research quantum computing developments."}
    ],
    "system_prompt": "You are a helpful research assistant specializing in emerging technologies."
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true

# ------------------------------------------------------------------------------
# Test 3: POST LlmResponse - Log the LLM's Answer
# ------------------------------------------------------------------------------
#
# Immediately after an LLM call, log the response to:
# - Capture the model's output
# - Track token usage (critical for cost monitoring)
# - Record any tool calls the model requested
#
# KEY FIELDS:
# - event_type: "llm_response"
# - llm_response.response: The actual text response from the model
# - llm_response.input_tokens: Tokens in the prompt
# - llm_response.output_tokens: Tokens in the response
# - llm_response.total_tokens: Sum (used for cost calculation)
# - llm_response.tool_calls: Any tools the model wants to use (optional)
#
# NOTE: Match prompt_number and turn_number with the corresponding LlmCall
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 2,
  "turn_number": 1,
  "event_id": "evt-llm-response-001",
  "event_type": "llm_response",
  "timestamp": 1725379265000,
  "llm_response": {
    "response": "In 2024, major breakthroughs include Google's achievement of quantum error correction, IBM's 1000+ qubit processor, and practical applications in drug discovery.",
    "input_tokens": 125,
    "output_tokens": 45,
    "total_tokens": 170,
    "tool_calls": null
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 3: TOOL USAGE - External Actions
################################################################################
#
# When your agent uses external tools (APIs, databases, functions), log both
# the tool call and its response. This helps you:
# - Debug tool integration issues
# - Monitor external API performance
# - Track errors and failures
# - Measure execution time

# ------------------------------------------------------------------------------
# Test 4: POST ToolCall - Log Tool Invocation
# ------------------------------------------------------------------------------
#
# Record when your agent calls an external tool/function.
#
# KEY FIELDS:
# - event_type: "tool_call"
# - tool_call.tool_name: Name of the tool being called
# - tool_call.parameters: Arguments passed to the tool
#
# COMMON TOOLS: web_search, calculator, database_query, api_request, etc.
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 3,
  "turn_number": 2,
  "event_id": "evt-tool-call-001",
  "event_type": "tool_call",
  "timestamp": 1725379320000,
  "tool_call": {
    "tool_name": "web_search",
    "parameters": {
      "query": "quantum computing breakthroughs 2024",
      "num_results": 10,
      "source": "arxiv"
    }
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true

# ------------------------------------------------------------------------------
# Test 5: POST ToolResponse - Log Tool Results
# ------------------------------------------------------------------------------
#
# After the tool executes, log its response. This is CRITICAL for debugging.
#
# KEY FIELDS:
# - event_type: "tool_response"
# - tool_response.tool_name: Same as the ToolCall
# - tool_response.parameters: Echo the parameters used
# - tool_response.result: The actual data/output from the tool
# - tool_response.success: Did it work? (boolean)
# - tool_response.error_message: If failed, what went wrong?
# - tool_response.execution_time_ms: Performance monitoring
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 3,
  "turn_number": 2,
  "event_id": "evt-tool-response-001",
  "event_type": "tool_response",
  "timestamp": 1725379325000,
  "tool_response": {
    "tool_name": "web_search",
    "parameters": {
      "query": "quantum computing breakthroughs 2024",
      "num_results": 10,
      "source": "arxiv"
    },
    "result": {
      "papers_found": 10,
      "top_result": {
        "title": "Fault-Tolerant Quantum Computing at Scale",
        "url": "https://arxiv.org/example",
        "relevance_score": 0.95
      }
    },
    "success": true,
    "error_message": null,
    "execution_time_ms": 1250
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 4: ERROR HANDLING - When Things Go Wrong
################################################################################
#
# Logging errors is essential for debugging and improving your agent.
# Track failures, their severity, and recovery attempts.

# ------------------------------------------------------------------------------
# Test 6: POST Error - Log Agent Errors
# ------------------------------------------------------------------------------
#
# When something goes wrong, create a detailed error log entry.
#
# KEY FIELDS:
# - event_type: "error"
# - error_info.error_id: Unique identifier for tracking
# - error_info.error_type: Category of error (api_timeout, validation_error, etc.)
# - error_info.error_message: Human-readable description
# - error_info.error_severity: low/medium/high/critical
# - error_info.component_id: Which part of your system failed
# - error_info.recovery_strategy: What you tried to do about it
# - error_info.recovery_successful: Did recovery work?
# - error_info.human_intervention_required: Does a human need to fix this?
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 4,
  "turn_number": 3,
  "event_id": "evt-error-001",
  "event_type": "error",
  "timestamp": 1725379380000,
  "error_info": {
    "error_id": "ERR-2024-001",
    "error_type": "api_rate_limit",
    "error_message": "OpenAI API rate limit exceeded (429 Too Many Requests)",
    "error_severity": "medium",
    "component_id": "llm_client",
    "recovery_strategy": "exponential_backoff_retry",
    "recovery_actions": ["wait_60s", "retry_request"],
    "recovery_successful": true,
    "human_intervention_required": false,
    "impact_assessment": "Delayed response by 60 seconds, user notified"
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 5: PERFORMANCE TRACKING - Metrics and Monitoring
################################################################################

# ------------------------------------------------------------------------------
# Test 7: POST with Performance Metrics
# ------------------------------------------------------------------------------
#
# Track performance metrics alongside your events for monitoring and optimization.
#
# PERFORMANCE METRICS AVAILABLE:
# - success_rate: Percentage of successful operations (0.0 to 1.0)
# - confidence_score: Agent's confidence in its output (0.0 to 1.0)
# - accuracy_score: Measured accuracy (0.0 to 1.0)
# - cost: Dollar cost of this operation
# - tokens_used: Total tokens consumed
# - memory_usage_mb: Memory footprint
# - cpu_usage_percent: CPU utilization
# - network_bytes: Network data transferred
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 5,
  "turn_number": 4,
  "event_id": "evt-llm-call-002",
  "event_type": "llm_call",
  "timestamp": 1725379440000,
  "prompt": "Synthesize the research findings into a summary",
  "llm_call": {
    "issuer": "synthesis_agent",
    "history": null,
    "system_prompt": "You synthesize research into clear summaries."
  },
  "performance_metrics": {
    "success_rate": 0.98,
    "confidence_score": 0.85,
    "accuracy_score": 0.92,
    "cost": 0.0045,
    "tokens_used": 850,
    "memory_usage_mb": 245.5,
    "cpu_usage_percent": 12.3,
    "network_bytes": 8192
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 6: CUSTOM METADATA - Extend with Your Own Data
################################################################################

# ------------------------------------------------------------------------------
# Test 8: POST with Custom Metadata
# ------------------------------------------------------------------------------
#
# You can add ANY custom fields to log entries using:
# - custom_metadata: For application-specific tracking data
# - additional_properties: For flexible, dynamic properties
# - meta: For general contextual information
#
# USE CASES:
# - Track user IDs and session context
# - Add feature flags and experiment identifiers
# - Include business metrics
# - Store debugging information
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 6,
  "turn_number": 5,
  "event_id": "evt-user-input-001",
  "event_type": "user_input",
  "timestamp": 1725379500000,
  "input_data": {
    "user_query": "Can you explain quantum entanglement?",
    "input_method": "voice",
    "language": "en-US"
  },
  "custom_metadata": {
    "user_id": "user-12345",
    "subscription_tier": "premium",
    "experiment_group": "new_prompt_template_v2",
    "session_context": "research_mode"
  },
  "additional_properties": {
    "client_version": "2.5.1",
    "platform": "web",
    "device_type": "desktop",
    "feature_flags": ["streaming_enabled", "advanced_reasoning", "multimodal"]
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 7: SESSION COMPLETION
################################################################################

# ------------------------------------------------------------------------------
# Test 9: POST SessionEnd - Close the Session
# ------------------------------------------------------------------------------
#
# Mark the end of your agent run with SessionEnd.
#
# KEY FIELDS:
# - event_type: "session_end"
# - meta.status: completed/failed/cancelled
# - meta.total_turns: How many interaction turns occurred
# - meta.duration_ms: Total session duration
# - additional_properties: Any final summary data
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
{
  "version": "2.0.0",
  "session_id": "tutorial-session-001",
  "prompt_number": 7,
  "turn_number": 6,
  "event_id": "evt-end-001",
  "event_type": "session_end",
  "timestamp": 1725379600000,
  "meta": {
    "status": "completed",
    "total_turns": 6,
    "duration_ms": 400000,
    "success": true
  },
  "additional_properties": {
    "elapsed_time_ms": 400000,
    "final_status": "success",
    "total_cost_usd": 0.0123,
    "total_tokens": 1500,
    "user_satisfied": true
  }
}

HTTP 200
[Asserts]
jsonpath "$.success" == true


################################################################################
# PART 8: BATCH LOGGING - Multiple Entries at Once
################################################################################

# ------------------------------------------------------------------------------
# Test 10: POST Array of Log Entries (Batch Mode)
# ------------------------------------------------------------------------------
#
# You can log multiple entries in a single API call by sending an array.
# This is useful for:
# - Reducing network overhead
# - Atomic logging of related events
# - Offline agents that buffer logs
#
# NOTE: Send a JSON array instead of a single object
#
POST http://localhost:3000/api/v1/logs
Content-Type: application/json
[
  {
    "version": "2.0.0",
    "session_id": "batch-tutorial-session",
    "prompt_number": 1,
    "turn_number": 0,
    "event_id": "batch-start",
    "event_type": "session_start",
    "timestamp": 1725379700000,
    "prompt": "Quick batch test",
    "agent_stack": ["batch-agent::1.0"]
  },
  {
    "version": "2.0.0",
    "session_id": "batch-tutorial-session",
    "prompt_number": 2,
    "turn_number": 1,
    "event_id": "batch-end",
    "event_type": "session_end",
    "timestamp": 1725379760000,
    "additional_properties": {
      "elapsed_time_ms": 60000
    }
  }
]

HTTP 200
[Asserts]
jsonpath "$.success" == true
jsonpath "$.message" == "All log entries stored successfully"


################################################################################
# PART 9: RETRIEVING LOGS - Read Your Data Back
################################################################################

# ------------------------------------------------------------------------------
# Test 11: GET Logs for a Specific Session
# ------------------------------------------------------------------------------
#
# Retrieve all log entries for a session_id.
# Returns an array of all events in chronological order.
#
# ENDPOINT: GET /api/v1/logs/{session_id}
#
GET http://localhost:3000/api/v1/logs/tutorial-session-001

HTTP 200
[Asserts]
jsonpath "$" isCollection
# We logged 8 events in tutorial-session-001
jsonpath "$[*]" count >= 8

# Verify first entry is session_start
jsonpath "$[0].event_type" == "session_start"
jsonpath "$[0].session_id" == "tutorial-session-001"
jsonpath "$[0].prompt" exists

# Verify last entry is session_end
jsonpath "$[-1].event_type" == "session_end"

# Verify LLM interaction data is present
jsonpath "$[?(@.event_type == 'llm_call')].llm_call.issuer" exists
jsonpath "$[?(@.event_type == 'llm_response')].llm_response.total_tokens" exists

# Verify performance metrics were stored
jsonpath "$[?(@.performance_metrics)].performance_metrics.success_rate" exists

# Verify custom metadata was preserved
jsonpath "$[?(@.custom_metadata)].custom_metadata.user_id" exists


# ------------------------------------------------------------------------------
# Test 12: GET All Session IDs
# ------------------------------------------------------------------------------
#
# List all session_ids in the system.
# Useful for dashboards and session management.
#
# ENDPOINT: GET /api/v1/runs
#
GET http://localhost:3000/api/v1/runs

HTTP 200
[Asserts]
jsonpath "$" isCollection
# Our tutorial sessions should be in the list
jsonpath "$[*]" contains "tutorial-session-001"
jsonpath "$[*]" contains "batch-tutorial-session"


# ------------------------------------------------------------------------------
# Test 13: GET Session Summaries (with statistics)
# ------------------------------------------------------------------------------
#
# Get high-level statistics for all sessions.
# Add ?summarize=1 to get log counts and timestamps.
#
# ENDPOINT: GET /api/v1/runs?summarize=1
#
# RESPONSE FIELDS:
# - run_id: The session identifier
# - log_count: Number of log entries
# - start_timestamp: When the session started (ms)
# - end_timestamp: When the session ended (ms)
#
GET http://localhost:3000/api/v1/runs?summarize=1

HTTP 200
[Asserts]
jsonpath "$" isCollection

# Verify our tutorial session has a summary
jsonpath "$[?(@.run_id == 'tutorial-session-001')].run_id" exists
jsonpath "$[?(@.run_id == 'tutorial-session-001')].log_count" exists
jsonpath "$[?(@.run_id == 'tutorial-session-001')].start_timestamp" exists
jsonpath "$[?(@.run_id == 'tutorial-session-001')].end_timestamp" exists

# Verify log count is reasonable (should be 8+)
# Note: The filter returns an array, so we check the first element
jsonpath "$[?(@.run_id == 'tutorial-session-001')].log_count" nth 0 >= 8


################################################################################
# CONGRATULATIONS! 🎉
################################################################################
#
# You've completed the CoAgent Logging API tutorial!
#
# WHAT YOU LEARNED:
# -----------------
# ✓ How to structure log entries for different event types
# ✓ How to track complete agent sessions from start to finish
# ✓ How to log LLM calls, tool usage, and errors
# ✓ How to add performance metrics and custom metadata
# ✓ How to retrieve and filter logs for analysis
# ✓ How to handle batch logging
# ✓ API validation and error handling
#
# NEXT STEPS:
# -----------
# 1. Integrate logging into your AI agent using the Python client library
# 2. Explore the CoAgent UI at http://localhost:3000 to visualize your logs
# 3. Read the Event Logging Reference: docs/reference.md
# 4. Check out integration examples: examples/langchain-simple, examples/smolagents
#
# QUESTIONS OR ISSUES?
# --------------------
# - Visit the CoAgent UI and use the "Feedback" link
# - Check the documentation for detailed API reference
# - Review example integrations in the examples/ directory
#
# Happy logging! 🚀
#
################################################################################
