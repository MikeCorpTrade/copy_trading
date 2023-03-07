import MetaTrader5 as mt5

from api.map_oanda_mt5 import login_mt5
from api.mt5_accounts import accounts


def get_current_price(symbol):
    prices = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
    return prices[0].close


def get_open_trade(symbol):
    position = mt5.positions_get(symbol=symbol)
    # Return the first position tuple (and the only one)
    return position[0]


def mt5_request(position, action=mt5.TRADE_ACTION_SLTP):
    request = {
        "action": action,
        "symbol": position.symbol,
        "type": position.type,
        "position": position.ticket,
        "sl": position.sl,
        "tp": position.tp,
        "magic": position.magic,
        "comment": position.comment,
    }

    return request


def update_stoploss_mt5(open_trade):

    symbol = open_trade.symbol

    # Get the current market price
    current_price = open_trade.price_current
    position_type = "buy" if open_trade.type == mt5.POSITION_TYPE_BUY else "sell"

    # Calculate the current risk reward ratio
    entry_price = float(open_trade.price_open)
    stop_loss = float(open_trade.sl)
    risk = entry_price - stop_loss
    reward = current_price - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward_ratio = None
    else:
        risk_reward_ratio = abs(reward / risk)

    # Calculate n
    n = int(risk_reward_ratio)

    # Check if the order is buy or sell (for the direction of the stoploss)
    if position_type == "buy":
        new_stop_loss = entry_price + (entry_price - stop_loss) * (n - 1)
    else:
        new_stop_loss = entry_price - (stop_loss - entry_price) * (n - 1)

    new_request = mt5_request(open_trade)
    # Update the stop loss if necessary
    if 1 <= risk_reward_ratio < 2 and stop_loss != entry_price:
        new_request["sl"] = entry_price
        mt5.order_send(new_request)
    elif 2 <= n <= risk_reward_ratio < n + 1 and stop_loss != new_stop_loss:
        new_request["sl"] = new_stop_loss
        mt5.order_send(new_request)


if __name__ == "__main__":

    login_mt5()

    for account in accounts:
        mt5.login(login=account.login, password=account.password, server=account.server)
        open_trades = mt5.positions_get()
        for open_trade in open_trades:
            update_stoploss_mt5(open_trade)
