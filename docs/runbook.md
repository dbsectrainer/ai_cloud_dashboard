# Cloud Dashboard Operations Runbook

**Version**: 0.2.0
**Last Updated**: 2025-11-08

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run locally
streamlit run src/app.py

# Run tests
pytest

# Run data ingestion
python scripts/fetch_data.py --force
```

### Production Deployment

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down
```

---

## Service Architecture

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| app | 8501 | Streamlit dashboard | http://localhost:8501/_stcore/health |
| postgres | 5432 | Metadata storage | `docker exec -it cloud-dashboard-db pg_isready` |
| minio | 9000, 9001 | Object storage | http://localhost:9001 |
| otel-collector | 4318 | Telemetry collection | http://localhost:8888/metrics |
| prometheus | 9090 | Metrics storage | http://localhost:9090/-/healthy |
| grafana | 3000 | Observability | http://localhost:3000/api/health |

---

## Common Operations

### Data Ingestion

**Manual refresh:**
```bash
python scripts/fetch_data.py --force
```

**Check cache freshness:**
```bash
cat data/.freshness
```

**View ingestion logs:**
```bash
docker compose logs -f app | grep ingestion
```

### Database Operations

**Connect to PostgreSQL:**
```bash
docker exec -it cloud-dashboard-db psql -U dashboard -d clouddb
```

**Run analytics query:**
```sql
SELECT provider, COUNT(*), AVG(price_per_hour)
FROM analytics.cloud_pricing
GROUP BY provider;
```

**Clean old data:**
```sql
SELECT analytics.cleanup_old_pricing();
```

### Monitoring

**Prometheus metrics:**
- http://localhost:9090/graph
- Query: `cloud_dashboard_ingestion_requests_total`

**Grafana dashboards:**
- http://localhost:3000 (admin/admin)
- Dashboard: "Cloud Dashboard - Data Ingestion"

**OTel Collector:**
- http://localhost:8888/metrics

---

## Troubleshooting

### Issue: Dashboard won't start

**Symptoms:**
- `streamlit run` fails
- Container restarts repeatedly

**Diagnosis:**
```bash
# Check logs
docker compose logs app

# Check dependencies
pip check

# Verify Python version
python --version  # Should be 3.11+
```

**Resolution:**
1. Reinstall dependencies: `pip install -r requirements.txt`
2. Check `.env` file exists and has correct values
3. Verify ports 8501 not in use: `lsof -i :8501`

### Issue: Data ingestion failing

**Symptoms:**
- Cache is stale
- "No data available" errors in UI

**Diagnosis:**
```bash
# Run fetch manually with verbose logging
python scripts/fetch_data.py --force

# Check cache directory
ls -lh data/cache/

# Check cache metadata
python -c "from src.ingestion.cache import CacheManager; print(CacheManager('data/cache').get_stats())"
```

**Resolution:**
1. Check network connectivity to pricing APIs
2. Verify cache directory permissions
3. Clear and rebuild cache: `rm -rf data/cache/* && python scripts/fetch_data.py --force`

### Issue: Database connection errors

**Symptoms:**
- `psycopg2.OperationalError`
- "Could not connect to server" errors

**Diagnosis:**
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Test connection
docker exec -it cloud-dashboard-db pg_isready -U dashboard

# Check DATABASE_URL in .env
grep DATABASE_URL .env
```

**Resolution:**
1. Restart PostgreSQL: `docker compose restart postgres`
2. Verify credentials match between .env and docker-compose.yml
3. Check network connectivity: `docker network ls`

### Issue: High memory usage

**Symptoms:**
- Container OOMKilled
- System slowness

**Diagnosis:**
```bash
# Check container stats
docker stats cloud-dashboard

# Check cache size
du -sh data/cache/
```

**Resolution:**
1. Reduce `CACHE_MAX_SIZE_MB` in .env
2. Increase Docker memory limit
3. Clear old cache entries

### Issue: Metrics not appearing in Grafana

**Symptoms:**
- Empty graphs
- "No data" in dashboards

**Diagnosis:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq

# Check OTel collector
curl http://localhost:8888/metrics

# Verify telemetry enabled
grep ENABLE_TELEMETRY .env
```

**Resolution:**
1. Verify `ENABLE_TELEMETRY=true` in .env
2. Restart OTel collector: `docker compose restart otel-collector`
3. Check Prometheus datasource config in Grafana

---

## Maintenance

### Daily

- [ ] Check dashboard health: http://localhost:8501
- [ ] Verify data freshness: `cat data/.freshness`
- [ ] Review error logs: `docker compose logs --tail=100 app`

### Weekly

- [ ] Review Grafana metrics for anomalies
- [ ] Check cache size: `du -sh data/cache/`
- [ ] Verify backup jobs completed
- [ ] Update dependencies: `pip list --outdated`

### Monthly

- [ ] Database cleanup: `SELECT analytics.cleanup_old_pricing();`
- [ ] Security scans: `docker run aquasec/trivy image cloud-dashboard:latest`
- [ ] Dependency audit: `pip-audit`
- [ ] Review and rotate credentials

---

## Backup & Recovery

### Backup Database

```bash
# Dump PostgreSQL
docker exec cloud-dashboard-db pg_dump -U dashboard clouddb > backup_$(date +%Y%m%d).sql

# Backup to S3 (if configured)
aws s3 cp backup_$(date +%Y%m%d).sql s3://your-bucket/backups/
```

### Restore Database

```bash
# Restore from dump
cat backup_20251108.sql | docker exec -i cloud-dashboard-db psql -U dashboard clouddb
```

### Backup Cache

```bash
# Tar cache directory
tar -czf cache_backup_$(date +%Y%m%d).tar.gz data/cache/
```

---

## Performance Tuning

### Cache Optimization

```bash
# Adjust cache settings in .env
CACHE_TTL_SECONDS=7200        # Increase for less frequent updates
CACHE_MAX_SIZE_MB=1000        # Increase for more cached data
```

### Database Tuning

```sql
-- Analyze tables for query optimization
ANALYZE analytics.cloud_pricing;

-- Create indexes
CREATE INDEX CONCURRENTLY idx_pricing_provider_region
ON analytics.cloud_pricing(provider, region);
```

### Container Resources

```yaml
# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          memory: 2G
```

---

## Security Procedures

### Rotate Secrets

```bash
# Generate new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env
vim .env  # Update SECRET_KEY

# Restart services
docker compose restart app
```

### Update Dependencies

```bash
# Check for vulnerabilities
pip-audit

# Update packages
pip install --upgrade -r requirements.txt

# Run tests
pytest

# Rebuild image
docker compose build app
```

---

## Escalation

| Severity | Response Time | Contact |
|----------|--------------|---------|
| P0 - Critical (Production down) | 15 minutes | On-call engineer |
| P1 - High (Degraded performance) | 1 hour | Team lead |
| P2 - Medium (Non-critical bug) | 4 hours | Engineering team |
| P3 - Low (Feature request) | Best effort | Product team |

**On-call rotation**: See internal wiki
**Incident process**: See [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

---

## References

- [Architecture Diagram](ARCHITECTURE.md)
- [SLOs](slo.md)
- [Security](../SECURITY.md)
- [Compliance](compliance_map.md)
