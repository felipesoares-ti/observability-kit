import os
from fastapi import FastAPI, Request
import logging
import time
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import structlog

# Structured logging setup
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

app = FastAPI()

# CORS (ajuste origins conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of HTTP requests", ["method", "endpoint"])

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    method = request.method
    path = request.url.path
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error("Unhandled exception", error=str(exc), path=path)
        raise
    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=method, endpoint=path).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=path).observe(latency)
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Global exception handler", error=str(exc), path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.get("/metrics")
def metrics():
    """Exibe métricas Prometheus."""
    return Response(generate_latest(), media_type="text/plain")

@app.get("/ping")
def ping():
    """Endpoint de teste de vida."""
    logger.info("Received ping request")
    return {"message": "pong"}

@app.get("/healthz")
def healthz():
    """Health check para orquestradores."""
    return {"status": "ok"}

# OpenTelemetry tracing setup
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318/v1/traces")
resource = Resource(attributes={SERVICE_NAME: "observability-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT))
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrumentations
FastAPIInstrumentor.instrument_app(app)
LoggingInstrumentor().instrument()
RequestsInstrumentor().instrument()
