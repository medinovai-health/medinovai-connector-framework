"""NCATS N3C enclave — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class N3CConnector(BaseConnector):
    """Bring-code-to-data enclave API (stub)."""

    def __init__(self) -> None:
        super().__init__("n3c", "NCATS N3C")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "nih_2fa",
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
        }
