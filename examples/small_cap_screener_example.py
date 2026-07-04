"""Example usage of SmallCapScreener."""

from app.screeners import SmallCapScreener


def main() -> None:
    """Demonstrate small-cap screener functionality."""

    # Create screener with custom thresholds
    screener = SmallCapScreener(
        max_market_cap=2000000000,  # $2B small-cap threshold
        max_debt_to_equity=1.0,  # Low debt
        min_roe=10.0,  # Minimum ROE
    )

    # Mock company data
    companies = [
        {
            "symbol": "ABC",
            "company_name": "ABC Technologies",
            "market_cap": 1500000000,  # $1.5B
            "roe": 15.5,
            "debt_to_equity": 0.4,
            "institutional_ownership": 25.0,
        },
        {
            "symbol": "XYZ",
            "company_name": "XYZ Manufacturing",
            "market_cap": 800000000,  # $800M
            "roe": 18.2,
            "debt_to_equity": 0.3,
            "institutional_ownership": 30.0,
        },
        {
            "symbol": "DEF",
            "company_name": "DEF Services",
            "market_cap": 2500000000,  # $2.5B (too large)
            "roe": 20.0,
            "debt_to_equity": 0.5,
            "institutional_ownership": 35.0,
        },
        {
            "symbol": "GHI",
            "company_name": "GHI Industries",
            "market_cap": 1200000000,  # $1.2B
            "roe": 8.0,  # Too low
            "debt_to_equity": 0.4,
            "institutional_ownership": 20.0,
        },
        {
            "symbol": "JKL",
            "company_name": "JKL Corporation",
            "market_cap": 1800000000,  # $1.8B
            "roe": 16.0,
            "debt_to_equity": 1.5,  # Too high debt
            "institutional_ownership": 28.0,
        },
        {
            "symbol": "MNO",
            "company_name": "MNO Solutions",
            "market_cap": 900000000,  # $900M
            "roe": 19.5,
            "debt_to_equity": 0.2,
            "institutional_ownership": 32.0,
        },
    ]

    # Mock historical data for trend analysis
    historical_data = {
        "ABC": {
            "roe_history": [12.0, 13.5, 14.8, 15.5],  # Improving
            "institutional_ownership_history": [20.0, 22.0, 24.0, 25.0],  # Increasing
        },
        "XYZ": {
            "roe_history": [15.0, 16.5, 17.2, 18.2],  # Improving
            "institutional_ownership_history": [25.0, 27.0, 29.0, 30.0],  # Increasing
        },
        "MNO": {
            "roe_history": [17.0, 18.0, 18.8, 19.5],  # Improving
            "institutional_ownership_history": [28.0, 30.0, 31.0, 32.0],  # Increasing
        },
    }

    # Run screener
    results = screener.screen_small_cap_companies(companies, historical_data)

    # Display results
    print("Small-Cap Companies with Improving ROE, Low Debt, and Increasing Institutional Ownership")
    print("=" * 100)
    print()

    if not results:
        print("No companies match the screening criteria.")
        return

    for result in results:
        print(f"Symbol: {result.symbol}")
        print(f"Company: {result.company_name}")
        print(f"Market Cap: ${result.market_cap:,.0f}")
        print(f"Current ROE: {result.current_roe:.1f}% (Trend: {result.roe_trend})")
        print(f"Debt-to-Equity: {result.debt_to_equity:.2f}")
        print(f"Institutional Ownership: {result.institutional_ownership:.1f}% (Trend: {result.institutional_trend})")
        print(f"Overall Score: {result.overall_score:.1f}/100")
        print("-" * 100)
        print()

    # Display summary
    summary = screener.get_screening_summary(results)
    print("Screening Summary:")
    print(f"Total Companies: {summary['total_companies']}")
    print(f"Average ROE: {summary['average_roe']:.1f}%")
    print(f"Average Debt-to-Equity: {summary['average_debt_to_equity']:.2f}")
    print(f"Average Institutional Ownership: {summary['average_institutional_ownership']:.1f}%")
    print(f"Average Score: {summary['average_score']:.1f}/100")


if __name__ == "__main__":
    main()
