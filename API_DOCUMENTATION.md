# UHIP API Documentation

## Overview

The UHIP API provides RESTful endpoints for accessing and managing the Unified Hybrid Intelligence Platform services. All endpoints use JSON for request and response bodies.

## Base URL

```
Production: https://api.uhip-platform.com/v1
Staging: https://staging-api.uhip-platform.com/v1
Local Development: http://localhost:8000/v1
```

## Authentication

### Bearer Token
All API requests must include an Authorization header with a Bearer token:

```bash
Authorization: Bearer {access_token}
```

### Token Generation
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Token Refresh
```bash
POST /auth/refresh
Authorization: Bearer {refresh_token}
```

## API Endpoints

### 1. Health & Status

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-03T10:00:00Z",
  "version": "1.0.0"
}
```

### 2. Predictions

#### POST /predictions/ml
Create a new machine learning prediction.

**Request:**
```json
{
  "model_id": "xgboost-v1",
  "features": {
    "temperature": 25.5,
    "humidity": 60,
    "pressure": 1013.25
  }
}
```

**Response:**
```json
{
  "prediction_id": "pred_123456",
  "model_id": "xgboost-v1",
  "prediction": 0.87,
  "confidence": 0.92,
  "created_at": "2026-01-03T10:00:00Z"
}
```

#### GET /predictions/{prediction_id}
Retrieve a specific prediction.

**Response:**
```json
{
  "prediction_id": "pred_123456",
  "model_id": "xgboost-v1",
  "prediction": 0.87,
  "confidence": 0.92,
  "features": { ... },
  "created_at": "2026-01-03T10:00:00Z"
}
```

### 3. Quantum Computing

#### POST /quantum/simulate
Run a quantum circuit simulation.

**Request:**
```json
{
  "circuit": "OPENQASM 2.0; ...",
  "shots": 1000,
  "simulator": "qasm_simulator"
}
```

**Response:**
```json
{
  "job_id": "qjob_789012",
  "status": "completed",
  "results": {
    "000": 245,
    "001": 255,
    "010": 250,
    "011": 250
  },
  "execution_time": 1.23
}
```

### 4. Blockchain

#### POST /blockchain/transaction
Submit a blockchain transaction.

**Request:**
```json
{
  "from": "0x123...",
  "to": "0x456...",
  "amount": "1000000000000000000",
  "contract": "transfer"
}
```

**Response:**
```json
{
  "transaction_id": "0xabc123def456",
  "status": "pending",
  "gas_price": "20",
  "gas_limit": "21000"
}
```

#### GET /blockchain/transaction/{tx_id}
Get transaction status.

**Response:**
```json
{
  "transaction_id": "0xabc123def456",
  "status": "confirmed",
  "block_number": 12345678,
  "confirmation_count": 100
}
```

### 5. Edge Computing

#### GET /edge/nodes
List all edge computing nodes.

**Response:**
```json
{
  "nodes": [
    {
      "node_id": "edge_001",
      "location": "us-west-1",
      "cpu_usage": 45.2,
      "memory_usage": 62.1,
      "status": "online"
    }
  ]
}
```

#### POST /edge/tasks
Submit a task to edge nodes.

**Request:**
```json
{
  "task_type": "inference",
  "model": "lightweight-model-v1",
  "target_node": "edge_001",
  "parameters": { ... }
}
```

### 6. Data Management

#### POST /data/upload
Upload dataset for processing.

**Request:**
```
Multipart form data
- file: (binary data)
- dataset_name: "sales_data_2026"
- format: "csv"
```

**Response:**
```json
{
  "dataset_id": "ds_654321",
  "name": "sales_data_2026",
  "records": 10000,
  "status": "processing"
}
```

#### GET /data/{dataset_id}
Retrieve dataset information.

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "email",
        "issue": "Email format is invalid"
      }
    ]
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|------------|-------------|
| UNAUTHORIZED | 401 | Missing or invalid authentication |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 400 | Invalid request parameters |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

## Rate Limiting

API requests are rate-limited:
- **Default**: 1000 requests per hour per API key
- **Enterprise**: 10000 requests per hour per API key

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

## Pagination

List endpoints support pagination:

```bash
GET /predictions?page=1&page_size=20&sort=-created_at
```

**Response:**
```json
{
  "items": [ ... ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 500,
    "total_pages": 25
  }
}
```

## WebSocket Support

For real-time updates, connect to the WebSocket endpoint:

```
ws://localhost:8000/ws/live
```

Authentication:
```json
{
  "type": "auth",
  "token": "{access_token}"
}
```

## SDK Examples

### Python
```python
from uhip_sdk import UHIPClient

client = UHIPClient(api_key="your_api_key")

# Make prediction
result = client.predictions.create(
    model_id="xgboost-v1",
    features={"temperature": 25.5}
)
print(result.prediction)
```

### JavaScript
```javascript
import { UHIPClient } from 'uhip-sdk-js';

const client = new UHIPClient({ apiKey: 'your_api_key' });

const result = await client.predictions.create({
  modelId: 'xgboost-v1',
  features: { temperature: 25.5 }
});
console.log(result.prediction);
```

## Webhooks

Register webhooks for real-time notifications:

```bash
POST /webhooks
{
  "url": "https://yourdomain.com/webhook",
  "events": ["prediction.completed", "task.failed"]
}
```

## Support
For API support and issues, refer to DEVELOPER_README.md or contact support@uhip-platform.com
