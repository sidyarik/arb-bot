from dataclasses import dataclass


@dataclass
class MarketData:
    exchange: str
    symbol: str

    spot_bid: float
    spot_ask: float

    futures_bid: float
    futures_ask: float

    funding_rate: float
    funding_interval_hours: int = 8

    borrow_rate: float | None = None
    borrow_available: bool = False

    deposit_enabled: bool = True
    withdraw_enabled: bool = True