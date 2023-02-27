import MetaTrader5 as mt5


def get_current_price(instrument):
    if not mt5.initialize():
        print("initialize() failed")
        return None

    prices = mt5.copy_rates_from_pos(instrument, mt5.TIMEFRAME_M1, 0, 1)
    mt5.shutdown()

    return prices[0].close


def update_order(*kwargs):
    pass


def get_open_trade(instrument):
    position = mt5.positions_get(symbol=instrument)
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


def update_stoploss_mt5(instrument):
    # Get the current market price
    current_price = get_current_price(instrument)

    # Get the order details
    position = get_open_trade(instrument)

    position_type = "buy" if position.type == mt5.POSITION_TYPE_BUY else "sell"

    # Calculate the current risk reward ratio
    entry_price = float(position.price_open)
    stop_loss = float(position.sl)
    take_profit = float(position.tp)
    risk = entry_price - stop_loss
    reward = take_profit - entry_price
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

    new_request = mt5_request(position)
    # Update the stop loss if necessary
    if 1 <= risk_reward_ratio < 2 and stop_loss != entry_price:
        new_request["sl"] = entry_price
        mt5.order_send(new_request)
    elif 2 <= n <= risk_reward_ratio < n + 1 and stop_loss != new_stop_loss:
        new_request["sl"] = new_stop_loss
        mt5.order_send(new_request)
