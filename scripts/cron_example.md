# Data Ingestion Cron Setup

This guide explains how to set up automated data ingestion using cron.

## Quick Setup

### 1. Make the script executable
```bash
chmod +x scripts/fetch_data.py
```

### 2. Test the script manually
```bash
python scripts/fetch_data.py --force
```

### 3. Add to crontab

Edit your crontab:
```bash
crontab -e
```

Add one of these schedules:

**Daily at 2 AM:**
```cron
0 2 * * * cd /path/to/ai_cloud_dashboard && python scripts/fetch_data.py >> /var/log/cloud-dashboard-fetch.log 2>&1
```

**Every 6 hours:**
```cron
0 */6 * * * cd /path/to/ai_cloud_dashboard && python scripts/fetch_data.py >> /var/log/cloud-dashboard-fetch.log 2>&1
```

**Every 12 hours:**
```cron
0 */12 * * * cd /path/to/ai_cloud_dashboard && python scripts/fetch_data.py >> /var/log/cloud-dashboard-fetch.log 2>&1
```

## Docker Setup

If running in Docker, use the container's cron:

```dockerfile
# Add to Dockerfile
RUN apt-get update && apt-get install -y cron
COPY scripts/crontab /etc/cron.d/cloud-dashboard
RUN chmod 0644 /etc/cron.d/cloud-dashboard && crontab /etc/cron.d/cloud-dashboard
```

Create `scripts/crontab`:
```
0 2 * * * cd /app && python scripts/fetch_data.py >> /var/log/cron.log 2>&1
```

## Monitoring

Check logs:
```bash
tail -f /var/log/cloud-dashboard-fetch.log
```

Check cache freshness:
```bash
cat data/.freshness
```

## Manual Force Refresh

Force a refresh ignoring cache:
```bash
python scripts/fetch_data.py --force
```
