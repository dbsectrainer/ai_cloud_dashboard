# API Integration Guide

This guide explains how to integrate with the AI Cloud Dashboard's APIs and external cloud provider services.

## Authentication

### API Keys
```python
from src.utils.auth import APIKeyAuth

class CloudAPIClient:
    def __init__(self, api_key):
        self.auth = APIKeyAuth(api_key)
        self.base_url = "https://api.aicloud-dashboard.com/v1"

    async def make_request(self, endpoint, method="GET", data=None):
        """Make authenticated API request"""
        headers = self.auth.get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"{self.base_url}/{endpoint}",
                headers=headers,
                json=data
            ) as response:
                return await response.json()
```

### OAuth Integration
```python
from src.utils.auth import OAuthHandler

class OAuthClient:
    def __init__(self, client_id, client_secret):
        self.oauth = OAuthHandler(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="https://aicloud-dashboard.com/oauth/callback"
        )

    async def get_access_token(self, auth_code):
        """Exchange auth code for access token"""
        return await self.oauth.exchange_code(auth_code)
```

## Cloud Provider Integration

### AWS Integration
```python
import boto3
from src.utils.aws import AWSCredentials

class AWSIntegration:
    def __init__(self, credentials: AWSCredentials):
        self.session = boto3.Session(
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            region_name=credentials.region
        )

    def get_cloudwatch_metrics(self, namespace, metric_name):
        """Get CloudWatch metrics"""
        client = self.session.client('cloudwatch')
        return client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name
                        },
                        'Period': 300,
                        'Stat': 'Average'
                    }
                }
            ],
            StartTime=datetime.utcnow() - timedelta(hours=1),
            EndTime=datetime.utcnow()
        )
```

### Azure Integration
```python
from azure.mgmt.monitor import MonitorManagementClient
from src.utils.azure import AzureCredentials

class AzureIntegration:
    def __init__(self, credentials: AzureCredentials):
        self.client = MonitorManagementClient(
            credentials=credentials.get_credentials(),
            subscription_id=credentials.subscription_id
        )

    def get_metrics(self, resource_id, metric_names):
        """Get Azure metrics"""
        return self.client.metrics.list(
            resource_id,
            timespan=f"{datetime.utcnow() - timedelta(hours=1)}/{datetime.utcnow()}",
            interval='PT5M',
            metricnames=','.join(metric_names),
            aggregation='Average'
        )
```

### Google Cloud Integration
```python
from google.cloud import monitoring_v3
from src.utils.gcp import GCPCredentials

class GCPIntegration:
    def __init__(self, credentials: GCPCredentials):
        self.client = monitoring_v3.MetricServiceClient(
            credentials=credentials.get_credentials()
        )

    def get_metrics(self, project_id, metric_type):
        """Get Google Cloud metrics"""
        project_name = f"projects/{project_id}"
        interval = monitoring_v3.TimeInterval({
            'end_time': {'seconds': int(time.time())},
            'start_time': {'seconds': int(time.time() - 3600)}
        })
        
        return self.client.list_time_series(
            request={
                "name": project_name,
                "filter": f'metric.type = "{metric_type}"',
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            }
        )
```

## Market Data Integration

### Provider Market Share
```python
class MarketDataClient:
    def __init__(self, api_key):
        self.client = CloudAPIClient(api_key)

    async def get_market_share(self):
        """Get cloud provider market share data"""
        return await self.client.make_request("market/share")

    async def get_growth_trends(self, timeframe="1Y"):
        """Get market growth trends"""
        return await self.client.make_request(
            "market/trends",
            params={"timeframe": timeframe}
        )
```

### Competitive Analysis
```python
class CompetitiveAnalysis:
    def __init__(self, api_key):
        self.client = CloudAPIClient(api_key)

    async def get_competitor_analysis(self, competitors):
        """Get competitive analysis data"""
        return await self.client.make_request(
            "market/competition",
            method="POST",
            data={"competitors": competitors}
        )
```

## Performance Integration

### Metrics Collection
```python
class MetricsCollector:
    def __init__(self):
        self.integrations = {
            'aws': AWSIntegration(AWSCredentials()),
            'azure': AzureIntegration(AzureCredentials()),
            'gcp': GCPIntegration(GCPCredentials())
        }

    async def collect_all_metrics(self):
        """Collect metrics from all providers"""
        tasks = [
            self.collect_provider_metrics(provider)
            for provider in self.integrations.keys()
        ]
        return await asyncio.gather(*tasks)

    async def collect_provider_metrics(self, provider):
        """Collect metrics from specific provider"""
        integration = self.integrations[provider]
        return await integration.get_metrics()
```

### Performance Analysis
```python
class PerformanceAnalyzer:
    def analyze_metrics(self, metrics_data):
        """Analyze performance metrics"""
        return {
            'summary': self.calculate_summary(metrics_data),
            'trends': self.analyze_trends(metrics_data),
            'anomalies': self.detect_anomalies(metrics_data)
        }
```

## Error Handling

### Rate Limiting
```python
from src.utils.rate_limit import RateLimiter

class RateLimitedClient:
    def __init__(self, base_client, rpm=60):
        self.client = base_client
        self.rate_limiter = RateLimiter(rpm)

    async def make_request(self, *args, **kwargs):
        """Make rate-limited request"""
        async with self.rate_limiter:
            return await self.client.make_request(*args, **kwargs)
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RetryableClient:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    async def make_request(self, *args, **kwargs):
        """Make request with retry logic"""
        try:
            return await self.client.make_request(*args, **kwargs)
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
```

## Best Practices

### Security
1. Never hardcode credentials
2. Use environment variables for sensitive data
3. Implement proper key rotation
4. Use secure communication (HTTPS)
5. Implement request signing

### Performance
1. Use connection pooling
2. Implement caching where appropriate
3. Use batch operations when possible
4. Monitor API usage and limits
5. Optimize request frequency

### Error Handling
1. Implement proper retry logic
2. Handle rate limiting gracefully
3. Log all API interactions
4. Provide meaningful error messages
5. Maintain fallback mechanisms

## Additional Resources

- [AWS SDK Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Azure SDK Documentation](https://docs.microsoft.com/python/azure/)
- [Google Cloud SDK Documentation](https://googleapis.dev/python/google-api-core/latest/index.html)
- [API Security Guide](security.md)
- [Performance Optimization](performance.md)
