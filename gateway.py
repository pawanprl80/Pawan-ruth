# gateway.py

def manage_positions():
    active_trades = redis.keys("slot:*")
    
    for slot in active_trades:
        symbol = slot.split(":")[1]
        data = mojo_engine.get_latest(symbol)
        
        # WHICHEVER IS EARLIER Rule
        # The logic checks ST, Mid-band, and RSI. First one to fail kills the trade.
        if data['status'] == "EXIT_IMMEDIATELY":
            order_id = angel.placeOrder({
                "variety": "NORMAL", "tradingsymbol": symbol,
                "transactiontype": "SELL", "exchange": "NFO",
                "ordertype": "MARKET", "quantity": redis.get(slot)['qty'],
                "producttype": "INTRADAY"
            })
            redis.delete(slot) # Clear the slot for a new Diamond signal
            print(f"🚨 EXIT TRIGGERED: {symbol} - Reason: {data['exit_reason']}")
