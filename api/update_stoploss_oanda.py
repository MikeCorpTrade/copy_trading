from api.crud_api import OandaAPI, OandaTrade
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT, BASE_URL, API_KEY


def update_stoploss(trade: OandaTrade):
    # Get the current market price
    current_price = OandaAPI().get_current_price(trade.instrument)

    units = trade.units

    # Get the trade details
    trade_id = trade.id
    stop_loss_order_id = trade.stop_loss_id

    # Calculate the current risk reward ratio
    entry_price = trade.open_price
    stop_loss = trade.stop_loss
    risk = entry_price - stop_loss
    reward = current_price - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward_ratio = None
    else:
        risk_reward_ratio = abs(reward / risk)

    # Calculate n
    n = int(risk_reward_ratio)

    # Check if the order is buy or sell (for the direction of the stoploss)
    if units > 0:
        new_stop_loss = entry_price + (entry_price - stop_loss) * (n - 1)
    else:
        new_stop_loss = entry_price - (stop_loss - entry_price) * (n - 1)

    # Update the stop loss if necessary
    if 1 <= risk_reward_ratio < 2 and stop_loss != entry_price:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stop_loss_order_id, entry_price)
    elif 2 <= n <= risk_reward_ratio < n + 1 and stop_loss != new_stop_loss:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stop_loss_order_id, new_stop_loss)


account_ids = [SOURCE_ACCOUNT, DESTINATION_ACCOUNT]

if __name__ == "__main__":
    print("Update Stop_loss Oanda Algorithm started...")

    while True:

        try:
            for account_id in account_ids:
                # Check for open trades in the source account
                trades = OandaAPI(account_id=account_id).get_open_trades()

                for trade in trades:
                    oanda_trade = OandaTrade(trade)
                    # Update the stoploss of a trade
                    update_stoploss(oanda_trade)

        except Exception as error:
            print("An error occurred:", error)
