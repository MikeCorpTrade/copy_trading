import requests
import json

# Oanda trade order details
oanda_trade_order = {
    "order": {
        "units": 1000,
        "instrument": "EUR_USD",
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT",
        "stopLossOnFill": {
            "timeInForce": "GTC",
            "price": 1.10
        },
        "takeProfitOnFill": {
            "price": 1.20
        }
    }
}

# Map the Oanda trade order to MT5 format
mt5_trade_order = {
    "volume": oanda_trade_order["order"]["units"],
    "symbol": oanda_trade_order["order"]["instrument"],
    "type": "OP_BUY" if oanda_trade_order["order"]["units"] > 0 else "OP_SELL",
    "price": 0,
    "sl": oanda_trade_order["order"]["stopLossOnFill"]["price"],
    "tp": oanda_trade_order["order"]["takeProfitOnFill"]["price"],
    "comment": "",
    "magic": 123456,
    "deviation": 200
}

# Place the trade order using MT5 API
mt5_api_url = "https://api.mt5.com/v1/trade/order/place"
mt5_api_key = "your_mt5_api_key"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + mt5_api_key
}
response = requests.post(mt5_api_url, headers=headers,
                         data=json.dumps(mt5_trade_order))

# Check the response status and retrieve the trade details
if response.status_code == 200:
    trade_details = response.json()
    print("Trade placed successfully: ", trade_details)
else:
    print("Failed to place trade: ", response.text)
