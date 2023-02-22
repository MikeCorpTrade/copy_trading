from crud_api import OandaAPI


def risk_reward_ratio(instrument):
    trade = OandaAPI().get_instrument_trade(instrument=instrument)

    # Calculate the current risk reward ratio
    entry_price = float(trade["price"])
    stop_loss = float(trade["stopLossOrder"]["price"])
    take_profit = float(trade["takeProfitOrder"]["price"])
    risk = entry_price - stop_loss
    reward = take_profit - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward = None
    else:
        risk_reward = abs(reward / risk)

    return risk_reward


if __name__ == "__main__":
    ratio = risk_reward_ratio("EUR_USD")
    print(ratio)
