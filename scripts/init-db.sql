-- Initialize Cloud Dashboard PostgreSQL database

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS cache;
CREATE SCHEMA IF NOT EXISTS audit;

-- Pricing data table
CREATE TABLE IF NOT EXISTS analytics.cloud_pricing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(50) NOT NULL,
    service VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    instance_type VARCHAR(100),
    price_per_hour DECIMAL(10, 6),
    currency VARCHAR(10) DEFAULT 'USD',
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_provider (provider),
    INDEX idx_service (service),
    INDEX idx_region (region),
    INDEX idx_fetched_at (fetched_at)
);

-- Usage metrics table
CREATE TABLE IF NOT EXISTS analytics.usage_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 2),
    labels JSONB,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric_name (metric_name),
    INDEX idx_recorded_at (recorded_at)
);

-- Compliance checks table
CREATE TABLE IF NOT EXISTS analytics.compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    check_name VARCHAR(200) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pass', 'fail', 'warning', 'unknown')),
    details JSONB,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_provider_status (provider, status),
    INDEX idx_checked_at (checked_at)
);

-- Cache metadata table
CREATE TABLE IF NOT EXISTS cache.metadata (
    cache_key VARCHAR(255) PRIMARY KEY,
    size_bytes BIGINT,
    record_count INTEGER,
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit.event_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Create views
CREATE OR REPLACE VIEW analytics.latest_pricing AS
SELECT DISTINCT ON (provider, service, region, instance_type)
    *
FROM analytics.cloud_pricing
ORDER BY provider, service, region, instance_type, fetched_at DESC;

-- Grant permissions
GRANT USAGE ON SCHEMA analytics TO dashboard;
GRANT USAGE ON SCHEMA cache TO dashboard;
GRANT USAGE ON SCHEMA audit TO dashboard;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA analytics TO dashboard;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA cache TO dashboard;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA audit TO dashboard;

-- Create function to clean old pricing data (retain last 90 days)
CREATE OR REPLACE FUNCTION analytics.cleanup_old_pricing()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM analytics.cloud_pricing
    WHERE fetched_at < NOW() - INTERVAL '90 days';

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Vacuum analyze
VACUUM ANALYZE;
