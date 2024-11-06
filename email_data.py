"""
Module for defining data models related to email content and trading details.

This module includes the `Instrument` class, which represents the details of ticker trading.
"""

from typing import List
from pydantic import BaseModel, Field


class Instrument(BaseModel):
    """Datamodel for ticker trading details."""

    direction: str = Field(description="ticker trading - Buy, Sell, Hold etc")
    ticker: str = Field(
        description="Stock Ticker. 1-4 character code. Example: AAPL, TSLS, MSFT, VZ"
    )
    company_name: str = Field(
        description="Company name corresponding to ticker"
    )
    shares_traded: float = Field(description="Number of shares traded")
    percent_of_etf: float = Field(description="Percentage of ETF")


class Etf(BaseModel):
    """ETF trading data model"""

    etf_ticker: str = Field(
        description="ETF Ticker code. Example: ARKK, FSPTX"
    )
    trade_date: str = Field(description="Date of trading")
    stocks: List[Instrument] = Field(
        description="List of instruments or shares traded under this etf"
    )


class EmailData(BaseModel):
    """Data model for email extracted information."""

    etfs: List[Etf] = Field(
        description="List of ETFs described in email having list of shares traded under it"
    )
    trade_notification_date: str = Field(
        description="Date of trade notification"
    )
    sender_email_id: str = Field(description="Email Id of the email sender.")
    email_date_time: str = Field(description="Date and time of email")
    