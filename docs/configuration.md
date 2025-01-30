# Configuration Guide

This guide explains how to configure the AI Cloud Dashboard for your specific needs.

## Environment Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# API Keys
AWS_ACCESS_KEY=your_aws_key
AWS_SECRET_KEY=your_aws_secret
AZURE_API_KEY=your_azure_key
GCP_API_KEY=your_gcp_key

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aicloud_dashboard
DB_USER=admin
DB_PASSWORD=secure_password

# Cache Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=cache_password

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Configuration Files

#### config/default.yaml
```yaml
server:
  port: 8501
  host: 0.0.0.0
  workers: 4

database:
  pool_size: 20
  timeout: 30
  max_connections: 100

cache:
  ttl: 3600
  max_size: 1000

monitoring:
  enabled: true
  interval: 60
```

## Feature Configuration

### Market Intelligence

```yaml
market_intelligence:
  update_interval: 300  # 5 minutes
  data_sources:
    - aws_marketplace
    - azure_market
    - gcp_marketplace
  metrics:
    - market_share
    - growth_rate
    - adoption_rate
```

### Security & Compliance

```yaml
security:
  encryption:
    algorithm: AES-256
    key_rotation: 90  # days
  compliance:
    frameworks:
      - SOC2
      - HIPAA
      - GDPR
    scan_interval: 86400  # 24 hours
```

### Performance Monitoring

```yaml
monitoring:
  metrics:
    - cpu_usage
    - memory_usage
    - response_time
    - error_rate
  alerts:
    cpu_threshold: 80
    memory_threshold: 85
    response_time_threshold: 1000
```

## Customization

### UI Customization

Edit `config/ui.yaml`:
```yaml
theme:
  primary_color: "#007bff"
  secondary_color: "#6c757d"
  font_family: "Arial, sans-serif"
  dark_mode: true

layout:
  sidebar_width: 250
  chart_height: 400
  table_rows_per_page: 25
```

### Chart Configuration

Edit `config/charts.yaml`:
```yaml
charts:
  default_type: "line"
  color_palette:
    - "#1f77b4"
    - "#ff7f0e"
    - "#2ca02c"
  animations: true
  responsive: true
```

## Advanced Configuration

### Caching Strategy

```yaml
cache:
  strategies:
    market_data:
      ttl: 300
      max_size: 500
    user_preferences:
      ttl: 86400
      max_size: 100
    api_responses:
      ttl: 60
      max_size: 1000
```

### Load Balancing

```yaml
load_balancer:
  algorithm: "round_robin"
  health_check:
    interval: 30
    timeout: 5
    unhealthy_threshold: 3
  session_persistence: true
```

### Logging

```yaml
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    file:
      filename: "logs/dashboard.log"
      max_bytes: 10485760  # 10MB
      backup_count: 5
    syslog:
      enabled: true
      facility: "local0"
```

## Environment-Specific Configuration

### Development

```yaml
environment:
  name: development
  debug: true
  hot_reload: true
  mock_services: true
```

### Production

```yaml
environment:
  name: production
  debug: false
  hot_reload: false
  mock_services: false
  ssl:
    enabled: true
    cert_path: "/etc/ssl/certs/dashboard.crt"
    key_path: "/etc/ssl/private/dashboard.key"
```

## Troubleshooting

If you encounter configuration issues:

1. Verify all required environment variables are set
2. Check file permissions for configuration files
3. Validate YAML syntax
4. Review logs for configuration-related errors

## Best Practices

1. Use environment variables for sensitive information
2. Keep different configurations for development and production
3. Regularly review and update security settings
4. Document all custom configurations
5. Maintain configuration version control

## Additional Resources

- [Environment Variables Guide](environment-variables.md)
- [Security Configuration](security.md)
- [Performance Tuning](performance.md)
- [Logging Configuration](logging.md)
