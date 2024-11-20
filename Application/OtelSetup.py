from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from typing import Optional, Dict, List

class OTelSetup:
    _instance = None

    def __init__(self, 
                 service_name: str,
                 service_version: str,
                 environment: Optional[str] = None,
                 debug: bool = False,
                 exporters: List[Dict[str, str]] = None):
        """Initialize OpenTelemetry setup"""
        self.service_name = service_name
        self.service_version = service_version
        
        # Create resource
        resource = Resource.create({
            "service.name": service_name,
            "service.version": service_version,
            **({"deployment.environment": environment} if environment else {})
        })

        # Create provider
        provider = TracerProvider(resource=resource)

        # Setup exporters
        if exporters:
            for exporter_config in exporters:
                otlp_exporter = OTLPSpanExporter(
                    endpoint=exporter_config.get("endpoint"),
                    headers=exporter_config.get("headers", {})
                )
                processor = BatchSpanProcessor(otlp_exporter)
                provider.add_span_processor(processor)
        
        # Set global provider
        trace.set_tracer_provider(provider)
        self.provider = provider

    @classmethod
    def initialize(cls, **kwargs) -> 'OTelSetup':
        """Initialize the singleton instance"""
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'OTelSetup':
        """Get the singleton instance"""
        if cls._instance is None:
            raise RuntimeError("OTelSetup not initialized")
        return cls._instance

    def get_tracer(self) -> trace.Tracer:
        """Get a tracer instance"""
        return trace.get_tracer(self.service_name, self.service_version)