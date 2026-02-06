# gateway_panic.py
import redis
from SmartApi import SmartConnect

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def global_panic_reset():
    """
    WHICHEVER IS EARLIER: Manual Panic Override
    Kills all 10 slots instantly and locks the bot.
    """
    # 1. Set Global Kill-Switch (Stops Engine from re-entering)
    r.setex("trading_halt", 3600, "TRUE") 
    
    # 2. Identify all active Diamond Slots
    active_slots = r.keys("slot:*")
    
    for slot in active_slots:
        trade_data = r.hgetall(slot)
        
        # 3. Fire Market Sell Orders
        try:
            order_id = api.placeOrder({
                "variety": "NORMAL",
                "tradingsymbol": trade_data['symbol'],
                "symboltoken": trade_data['token'],
                "transactiontype": "SELL",
                "exchange": "NFO",
                "ordertype": "MARKET",
                "quantity": trade_data['qty'],
                "producttype": "INTRADAY"
            })
            print(f"🚨 PANIC EXIT: {trade_data['symbol']} executed.")
        except Exception as e:
            print(f"⚠️ Manual intervention required for {trade_data['symbol']}: {e}")
            
        # 4. Clear Redis Slot
        r.delete(slot)

    return {"status": "ALL_SLOTS_CLEARED", "count": len(active_slots)}
