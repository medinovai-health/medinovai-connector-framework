"""Azure Health Data Services (FHIR R4) — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class AzureHdsConnector(BaseConnector):
    """Azure AD / managed identity FHIR (stub)."""

    def __init__(self) -> None:
        super().__init__("azure", "Azure Health Data Services")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "azure_ad_managed_identity",
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
