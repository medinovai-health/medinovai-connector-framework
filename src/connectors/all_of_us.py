"""NIH All of Us Research Program — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class AllOfUsConnector(BaseConnector):
    """Workbench API cohort / controlled tier (stub)."""

    def __init__(self) -> None:
        super().__init__("all_of_us", "NIH All of Us")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "nih_workspace",
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
