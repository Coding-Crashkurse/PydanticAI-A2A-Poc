# Pydantic-AI A2A Showcase

#### TL;DR

This project demonstrates a minimal **Pydantic-AI A2A (Assistant-to-Assistant)** setup:

* **`server.py`**: Runs an A2A-compatible agent using `pydantic-ai` and `FastA2A`.
* **`fasta2a_client.py`**: Sends a valid A2A request, polls the task status, and prints the agent's response.
* **`wrong_client.py`**: Uses the old Google `a2sa` client — fails because the schema is incompatible.
* **`mcp_server.py`**: Shows a mock server integration (MCP-style).

**Purpose:** Demonstrate a working stack and highlight current issues (schema mismatches, model access, etc.).
