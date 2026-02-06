import json
from datetime import datetime

def log_diamond_trade(symbol, entry_data, exit_data, pnl):
    audit_report = {
        "trade_id": f"DT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "symbol": symbol,
        "execution_summary": {
            "entry_time": datetime.now().isoformat(),
            "leverage": "10x",
            "capital_slot": "20,000 INR"
        },
        # --- THE 10-CONDITION VERIFICATION ---
        "entry_validator_snapshot": {
            "st_green": entry_data['st_dir'] == 1,
            "macd_green": entry_data['macd'] > 0,
            "midband_support": entry_data['ltp'] > entry_data['mid'],
            "rsi_breakout": entry_data['rsi'] > 70,
            "upper_expansion": entry_data['ub_rising'],
            "golden_cross_locked": entry_data['st_line'] > entry_data['mid'],
            "squeeze_confirmed": entry_data['bb_width'] < 0.05,
            "slope_angle": entry_data['slope'],
            "shape_parabolic": entry_data['is_parabolic'],
            "vertical_shift": entry_data['is_vertical']
        },
        # --- THE EXIT ANALYSIS ---
        "exit_validator_snapshot": {
            "exit_time": datetime.now().isoformat(),
            "trigger_reason": exit_data['reason'], # Whichever was earlier
            "final_pnl": f"{pnl}%"
        }
    }

    with open(f"audit_{symbol}.json", "w") as f:
        json.dump(audit_report, f, indent=4)
    print(f"✅ Audit Log Generated for {symbol}")
