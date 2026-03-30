"""AWS HealthLake connector (FHIR R4) — scaffold."""

from __future__ import annotations

from typing import Any, Dict

from connectors.base import BaseConnector


class AwsHealthLakeConnector(BaseConnector):
    """FHIR R4 REST against AWS HealthLake (SigV4 in future sessions)."""

    def __init__(self) -> None:
        super().__init__("aws", "AWS HealthLake")

    async def authenticate(self) -> Dict[str, Any]:
        return {
            "platform": self.mos_platformKey,
            "auth": "aws_iam_sts",
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
