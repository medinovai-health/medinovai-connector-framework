"""PCORnet federated CDM — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class PcornetConnector(BaseConnector):
    """Site-level VPN + CDM query distribution (stub)."""

    def __init__(self) -> None:
        super().__init__("pcornet", "PCORnet")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "site_vpn",
            "ok": False,
            "detail": "stub",
        }

    async def health_check(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "healthy": False,
            "detail": "stub_not_configured",
            "vpn": "unknown",
        }

    async def ingest(self, mos_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "accepted": False,
            "detail": "stub_ingest",
        }
