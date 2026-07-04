"""NSE connector for bhavcopy and corporate actions."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
import pandas as pd
import zipfile
from io import BytesIO

from app.connectors.models import CorporateAction, OHLCVData
from app.core.exceptions import ProviderError


class NSEConnector:
    """Connector for NSE data sources."""

    def __init__(self, timeout: int = 30) -> None:
        """Initialize the NSE connector.

        Args:
            timeout: Request timeout in seconds.
        """
        self.timeout = timeout
        self.base_url = "https://www.nseindia.com"

    async def fetch_bhavcopy(
        self,
        date: datetime | None = None,
    ) -> list[OHLCVData]:
        """Fetch NSE bhavcopy data for a specific date.

        Args:
            date: Date for bhavcopy. If None, fetches latest.

        Returns:
            List of OHLCVData objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        try:
            if date is None:
                date = datetime.now()

            # NSE bhavcopy URL pattern
            date_str = date.strftime("%d%m%Y")
            year_str = date.strftime("%Y")
            month_str = date.strftime("%b").upper()

            url = f"{self.base_url}/products/dynaContent/equities/equities/json/{month_str}{year_str}/cm{date_str}bhav.csv.zip"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()

            # Extract CSV from zip
            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                csv_file = zip_ref.namelist()[0]
                with zip_ref.open(csv_file) as f:
                    df = pd.read_csv(f)

            # Process data
            data_points = []
            for _, row in df.iterrows():
                try:
                    data_point = OHLCVData(
                        symbol=row["SYMBOL"],
                        date=datetime.strptime(row["TIMESTAMP"], "%d-%b-%Y"),
                        open=float(row["OPEN"]),
                        high=float(row["HIGH"]),
                        low=float(row["LOW"]),
                        close=float(row["CLOSE"]),
                        volume=int(row["TOTTRDQTY"]),
                        adjusted_close=None,
                    )
                    data_points.append(data_point)
                except (KeyError, ValueError, TypeError) as e:
                    continue

            return data_points

        except httpx.HTTPStatusError as e:
            raise ProviderError(f"Failed to fetch NSE bhavcopy: HTTP {e.response.status_code}")
        except Exception as e:
            raise ProviderError(f"Failed to fetch NSE bhavcopy: {e}")

    async def fetch_corporate_actions(
        self,
        symbol: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[CorporateAction]:
        """Fetch NSE corporate actions.

        Args:
            symbol: Optional symbol filter.
            from_date: Optional start date filter.
            to_date: Optional end date filter.

        Returns:
            List of CorporateAction objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        try:
            # NSE corporate actions URL
            url = f"{self.base_url}/products/dynaContent/equities/equities/json/ CorpActionExport.json"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

            actions = []
            if data.get("data"):
                for item in data["data"]:
                    try:
                        # Parse date
                        announcement_date = datetime.strptime(
                            item["annDate"],
                            "%d-%b-%Y",
                        )
                        effective_date = None
                        if item.get("exDate"):
                            effective_date = datetime.strptime(
                                item["exDate"],
                                "%d-%b-%Y",
                            )

                        # Apply filters
                        if symbol and item.get("symbol") != symbol:
                            continue
                        if from_date and announcement_date < from_date:
                            continue
                        if to_date and announcement_date > to_date:
                            continue

                        action = CorporateAction(
                            symbol=item["symbol"],
                            action_type=item.get("subject", "unknown"),
                            announcement_date=announcement_date,
                            effective_date=effective_date,
                            description=item.get("desc", ""),
                            ratio=float(item.get("recordDate", 0)) if item.get("recordDate") else None,
                            amount=float(item.get("purpose", 0)) if item.get("purpose") else None,
                        )
                        actions.append(action)
                    except (KeyError, ValueError, TypeError) as e:
                        continue

            return actions

        except httpx.HTTPStatusError as e:
            raise ProviderError(f"Failed to fetch NSE corporate actions: HTTP {e.response.status_code}")
        except Exception as e:
            raise ProviderError(f"Failed to fetch NSE corporate actions: {e}")

    def fetch_bhavcopy_sync(
        self,
        date: datetime | None = None,
    ) -> list[OHLCVData]:
        """Synchronous version of fetch_bhavcopy.

        Args:
            date: Date for bhavcopy.

        Returns:
            List of OHLCVData objects.
        """
        import asyncio

        return asyncio.run(self.fetch_bhavcopy(date))

    def fetch_corporate_actions_sync(
        self,
        symbol: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[CorporateAction]:
        """Synchronous version of fetch_corporate_actions.

        Args:
            symbol: Optional symbol filter.
            from_date: Optional start date filter.
            to_date: Optional end date filter.

        Returns:
            List of CorporateAction objects.
        """
        import asyncio

        return asyncio.run(self.fetch_corporate_actions(symbol, from_date, to_date))
