# exit_validator.mojo

fn validate_exit_conditions(cur: PythonObject, entry_price: Float64) -> String:
    # --- RULE: WHICHEVER IS EARLIER ---
    
    # 1. Structural Break: Supertrend Flips Red
    if cur.st_dir == -1: 
        return "EXIT: ST_FLIP"
        
    # 2. Mean Break: Price falls below Midband
    if cur.ltp < cur.mid: 
        return "EXIT: MIDBAND_BREAK"
        
    # 3. Verticality Loss: Slope turns negative or flat
    if cur.slope < 0.1: 
        return "EXIT: MOMENTUM_LOSS"
        
    # 4. Shape Break: Current Close < Previous Close (Lower High/Lower Low)
    if cur.ltp < cur.prev_close:
        return "EXIT: SHAPE_DESTRUCTION"
        
    # 5. RSI Exhaustion: RSI drops back below 65 from 70
    if cur.rsi < 65:
        return "EXIT: RSI_EXHAUSTION"

    return "HOLD"
