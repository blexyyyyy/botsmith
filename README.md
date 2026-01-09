# BotSmith

**A Governed Multi-Agent System for Building Bots from Natural Language**

BotSmith is a modular, production-oriented multi-agent framework that converts natural language requests into planned, validated, governed, and executable workflows. It is designed to demonstrate how autonomous agents can be built safely, with strong separation of concerns, deterministic execution, and full observability.

> This is not a prompt toy or a chat wrapper. BotSmith focuses on control, correctness, and extensibility.

## Key Capabilities

### Natural Language Interface
Parses user intent from plain English with confidence and ambiguity handling.

### Planner–Compiler–Executor Architecture
Translates intent to plan to workflow to execution deterministically.

### Hybrid Agent System
- **Logic-first agents** for planning, validation, routing, execution
- **LLM-assisted agents** where language reasoning is useful
- **Model-agnostic design** via LLM abstraction

### Governance Built In
- Validation gates
- Cost estimation
- Security scanning
- Workflow optimization

### End-to-End Tested
Full integration tests covering the complete lifecycle.

### 3-Layer Memory System (State + Preferences + Persistence)
- **Execution Context**: Ephemeral, step-level state for tools and reasoning.
- **Session Memory**: Short-term, workflow-scoped coordination across agents.
- **Long-Term Memory**: Persistent, policy-gated storage for user preferences and project knowledge.

## High-Level Architecture

```mermaid
graph TD
    A[Natural Language Input] --> B[NLP Interpreter]
    B --> C[Router Agent]
    C --> D[Planner Agent]
    D --> E[Validator Agent]
    E --> F[Workflow Compiler]
    F --> G[Optimizer / Cost / Security]
    G --> H[Workflow Executor]
    H --> I[Memory Manager]
    I --> J[(SQLite Persistence)]
```

Each stage is explicit, testable, and replaceable.

## Core Design Principles

- **SOLID and Clean Architecture**
- **Dependency Inversion** (interfaces over implementations)
- **Deterministic execution**
- **No blind trust in LLMs**
- **Governed autonomy over raw autonomy**

## Agent Types

### Core Logic Agents
- **RouterAgent**: selects the appropriate workflow
- **PlannerAgent**: generates a structured execution plan
- **ValidatorAgent**: validates plans and invariants
- **WorkflowCompilerAgent**: compiles plans into executable workflows
- **WorkflowExecutor**: executes workflows step by step
- **CostEstimatorAgent**: estimates and gates execution cost
- **SecurityAgent**: blocks unsafe operations
- **WorkflowOptimizerAgent**: reorders and deduplicates steps

### NLP Agent
- **NLPInterpreterAgent**: LLM-assisted semantic parsing, Schema validation, Confidence and ambiguity handling

### LLM Support
- **Gated Memory**: Multi-layer scoped storage with policy-enforced writes.
- **Local inference** via Ollama
- **Cloud-ready design** (Groq, Gemini, OpenAI supported via abstraction)

## Example End-to-End Flow

**User**: "Build a Python weather bot"

1.  NLP extracts intent
2.  Router selects `bot_creation_workflow`
3.  Planner generates steps
4.  Validator enforces correctness
5.  Compiler builds workflow
6.  Cost and security checks pass
7.  Executor runs steps
8.  Execution persisted to database

## Running Tests

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run integration tests

```bash
pytest tests/integration
```

### Run full end-to-end test

```bash
pytest tests/integration/test_end_to_end_creation.py
```

## Current Status

- **3-Layer Memory System**: Execution, Session, and Long-Term Persistent memory implemented.
- **Hybrid Multi-Agent Core**: Fully implemented and end-to-end tested.
- **Workflow Governance**: Cost estimation, security scanning, and optimization gates active.
- **API & UI**: FastAPI implementation and React/Vite visualization (`botsmith-ui`) in progress.
- **Workflow Persistence**: SQLite-backed audit trails and session history functional.

## Planned

- **Dynamic Agent Synthesis**: Auto-generation of specialized agents based on task complexity.
- **Human-in-the-Loop**: Interactive control gates for high-risk operations.
- **Adaptive Execution**: Real-time workflow adjustment based on tool feedback.
- **Advanced visualization**: Enhanced pipeline and agent state monitoring.

## Project Structure

```text
botsmith/
├── core/               # Interfaces, base classes, utilities
├── agents/             # Specialized agents
├── workflows/          # Workflow compiler and executor
├── nlp/                # NLP parsing and intent normalization
├── persistence/        # SQLite persistence layer
├── factory/            # Agent and workflow factories
├── tests/              # Unit, integration, end-to-end tests
├── botsmith-ui/        # React + Vite + Tailwind CSS Frontend
└── main.py
```

## Why This Project Exists

Most AI agent projects focus on prompting. BotSmith focuses on systems design.

The goal is to demonstrate how autonomous systems can be structured, governed, tested, and safely extended.

This repository is intended as a portfolio-grade systems project, not a product demo.

## License

MIT
