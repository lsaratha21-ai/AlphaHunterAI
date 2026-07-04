# AlphaHunterAI

An intelligent stock screening and evaluation framework for Indian markets, designed to identify high-potential investment opportunities using comprehensive fundamental and technical analysis.

## Overview

AlphaHunterAI provides a systematic approach to stock screening with:
- **5 Avoid Criteria** (Red Flags) to filter out risky stocks
- **8 Consider Criteria** (Green Flags) to identify promising stocks
- Detailed evaluation templates for deep analysis
- Search strategies for finding stocks that pass all criteria
- Focus on emerging sectors with high growth potential

## Features

- **Comprehensive Screening Framework**: 13-point evaluation system (5 avoid + 8 consider criteria)
- **Multi-Cap Coverage**: Large-cap, Mid-cap, and Small-cap stock analysis
- **Emerging Sector Focus**: Renewable Energy, EV, Electronics Manufacturing, Defense, AI/ML, Fintech, Healthcare/Biotech, and more
- **Risk Management**: Clear pass/fail criteria with scoring methodology
- **Search Strategy**: Step-by-step guides for Screener.in, Moneycontrol, and Chartink

## Screening Criteria

### Avoid Criteria (Must PASS all 5)
1. Stocks that have already doubled without new catalyst
2. Declining profits
3. High debt
4. Poor liquidity
5. Social media promotion without business improvement

### Consider Criteria (Need 4+ of 8 to PASS)
1. Profit growth ≥ 40%
2. Sales growth ≥ 30%
3. Trading sideways 3-6 months
4. Breakout on 3X volume
5. Low debt
6. Promoter holdings ≥ 50%
7. Emerging sector
8. Management confidence & guidance

## Project Structure

```
AlphaHunterAI/
├── app/                                    # Python application source code
│   ├── ai/                                 # AI/ML analysis modules
│   ├── alerts/                             # Alerting system
│   ├── config/                             # Configuration management
│   ├── core/                               # Core domain components
│   ├── dashboard/                          # Web dashboard
│   ├── database/                           # Database connection managers
│   ├── financials/                         # Financial analysis modules
│   ├── ingestion/                          # Data ingestion pipelines
│   ├── management/                         # Management commands
│   ├── models/                             # Data models
│   ├── portfolio/                          # Portfolio management
│   ├── providers/                          # Data providers
│   ├── reports/                            # Report generation
│   ├── scoring/                            # Scoring engine
│   ├── sectors/                            # Sector analysis
│   ├── technical/                          # Technical analysis
│   ├── utils/                              # Utility modules
│   └── tests/                              # Unit tests
├── configs/                                # Configuration files
├── data/                                   # Data storage (bronze/silver/gold)
│   ├── bronze/                             # Raw ingested data
│   ├── silver/                             # Cleaned and transformed data
│   └── gold/                               # Aggregated and feature data
├── docs/                                   # Documentation
├── logs/                                   # Application logs
├── notebooks/                              # Jupyter notebooks
├── outputs/                                # Generated outputs
├── scripts/                                # Utility scripts
├── MASTER_Stock_Screening_Framework.txt    # Complete screening framework
├── Stock_Screening_Step_by_Step_Guide.txt  # Platform-specific screening guides
├── Stock_Candidates_From_Web_Search.txt    # Preliminary stock candidates
├── Small_Cap_Stocks_Heavily_Corrected_Ready_For_Recovery.txt  # Sample analysis
├── pyproject.toml                          # Python project configuration
├── requirements.txt                        # Production dependencies
├── Makefile                                # Development commands
├── Dockerfile                              # Production Docker image
├── docker-compose.yml                      # Docker orchestration
├── .github/workflows/ci.yml                # GitHub Actions CI
├── ruff.toml                               # Ruff linter configuration
├── .pre-commit-config.yaml                 # Pre-commit hooks
├── .env.example                            # Environment variables template
└── README.md
```

## Getting Started

### Python Application Setup

1. **Clone the repository** (Python 3.12 required)
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```
4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
5. **Run the application**
   ```bash
   python -m app
   # Or via CLI
   python -m app serve
   ```

### Stock Screening Framework

1. Review the `MASTER_Stock_Screening_Framework.txt` for complete criteria
2. Use `Stock_Screening_Step_by_Step_Guide.txt` to run screeners on:
   - Screener.in
   - Moneycontrol
   - Chartink
3. Export results and evaluate using the detailed evaluation template
4. Score stocks against the 13 criteria
5. Select stocks that pass 5/5 avoid criteria and 4+/8 consider criteria

## Usage

### API Server

Run the FastAPI application:
```bash
python -m app serve
```

Access the API at http://localhost:8000
- Health check: `GET /`
- Detailed health: `GET /health`
- Interactive docs: `GET /docs`

### Development Commands

```bash
make install-dev     # Install development dependencies
make lint            # Run Ruff linter
make format          # Format code with Ruff and Black
make test            # Run tests
make test-cov        # Run tests with coverage
make type-check      # Run MyPy type checker
make quality         # Run all quality checks
make docker-build    # Build Docker image
make docker-up       # Start Docker containers
```

### Quick Screening
Use the screening checklist in the MASTER framework for initial evaluation.

### Deep Analysis
Use the detailed evaluation template for comprehensive analysis of promising stocks.

### Search Strategy
Follow the step-by-step guide to find stocks that meet all criteria on screening platforms.

## Emerging Sectors

The framework prioritizes stocks in emerging sectors expected to grow 20%+ annually:
- Renewable Energy (Solar, Wind, Green Hydrogen)
- Electric Vehicles (EV components, batteries, charging)
- Electronics Manufacturing (EMS, semiconductors, PCB)
- Specialty Chemicals (agrochemicals, pharma intermediates)
- Defense & Aerospace
- Data Centers & Cloud Infrastructure
- AI & Machine Learning applications
- Fintech & Digital Payments
- Healthcare & Biotechnology
- Advanced Materials

## Data Sources

- Screener.in
- Moneycontrol
- Chartink
- Trendlyne
- BSE/NSE filings
- TradingView
- Corporate announcements

## Disclaimer

This framework is for educational and informational purposes only. It does not constitute financial advice or investment recommendations. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Note**: This framework is designed for Indian stock markets (NSE/BSE). Adjustments may be needed for other markets.
