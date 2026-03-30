"""Datavant tokenization / linkage — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class DatavantConnector(BaseConnector):
    """Privacy-preserving tokenization APIs (stub)."""

    def __init__(self) -> None:
        super().__init__("datavant", "Datavant")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "api_key",
            "ok": False,
            "detail": "stub",
        }

    async def health_check(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "healthy": False,
            "detail": "stub_not_configured",
        }

    async def ingest(self, mos_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "accepted": False,
            "detail": "stub_ingest",
            "field_count": len(mos_payload),
        }
