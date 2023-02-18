import requests
import json

# Replace with your own values
ACCOUNT_ID = "123456"
ORDER_ID = "123456"
API_KEY = "your_api_key"


def risk_reward_ratio(api_key, account_id, order_id):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(
        f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/orders/{order_id}",
        headers=headers
    )
    response_data = json.loads(response.text)
    stop_loss = float(response_data["order"]["stopLossOnFill"]["price"])
    take_profit = float(response_data["order"]["takeProfitOnFill"]["price"])
    entry_price = float(response_data["order"]["price"])
    units = float(response_data["order"]["units"])
    if units < 0:
        pips = (entry_price - stop_loss) / 0.0001
        risk = abs(units) * pips * 10
        reward = abs(units) * (take_profit - entry_price) / 0.0001 * 10
    else:
        pips = (take_profit - entry_price) / 0.0001
        risk = abs(units) * (entry_price - stop_loss) / 0.0001 * 10
        reward = abs(units) * pips * 10
    ratio = reward / risk
    return ratio
