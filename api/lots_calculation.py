from typing import List
from api.crud_api import OandaTrade


def is_currency_pair(instrument: str, list_currencies: List[str]) -> bool:
    if instrument in list_currencies:
        return True
    else:
        return False


def convert_units_to_volume(units: float) -> float:
    factor = 100000
    return round(units / factor, 2)


def convert_volume_to_units(volume: float) -> float:
    return volume * 100000


class LotsCalculation:
    def __init__(self, trade: OandaTrade, is_currency: bool, source_account_balance: float) -> None:
        self.open_price = trade.open_price
        self.stop_loss = trade.stop_loss
        self.instrument = trade.instrument
        self.is_currency = is_currency
        self.units = trade.units
        self.mini_lots = 10000
        self.source_account_balance = source_account_balance
        self.pips = self.calculate_pips()
        self.pip_value = self.get_pip_value()
        self.risk = self.calculate_risk_per_trade()

    def get_forex_pip_value(self) -> float:
        return self.units / self.mini_lots

    def get_pip_value(self) -> float:
        if self.is_currency:
            pip_value = self.get_forex_pip_value()
            return pip_value
        else:
            return self.units

    def calculate_forex_pips(self, decimal_places=4) -> float:
        """
        Calculates the number of pips between the stop loss and open price for any currency pair.

        Parameters:
        open_price (float): The open price of the trade.
        stop_loss (float): The stop loss price of the trade.
        decimal_places (int): The number of decimal places to round the pip value to. Defaults to 4.

        Returns:
        float: The number of pips between the stop loss and open price.
        """
        pip_multiplier = 10 ** decimal_places

        # Calculate the pip value based on the currency pair's decimal places
        if "JPY" in self.instrument:  # Japanese Yen currency pairs have 2 decimal places
            pip_reference = 0.01
        elif "XAU" in self.instrument:  # Gold (XAU) has 2 decimal places
            pip_reference = 0.01
        elif "XAG" in self.instrument:  # Silver (XAG) has 3 decimal places
            pip_reference = 0.001
        else:  # All other currency pairs have 4 decimal places
            pip_reference = 0.0001

        # Calculate the number of pips based on the pip value and decimal places
        pips = round(abs(self.stop_loss - self.open_price) / pip_reference * pip_multiplier) / pip_multiplier

        # Return the number of pips rounded to the specified decimal places
        return round(pips, decimal_places)

    def calculate_indices_pips(self, decimal_places: int = 2) -> float:
        """
        Calculates the number of pips between the stop loss and open price for indices like SP500, NASDAQ100, etc.

        Parameters:
        open_price (float): The open price of the trade.
        stop_loss (float): The stop loss price of the trade.
        decimal_places (int): The number of decimal places to round the pip value to. Defaults to 2.
        pip_value (float): The pip value of the instrument. Defaults to 1.

        Returns:
        float: The number of pips between the stop loss and open price.
        """

        pip_multiplier = 10 ** decimal_places

        # Calculate the number of pips based on the pip value and decimal places
        pips = round(abs(self.stop_loss - self.open_price))

        # Return the number of pips rounded to the specified decimal places
        return round(pips, decimal_places)

    def calculate_pips(self) -> float:
        if self.is_currency:
            decimal_place = 4
            pips = self.calculate_forex_pips(decimal_place)
            return pips
        else:
            decimal_place = 2
            pips = self.calculate_indices_pips(decimal_place)
            return pips

    def calculate_risk_per_trade(self) -> float:

        pip_value = self.pip_value
        pips = self.pips

        percentage_risk = round(((pip_value * pips) / self.source_account_balance), 4)

        return percentage_risk

    def calculate_units_per_trade(self, target_account_balance: float) -> float:

        pips_value = (self.risk * target_account_balance) / self.pips

        if self.is_currency:
            return pips_value * self.mini_lots
        else:
            return pips_value
