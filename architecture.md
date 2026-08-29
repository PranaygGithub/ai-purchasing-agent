# Procura AI Architecture

```mermaid
flowchart TD
    A[Modern Web Dashboard] --> B[FastAPI REST API]

    B --> C[Scenario 1 Purchasing Agent]
    B --> D[Scenario 2 Supplier Shortfall Agent]

    C --> E[Inventory + Demand + Open PO + Supplier + Budget + Storage]
    D --> F[Inventory + Supplier Confirmation + Alternative Supplier + Budget]

    C --> G[Validation Engine]
    D --> G

    G --> H[Decision]
    H --> I[Action]
    I --> J[Validation Result]
    J --> A
```

## Agent decision pipeline

```text
INPUT
  ↓
INVESTIGATE DATA
  ↓
CALCULATE POSITION
  ↓
CHECK HARD CONSTRAINTS
  ↓
DECIDE
  ↓
PROPOSE ACTION
  ↓
VALIDATE
  ↓
RETURN RESULT
```

## Production evolution

The assignment is a one-day exercise, so the project intentionally uses mock data and a simple deterministic engine.

A production version could replace:
- mock data → PostgreSQL / ERP / inventory APIs
- simple rules → rules + optimization + LLM tool-calling
- direct actions → approval workflow
- console/test validation → audit logs and monitoring
