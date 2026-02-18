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

    borrow_rate: float | None
    borrow_available: bool