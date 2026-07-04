"""Generate diversified portfolio example for user."""

from datetime import datetime

from app.alpha import AlphaScore, AlphaScoreComponents, ComponentScore
from app.portfolio import PortfolioConstructor


def create_mock_alpha_scores() -> list[AlphaScore]:
    """Create mock AlphaScore recommendations for demonstration.

    Returns:
        List of AlphaScore objects.
    """
    scores = []

    # High quality recommendation
    components1 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 18.0, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 14.0, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 13.0, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 9.0, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 9.0, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 9.0, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 4.0, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
        risk=ComponentScore("Risk", 4.0, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="TCS",
        overall_score=88.0,
        components=components1,
        action="buy",
        confidence=85.0,
        current_price=3500.0,
        target_price=4200.0,
        stop_loss=3080.0,
        reasoning="Strong financial quality and institutional buying",
        timestamp=datetime.now(),
    ))

    # Mid-cap growth
    components2 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 16.5, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 13.5, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 12.0, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 8.5, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 8.5, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 8.5, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 4.5, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
        risk=ComponentScore("Risk", 3.5, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="HDFCBANK",
        overall_score=83.5,
        components=components2,
        action="buy",
        confidence=80.0,
        current_price=1650.0,
        target_price=1980.0,
        stop_loss=1452.0,
        reasoning="Strong banking sector momentum",
        timestamp=datetime.now(),
    ))

    # Small-cap opportunity
    components3 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 15.0, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 13.0, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 12.5, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 8.0, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 8.0, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 8.0, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 4.0, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 3.5, 5.0, 5.0),
        risk=ComponentScore("Risk", 3.5, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 3.5, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="INFY",
        overall_score=79.5,
        components=components3,
        action="buy",
        confidence=75.0,
        current_price=1450.0,
        target_price=1740.0,
        stop_loss=1276.0,
        reasoning="IT sector showing strong momentum",
        timestamp=datetime.now(),
    ))

    # Value opportunity
    components4 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 17.0, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 12.0, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 11.5, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 8.0, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 8.5, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 8.0, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 5.0, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
        risk=ComponentScore("Risk", 4.0, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="RELIANCE",
        overall_score=86.0,
        components=components4,
        action="buy",
        confidence=82.0,
        current_price=2800.0,
        target_price=3360.0,
        stop_loss=2464.0,
        reasoning="Strong financials and attractive valuation",
        timestamp=datetime.now(),
    ))

    # Growth stock
    components5 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 14.5, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 14.0, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 13.0, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 9.0, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 8.5, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 9.0, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 3.5, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
        risk=ComponentScore("Risk", 3.0, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="BAJFINANCE",
        overall_score=82.5,
        components=components5,
        action="buy",
        confidence=78.0,
        current_price=7200.0,
        target_price=8640.0,
        stop_loss=6336.0,
        reasoning="Strong growth momentum in financial services",
        timestamp=datetime.now(),
    ))

    # Defensive play
    components6 = AlphaScoreComponents(
        financial_quality=ComponentScore("Financial Quality", 18.5, 20.0, 20.0),
        growth_acceleration=ComponentScore("Growth Acceleration", 11.0, 15.0, 15.0),
        technical_momentum=ComponentScore("Technical Momentum", 10.5, 15.0, 15.0),
        sector_momentum=ComponentScore("Sector Momentum", 8.0, 10.0, 10.0),
        management_guidance=ComponentScore("Management Guidance", 9.0, 10.0, 10.0),
        institutional_buying=ComponentScore("Institutional Buying", 8.5, 10.0, 10.0),
        valuation=ComponentScore("Valuation", 4.0, 5.0, 5.0),
        order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
        risk=ComponentScore("Risk", 4.5, 5.0, 5.0),
        earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
    )

    scores.append(AlphaScore(
        symbol="ITC",
        overall_score=78.0,
        components=components6,
        action="hold",
        confidence=72.0,
        current_price=450.0,
        target_price=540.0,
        stop_loss=396.0,
        reasoning="Defensive FMCG stock with steady returns",
        timestamp=datetime.now(),
    ))

    return scores


def main() -> None:
    """Generate and display diversified portfolio."""
    # Parameters
    total_capital = 1000000  # ₹10 lakh
    risk_tolerance = "moderate"
    horizon_months = 3

    # Create mock recommendations
    alpha_scores = create_mock_alpha_scores()

    # Construct portfolio
    constructor = PortfolioConstructor()
    portfolio = constructor.construct_portfolio(
        alpha_scores=alpha_scores,
        total_capital=total_capital,
        risk_tolerance=risk_tolerance,
        horizon_months=horizon_months,
        portfolio_name="AlphaHunter 3-Month Portfolio",
    )

    # Display portfolio
    print("=" * 100)
    print(f"ALPHAHUNTER DIVERSIFIED PORTFOLIO")
    print("=" * 100)
    print()
    print(f"Portfolio Name: {portfolio.name}")
    print(f"Total Capital: ₹{portfolio.total_capital:,.0f}")
    print(f"Risk Tolerance: {portfolio.risk_profile.risk_tolerance}")
    print(f"Horizon: {portfolio.horizon_months} months")
    print(f"Created: {portfolio.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    summary = portfolio.get_summary()
    print("PORTFOLIO SUMMARY:")
    print("-" * 50)
    print(f"Invested Amount: ₹{summary['invested_amount']:,.0f}")
    print(f"Cash: ₹{summary['cash']:,.0f} ({summary['cash_percentage']:.1f}%)")
    print(f"Number of Positions: {summary['number_of_positions']}")
    print(f"Average Alpha Score: {summary['average_alpha_score']:.1f}")
    print(f"Average Weight: {summary['average_weight']:.1f}%")
    print()

    print("POSITIONS:")
    print("=" * 100)
    print()

    for i, position in enumerate(portfolio.positions, 1):
        print(f"{i}. {position.symbol} ({position.company_name})")
        print("-" * 100)
        print(f"   Alpha Score: {position.alpha_score:.1f}/100")
        print(f"   Action: {position.action.upper()}")
        print(f"   Weight: {position.weight:.1f}%")
        print(f"   Position Size: ₹{position.position_size:,.0f}")
        print(f"   Shares: {position.shares}")
        print(f"   Entry Range: ₹{position.entry_price_low:.2f} - ₹{position.entry_price_high:.2f}")
        print(f"   Stop Loss: ₹{position.stop_loss:.2f} ({((position.stop_loss / position.entry_price_high - 1) * 100):.1f}%)")
        print(f"   Target: ₹{position.target_price:.2f} ({((position.target_price / position.entry_price_high - 1) * 100):.1f}%)")
        print(f"   Risk/Reward: {((position.target_price - position.entry_price_high) / (position.entry_price_high - position.stop_loss)):.2f}")
        if position.reasoning:
            print(f"   Reasoning: {position.reasoning}")
        print()

    print("RISK PROFILE:")
    print("-" * 50)
    print(f"Max Position Size: {portfolio.risk_profile.max_position_size}%")
    print(f"Max Sector Exposure: {portfolio.risk_profile.max_sector_exposure}%")
    print(f"Default Stop Loss: {portfolio.risk_profile.stop_loss_percentage}%")
    print(f"Default Target: {portfolio.risk_profile.target_percentage}%")
    print(f"Max Positions: {portfolio.risk_profile.max_positions}")
    print()

    print("REBALANCING NOTES:")
    print("-" * 50)
    print(f"- Review portfolio every 2 weeks")
    print(f"- Rebalance if any position deviates by ±5% from target weight")
    print(f"- Exit positions if stop loss or target is hit")
    print(f"- Maintain cash buffer of {summary['cash_percentage']:.1f}% for opportunities")
    print()


if __name__ == "__main__":
    main()
