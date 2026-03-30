"""Connector registry — slug → instance."""

from __future__ import annotations

from typing import Dict

from connectors.all_of_us import AllOfUsConnector
from connectors.aws_healthlake import AwsHealthLakeConnector
from connectors.azure_hds import AzureHdsConnector
from connectors.base import BaseConnector
from connectors.datavant import DatavantConnector
from connectors.mayo_mcp import MayoMcpConnector
from connectors.n3c import N3CConnector
from connectors.pcornet import PcornetConnector
from connectors.trinetx import TriNetXConnector

E_CONNECTOR_SLUGS: tuple[str, ...] = (
    "aws",
    "datavant",
    "trinetx",
    "n3c",
    "pcornet",
    "mayo",
    "azure",
    "all_of_us",
)

_mos_registry: Dict[str, BaseConnector] | None = None


def get_connector_registry() -> Dict[str, BaseConnector]:
    """Lazily build and return the connector map."""

    global _mos_registry
    if _mos_registry is None:
        _mos_registry = {
            "aws": AwsHealthLakeConnector(),
            "datavant": DatavantConnector(),
            "trinetx": TriNetXConnector(),
            "n3c": N3CConnector(),
            "pcornet": PcornetConnector(),
            "mayo": MayoMcpConnector(),
            "azure": AzureHdsConnector(),
            "all_of_us": AllOfUsConnector(),
        }
    return _mos_registry

