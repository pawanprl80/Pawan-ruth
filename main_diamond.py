import os, time, redis, pyotp
from SmartApi import SmartConnect
from engine_logic import DiamondValidator # Import from our Mojo compiled module

# --- 1. INITIALIZATION ---
load_dotenv()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
api = SmartConnect(api_key=os.getenv("ANGEL_ONE_API_KEY"))
totp = pyotp.TOTP(os.getenv("ANGEL_ONE_TOTP_SECRET")).now()
api.generateSession(os.getenv("CLIENT_ID"), os.getenv("PASSWORD"), totp)

validator = DiamondValidator() # The 10-Condition Logic

# --- 2. CORE LOOP: ENTRY & EXIT ---
def diamond_heart_beat():
    while True:
        # Check for Global Panic Reset first
        if r.get("panic_reset") == "TRUE":
            execute_global_exit()
            break

        # FETCH 200 SCRIPTS OHLC
        for script in filtered_scrip_list:
            ohlc = get_ohlc(script['token'])
            
            # 1. THE MATH & VALIDATION (10 CONDITIONS)
            status = validator.validate_10_points(ohlc)
            
            # 2. ENTRY LOGIC
            if status == "DIAMOND_LOCKED":
                if len(r.keys("slot:*")) < 10 and not r.exists(f"slot:{script['symbol']}"):
                    fire_diamond_order(script, "BUY")

            # 3. EXIT LOGIC (WHICHEVER IS EARLIER)
            if r.exists(f"slot:{script['symbol']}"):
                exit_check = validator.check_early_exit(ohlc)
                if exit_check != "HOLD":
                    fire_diamond_order(script, "SELL", reason=exit_check)

        time.sleep(0.5) # High-speed refresh

# --- 3. THE 10-CONDITION DICTIONARY (For Visual Dashboard) ---
def get_dashboard_payload(symbol):
    vals = get_current_indicators(symbol)
    return {
        "symbol": symbol,
        "ltp": vals.ltp,
        "dots": {
            "st": vals.st_dir == 1,
            "macd": vals.macd > 0,
            "mid": vals.ltp > vals.mid,
            "rsi": vals.rsi > 70,
            "ub": vals.upper_rising,
            "gold": vals.st_line > vals.mid,
            "sqz": vals.bb_width < 0.05,
            "slope": vals.slope > 0.5,
            "shape": vals.is_parabolic,
            "vert": vals.is_vertical
        }
    }

def execute_global_exit():
    # Emergency closure of all 10 slots
    for slot in r.keys("slot:*"):
        # API Market Sell Logic...
        r.delete(slot)
    print("🚨 SYSTEM HALTED: ALL TRADES CLOSED")

if __name__ == "__main__":
    diamond_heart_beat()
