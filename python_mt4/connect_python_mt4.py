from pymt4 import MT4

# Connect to the MT4 terminal
mt4 = MT4(host='127.0.0.1', port=7788, login=123456, password='password')

# Get the list of open trades
open_trades = mt4.trades_get()

# Print the list of open trades
for trade in open_trades:
    print(trade)

# Disconnect from the MT4 terminal
mt4.disconnect()
