"""Main script to run the weekly scheduler."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.scheduler import WeeklyScheduler


def main() -> None:
    """Run the weekly scheduler."""
    # Configuration
    symbols = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
        "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
        "LT", "AXISBANK", "BAJFINANCE", "MARUTI", "TATAMOTORS",
        "SUNPHARMA", "WIPRO", "TITAN", "HCLTECH", "ASIANPAINT",
    ]

    sectors = [
        "Technology", "Healthcare", "Finance", "Energy",
        "Consumer", "Industrial", "Automotive", "Pharmaceuticals",
    ]

    # Email configuration (set in environment or config file in production)
    email_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "email": None,  # Set from environment
        "password": None,  # Set from environment
    }

    recipients = [
        # Add recipient emails here
    ]

    # Initialize scheduler
    scheduler = WeeklyScheduler(
        data_dir="data",
        output_dir="reports",
        archive_dir="archive",
        email_config=email_config,
    )

    # Run weekly report
    print("Starting weekly report generation...")
    report = scheduler.run_weekly_report(
        symbols=symbols,
        sectors=sectors,
        recipients=recipients if recipients else None,
    )

    print(f"Report ID: {report.report_id}")
    print(f"Status: {report.status.value}")
    print(f"Report Date: {report.report_date}")

    if report.status.value == "completed":
        print(f"Report File: {report.file_path}")
        print("Weekly report generated successfully!")
    else:
        print(f"Error: {report.error_message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
