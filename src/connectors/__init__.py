"""External platform connectors package."""

from connectors.registry import E_CONNECTOR_SLUGS, get_connector_registry

__all__ = ["E_CONNECTOR_SLUGS", "get_connector_registry"]
