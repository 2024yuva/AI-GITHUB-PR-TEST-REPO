# PR Guardian Review Output Schema

The review contract is implemented with Pydantic in `src/review/schemas.py`.
No finding is included unless it has a valid file and line location plus evidence.

## JSON example

```json
{
  "status": "reviewed",
  "summary": "The PR can fail on an empty result set.",
  "complexity": "medium",
  "findings": [
    {
      "title": "Missing empty-result guard",
      "category": "bug",
      "severity": "high",
      "file": "src/orders.py",
      "line_start": 42,
      "line_end": 44,
      "explanation": "The function indexes the first result without handling an empty list.",
      "evidence": "orders[0] is executed after find_orders() returns an empty list.",
      "confidence": 0.91,
      "source": "llm"
    }
  ],
  "metadata": {
    "mode": "improved",
    "provider": "anthropic",
    "model": "claude-sonnet",
    "latency_ms": 1240,
    "input_tokens": 3500,
    "output_tokens": 420,
    "estimated_cost_usd": 0.018
  }
}
```

## Field rules

| Field | Required | Rules |
|---|---:|---|
| `status` | Yes | `reviewed`, `no_findings`, or `failed` |
| `summary` | Yes | Non-empty, concise summary |
| `complexity` | Yes | `low`, `medium`, or `high` |
| `findings` | Yes | Zero or more validated findings |
| `title` | Yes | Non-empty finding title |
| `category` | Yes | `bug`, `security`, `logic`, `edge_case`, `reliability`, or `quality` |
| `severity` | Yes | `low`, `medium`, `high`, or `critical` |
| `file` | Yes | Repository-relative POSIX path |
| `line_start` | Yes | Integer greater than zero |
| `line_end` | Yes | Greater than or equal to `line_start` |
| `evidence` | Yes | Non-empty, source-backed text |
| `confidence` | Yes | Float from 0.0 through 1.0 |
| `source` | Yes | `llm`, `static`, or `hybrid` |
| `metadata` | Yes | Provider, model, mode, latency, usage, and cost |

Invalid findings must be removed before delivery or cause a named validation
failure when a review contract is required.
