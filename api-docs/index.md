# AI Cloud Dashboard API Documentation

Welcome to the API documentation for the AI Cloud Dashboard. This guide provides comprehensive information about the available APIs, their endpoints, and usage examples.

## API Overview

The AI Cloud Dashboard provides RESTful APIs for accessing various features and data points of the dashboard programmatically.

## Authentication

All API requests require authentication using an API key. Include your API key in the request header:

```bash
Authorization: Bearer your_api_key_here
```

## Base URL

```
https://api.aicloud-dashboard.com/v1
```

## API Endpoints

### Market Intelligence

#### Get Market Share Data
```http
GET /market/share
```

Parameters:
- `region` (optional): Filter by geographic region
- `provider` (optional): Filter by cloud provider
- `timeframe` (optional): Time period for data (default: 30 days)

Response:
```json
{
  "data": {
    "providers": [
      {
        "name": "AWS",
        "share": 32.5,
        "growth": 2.1
      },
      {
        "name": "Azure",
        "share": 28.7,
        "growth": 3.4
      }
    ],
    "timestamp": "2025-01-29T19:00:00Z"
  }
}
```

### Performance Metrics

#### Get Performance Data
```http
GET /metrics/performance
```

Parameters:
- `metric` (required): Specific metric to retrieve
- `service` (optional): Filter by service
- `region` (optional): Filter by region

Response:
```json
{
  "data": {
    "metric": "latency",
    "values": [
      {
        "timestamp": "2025-01-29T19:00:00Z",
        "value": 45.2,
        "unit": "ms"
      }
    ]
  }
}
```

### Cost Analysis

#### Get Cost Estimates
```http
GET /costs/estimate
```

Parameters:
- `services` (required): Array of services to include
- `region` (optional): Target region
- `term` (optional): Commitment term

Response:
```json
{
  "data": {
    "total": 1250.00,
    "currency": "USD",
    "breakdown": [
      {
        "service": "compute",
        "cost": 850.00
      },
      {
        "service": "storage",
        "cost": 400.00
      }
    ]
  }
}
```

### Security & Compliance

#### Get Compliance Status
```http
GET /compliance/status
```

Parameters:
- `framework` (optional): Specific compliance framework
- `region` (optional): Filter by region

Response:
```json
{
  "data": {
    "status": "compliant",
    "lastCheck": "2025-01-29T19:00:00Z",
    "findings": [
      {
        "category": "encryption",
        "status": "passed"
      }
    ]
  }
}
```

## Error Handling

The API uses standard HTTP response codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

Error Response Format:
```json
{
  "error": {
    "code": "invalid_request",
    "message": "Detailed error message",
    "details": {}
  }
}
```

## Rate Limiting

- 1000 requests per hour per API key
- Rate limit headers included in responses:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## SDKs and Libraries

Official SDKs are available for:

- Python: `pip install aicloud-dashboard`
- JavaScript: `npm install aicloud-dashboard`
- Java: Available through Maven
- Go: `go get github.com/aicloud-dashboard/sdk-go`

## Webhooks

The API supports webhooks for real-time notifications:

```http
POST /webhooks/configure
```

```json
{
  "url": "https://your-server.com/webhook",
  "events": ["metric.alert", "compliance.change"],
  "secret": "your_webhook_secret"
}
```

## Additional Resources

- [Getting Started Guide](getting-started.md)
- [API Reference](reference.md)
- [Code Examples](examples.md)
- [SDK Documentation](sdk/index.md)
- [Changelog](changelog.md)

## Support

For API support:

1. Check the [API Troubleshooting Guide](troubleshooting.md)
2. Review [Common Issues](common-issues.md)
3. Contact support at api-support@aicloud-dashboard.com

## Terms of Use

By using the API, you agree to our [Terms of Service](terms.md) and [API Usage Policy](usage-policy.md).
