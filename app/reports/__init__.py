"""Reports module for AlphaHunter Research Reports."""

from app.reports.generator import WeeklyReportGenerator
from app.reports.weekly_report import (
    HiddenGem,
    InstitutionalActivity,
    ManagementUpgrade,
    NewOpportunity,
    PortfolioChange,
    RiskAlert,
    SectorTrend,
    StockRanking,
    StockToAvoid,
    TechnicalBreakout,
    WeeklyReport,
)

__all__ = [
    "WeeklyReportGenerator",
    "WeeklyReport",
    "StockRanking",
    "HiddenGem",
    "SectorTrend",
    "ManagementUpgrade",
    "InstitutionalActivity",
    "TechnicalBreakout",
    "StockToAvoid",
    "RiskAlert",
    "PortfolioChange",
    "NewOpportunity",
]
