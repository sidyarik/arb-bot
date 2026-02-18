from itertools import combinations
from core.models import MarketData


class Opportunity:
    def __init__(
        self,
        symbol: str,
        spot_exchange: str,
        futures_exchange: str,
        spot_price: float,
        futures_price: float,
        spread: float,
        funding_rate: float,
        borrow_available: bool,
    ):
        self.symbol = symbol
        self.spot_exchange = spot_exchange
        self.futures_exchange = futures_exchange
        self.spot_price = spot_price
        self.futures_price = futures_price
        self.spread = spread
        self.funding_rate = funding_rate
        self.borrow_available = borrow_available


def calculate_spread(spot_price: float, futures_price: float) -> float:
    if spot_price == 0:
        return 0
    return (spot_price - futures_price) / spot_price


def build_opportunities(markets: dict):
    opportunities = []

    for symbol, exchanges in markets.items():

        exchange_list = list(exchanges.items())

        # 🔹 1. Внутрибиржевой арбитраж (spot vs futures)
        for exchange_name, data in exchange_list:

            spread = calculate_spread(data.spot_bid, data.futures_ask)

            opportunities.append(
                Opportunity(
                    symbol=symbol,
                    spot_exchange=exchange_name,
                    futures_exchange=exchange_name,
                    spot_price=data.spot_bid,
                    futures_price=data.futures_ask,
                    spread=spread,
                    funding_rate=data.funding_rate,
                    borrow_available=data.borrow_available,
                )
            )

        # 🔹 2. Кросс-биржевой арбитраж
        for (ex1_name, data1), (ex2_name, data2) in combinations(exchange_list, 2):

            # SELL spot on ex1 / LONG futures on ex2
            spread_1 = calculate_spread(data1.spot_bid, data2.futures_ask)

            opportunities.append(
                Opportunity(
                    symbol=symbol,
                    spot_exchange=ex1_name,
                    futures_exchange=ex2_name,
                    spot_price=data1.spot_bid,
                    futures_price=data2.futures_ask,
                    spread=spread_1,
                    funding_rate=data2.funding_rate,
                    borrow_available=data1.borrow_available,
                )
            )

            # SELL spot on ex2 / LONG futures on ex1
            spread_2 = calculate_spread(data2.spot_bid, data1.futures_ask)

            opportunities.append(
                Opportunity(
                    symbol=symbol,
                    spot_exchange=ex2_name,
                    futures_exchange=ex1_name,
                    spot_price=data2.spot_bid,
                    futures_price=data1.futures_ask,
                    spread=spread_2,
                    funding_rate=data1.funding_rate,
                    borrow_available=data2.borrow_available,
                )
            )

    return opportunities