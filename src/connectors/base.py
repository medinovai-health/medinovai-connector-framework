"""Abstract base connector — Phase E standard interface (scaffold)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConnector(ABC):
    """Pluggable connector to an external health data platform."""

    def __init__(self, mos_platformKey: str, mos_displayName: str) -> None:
        self.mos_platformKey = mos_platformKey
        self.mos_displayName = mos_displayName

    @abstractmethod
    async def authenticate(self) -> Dict[str, Any]:
        """Establish or validate session with the external platform."""

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Verify connectivity and credential configuration (no PHI in response)."""

    @abstractmethod
    async def ingest(self, mos_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Accept canonical ingest payload and return job metadata (stub)."""

    async def fetch_data(self, mos_query: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve platform-native data — optional until implemented."""

        raise NotImplementedError("fetch_data not implemented for this connector")

    async def transform(self, mos_raw: Dict[str, Any]) -> Dict[str, Any]:
        """Convert platform payload to MedinovAI canonical form — optional."""

        raise NotImplementedError("transform not implemented for this connector")

    async def get_rate_limit_status(self) -> Dict[str, Any]:
        """Return rate limit consumption hint for this connector."""

        return {
            "platform": self.mos_platformKey,
            "remaining": None,
            "note": "not_configured",
        }

    def describe(self) -> Dict[str, Any]:
        """Static metadata for the registry endpoint."""

        return {
            "id": self.mos_platformKey,
            "display_name": self.mos_displayName,
            "status": "stub",
        }
