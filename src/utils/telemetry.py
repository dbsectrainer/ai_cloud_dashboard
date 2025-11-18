"""OpenTelemetry instrumentation for observability."""

import logging

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)


def init_telemetry(
    service_name: str,
    endpoint: str | None = None,
    environment: str = "development",
) -> tuple[trace.Tracer, metrics.Meter]:
    """
    Initialize OpenTelemetry instrumentation for traces and metrics.

    Args:
        service_name: Name of the service for telemetry
        endpoint: OTLP collector HTTP endpoint (e.g., http://otel-collector:4318)
        environment: Deployment environment

    Returns:
        Tuple of (tracer, meter) for creating spans and metrics
    """
    if not endpoint:
        logger.warning("OTEL_ENDPOINT not configured. Telemetry disabled.")
        # Return no-op tracer and meter
        return trace.get_tracer(__name__), metrics.get_meter(__name__)

    # Create resource attributes
    resource = Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": environment,
            "service.version": "0.2.0",
        }
    )

    # Initialize tracing
    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")
    span_processor = BatchSpanProcessor(trace_exporter)
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)

    logger.info(f"Trace exporter configured: {endpoint}/v1/traces")

    # Initialize metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics"),
        export_interval_millis=30000,  # Export every 30 seconds
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    logger.info(f"Metric exporter configured: {endpoint}/v1/metrics")

    # Get tracer and meter instances
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)

    logger.info(f"OpenTelemetry initialized for service: {service_name}")

    return tracer, meter


def create_metrics(meter: metrics.Meter) -> dict:
    """
    Create application-specific metrics.

    Args:
        meter: OpenTelemetry Meter instance

    Returns:
        Dictionary of metric instruments
    """
    return {
        # Data ingestion metrics
        "ingestion_requests": meter.create_counter(
            name="ingestion_requests_total",
            description="Total number of data ingestion requests",
            unit="1",
        ),
        "ingestion_failures": meter.create_counter(
            name="ingestion_failures_total",
            description="Total number of failed ingestion requests",
            unit="1",
        ),
        "ingestion_duration": meter.create_histogram(
            name="ingestion_duration_seconds",
            description="Duration of data ingestion operations",
            unit="s",
        ),
        "cached_records": meter.create_up_down_counter(
            name="cached_records_total",
            description="Current number of cached records",
            unit="1",
        ),
        # Cache metrics
        "cache_hits": meter.create_counter(
            name="cache_hits_total",
            description="Total cache hits",
            unit="1",
        ),
        "cache_misses": meter.create_counter(
            name="cache_misses_total",
            description="Total cache misses",
            unit="1",
        ),
        "cache_size_bytes": meter.create_up_down_counter(
            name="cache_size_bytes",
            description="Current cache size in bytes",
            unit="By",
        ),
        # API metrics
        "api_requests": meter.create_counter(
            name="api_requests_total",
            description="Total API requests",
            unit="1",
        ),
        "api_errors": meter.create_counter(
            name="api_errors_total",
            description="Total API errors",
            unit="1",
        ),
        "api_duration": meter.create_histogram(
            name="api_duration_seconds",
            description="API request duration",
            unit="s",
        ),
        # Business metrics
        "cost_calculations": meter.create_counter(
            name="cost_calculations_total",
            description="Total TCO calculations performed",
            unit="1",
        ),
        "compliance_checks": meter.create_counter(
            name="compliance_checks_total",
            description="Total compliance checks performed",
            unit="1",
        ),
        "data_exports": meter.create_counter(
            name="data_exports_total",
            description="Total data exports",
            unit="1",
        ),
    }


# Global telemetry instances (initialized in app startup)
tracer: trace.Tracer | None = None
meter: metrics.Meter | None = None
app_metrics: dict | None = None
