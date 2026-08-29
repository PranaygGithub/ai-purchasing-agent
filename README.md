# Procura AI — Python Purchasing Agent

Full-stack implementation of Scenario 1 and Scenario 2 from the AI Purchasing Agent assignment.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- Vanilla HTML/CSS/JavaScript
- Mock operational data
- Deterministic purchasing decision engine
- Validation loop
- Pytest tests

## Assignment coverage

### Scenario 1
The agent reviews a recommended purchase and considers:
- current inventory
- expected demand
- open purchase orders
- supplier lead time
- supplier minimum order
- purchasing budget
- storage capacity

Possible decisions:
- ACCEPT
- MODIFY
- REJECT
- INVESTIGATE

### Scenario 2
The agent handles a supplier shortfall:
- original PO
- supplier-confirmed quantity
- inventory
- expected demand
- alternative supplier
- alternative supplier quantity and price
- budget

Possible decisions:
- ACCEPT
- ACCEPT PARTIAL + WAIT
- SOURCE REMAINDER
- INVESTIGATE
- ESCALATE

## Architecture

```text
Browser
  |
  | JSON / HTTP
  v
FastAPI
  |
  +--> Scenario 1 Agent
  |
  +--> Scenario 2 Agent
  |
  v
Validation Engine
  |
  v
Decision + Reasons + Action + Validation
```

## Project structure

```text
ai-purchasing-agent-python/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── data.py
│   ├── agent.py
│   └── validation.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── requirements.txt
├── .env.example
├── README.md
├── architecture.md
└── run.bat
```

## Windows setup — beginner friendly

### 1. Install Python

Install Python 3.11 or newer.

During installation, tick:

```text
Add Python to PATH
```

Check:

```cmd
python --version
```

### 2. Open CMD in this project folder

For example:

```cmd
cd /d D:\ai-purchasing-agent-python
```

### 3. Create a virtual environment

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your command prompt.

### 4. Install packages

```cmd
pip install -r requirements.txt
```

### 5. Start the application

```cmd
uvicorn backend.main:app --reload
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

### 6. Open the UI

Go to:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Quick run

You can also double-click:

```text
run.bat
```

## API examples

### Scenario 1

POST:

```text
/api/scenario1/analyze
```

```json
{
  "product": "Premium Coffee Beans",
  "recommended_quantity": 800,
  "current_inventory": 300,
  "expected_demand": 850,
  "open_purchase_orders": 200,
  "supplier_lead_time_days": 5,
  "supplier_minimum_order": 100,
  "available_budget": 25000,
  "unit_price": 20,
  "storage_capacity": 1500
}
```

### Scenario 2

POST:

```text
/api/scenario2/analyze
```

```json
{
  "product": "Organic Milk",
  "original_purchase_order": 500,
  "supplier_confirmed_quantity": 250,
  "current_inventory": 80,
  "expected_demand": 400,
  "alternative_supplier_available": true,
  "alternative_supplier_quantity": 250,
  "alternative_supplier_unit_price": 24,
  "current_supplier_unit_price": 20,
  "available_budget": 10000
}
```

## Run tests

```cmd
pytest -q
```

## Why no LLM?

The assignment does not require a specific LLM and explicitly permits mock APIs/data. This implementation uses deterministic business rules for hard purchasing constraints. An LLM can later be added for tool selection, explanation, and natural-language interaction, while the constraint checks remain deterministic.

## Validation loop

```text
1. Investigate
2. Calculate inventory position / shortfall
3. Check constraints
4. Make decision
5. Propose action
6. Validate action
7. Return decision + validation
```

This directly demonstrates the assignment's emphasis on validating the result of an agent action.
