# Botsmith

Botsmith is a framework for orchestrating autonomous AI agents to build, deploy, and manage software projects. It leverages Large Language Models (LLMs) to plan, compile, and execute complex workflows.

## Features

- **Agent Orchestration**: Specialized agents for routing, planning, coding, and validation.
- **Workflow Compilation**: Dynamically compiles abstract requirements into executable steps.
- **LLM Integration**: Supports multiple providers including Ollama, Groq, and Google Gemini.
- **Persistence**: SQLite-based state management for workflows and agents.
- **Automated Testing**: Comprehensive test suite ensuring end-to-end reliability.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/blexyyyyy/botsmith.git
   cd botsmith
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory with your API keys (see `.env.example` if available, or source code for required keys).

## Usage

To run the end-to-end bot creation workflow (for testing purposes):

```bash
python tests/integration/test_end_to_end_creation.py
```

## Testing

Run the full test suite using pytest:

```bash
pytest
```

## Project Structure

- `agents/`: Implementation of specialized agents (Router, Planner, Executor, etc.).
- `core/`: Core interfaces and utilities (LLM wrappers, memory management).
- `factory/`: Agent factory and dependency injection.
- `generated/`: Output directory for generated code.
- `persistence/`: Database models and repositories.
- `tests/`: Unit and integration tests.
- `workflows/`: Workflow definitions.
