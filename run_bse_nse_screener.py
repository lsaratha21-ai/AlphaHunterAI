"""Generate BSE/NSE small-cap screener results with real company examples."""

from app.screeners import get_bse_nse_small_cap_examples, SmallCapScreener


def main() -> None:
    """Generate and display BSE/NSE small-cap screener results."""

    screener = SmallCapScreener(
        max_market_cap=16000000000,  # ₹1,600 crore (approx $2B)
        max_debt_to_equity=1.0,
        min_roe=10.0,
    )

    # Get real BSE/NSE company examples
    companies_data = []
    bse_nse_examples = get_bse_nse_small_cap_examples()

    for symbol, data in bse_nse_examples.items():
        companies_data.append({
            "symbol": symbol,
            "company_name": data["company_name"],
            "market_cap": data["market_cap"],
            "roe": data["roe"],
            "debt_to_equity": data["debt_to_equity"],
            "institutional_ownership": data["institutional_ownership"],
        })

    # Mock historical data for demonstration
    historical_data = {
        "CENTURYTEX": {
            "roe_history": [10.5, 11.0, 11.8, 12.0],  # Improving
            "institutional_ownership_history": [20.0, 21.0, 21.5, 22.0],  # Increasing
        },
    }

    results = screener.screen_small_cap_companies(companies_data, historical_data)

    print("BSE/NSE Small-Cap Companies with Improving ROE, Low Debt, and Increasing Institutional Ownership")
    print("=" * 100)
    print()

    if not results:
        print("No companies match the screening criteria.")
        print()
        print("This is because most of the example companies are large-cap or mid-cap.")
        print("To see results, we need actual small-cap companies (< ₹1,600 crore).")
        return

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.symbol} - {result.company_name}")
        print("-" * 100)
        print(f"   Market Cap: ₹{result.market_cap/10000000:.0f} crore")
        print(f"   Current ROE: {result.current_roe:.1f}% (Trend: {result.roe_trend})")
        print(f"   Debt-to-Equity: {result.debt_to_equity:.2f}")
        print(f"   Institutional Ownership: {result.institutional_ownership:.1f}% (Trend: {result.institutional_trend})")
        print(f"   Overall Score: {result.overall_score:.1f}/100")
        print()
        print("   WHY IT MATCHES:")
        print(f"   ✓ Small-cap: Market cap ₹{result.market_cap/10000000:.0f} crore < ₹1,600 crore threshold")
        print(f"   ✓ Improving ROE: ROE increased from historical average, trend = {result.roe_trend}")
        print(f"   ✓ Low debt: Debt-to-equity {result.debt_to_equity:.2f} < 1.0 threshold")
        print(f"   ✓ Increasing institutional ownership: {result.institutional_trend} trend")
        print()
        print("=" * 100)
        print()

    # Show all BSE/NSE examples with their characteristics
    print("BSE/NSE COMPANY EXAMPLES AND WHY THEY MATCH/ DON'T MATCH:")
    print("=" * 100)
    print()

    for symbol, data in bse_nse_examples.items():
        print(f"{symbol} - {data['company_name']}")
        print(f"   Market Cap: ₹{data['market_cap']/10000000:.0f} crore")
        print(f"   ROE: {data['roe']:.1f}%")
        print(f"   Debt-to-Equity: {data['debt_to_equity']:.2f}")
        print(f"   Institutional Ownership: {data['institutional_ownership']:.1f}%")
        print(f"   Notes: {data['notes']}")
        print()


if __name__ == "__main__":
    main()
