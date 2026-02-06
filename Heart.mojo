# engine.mojo
from python import Python

struct DiamondEngine:
    var rsi_period: Int
    var st_len: Int
    var st_mult: Float64

    fn __init__(out self):
        self.rsi_period = 14
        self.st_len = 10
        self.st_mult = 3.0

    fn validate_core(self, ohlc: PythonObject) raises -> PythonObject:
        """
        NON-STOP CORE:
        1. RMA Math (Indicator Value)
        2. Golden Cross (Signal Validator)
        3. 3-Tick Persistence (Anti-Repaint)
        """
        let ta = Python.import_module("pandas_ta")
        
        # --- LAYER 1: INDICATOR VALUES ---
        let rsi = ta.rsi(ohlc.close, length=self.rsi_period)
        let st = ta.supertrend(ohlc.high, ohlc.low, ohlc.close, self.st_len, self.st_mult)
        let bb = ta.bbands(ohlc.close, length=20, std=2)
        
        # --- LAYER 2: SIGNAL VALIDATOR LOGIC ---
        let cur = -1
        let pre = -2
        
        let st_line = st['SUPERT_10_3.0']
        let mid_band = bb['BBM_20_2.0']
        
        # Condition 1: Supertrend Green
        let trend_up = st['SUPERTd_10_3.0'][cur] == 1
        # Condition 2: RSI Breakout
        let rsi_70 = rsi[cur] > 70
        # Condition 3: Price Support
        let above_mid = ohlc.close[cur] > mid_band[cur]
        # Condition 4: THE GOLDEN CROSS (ST crosses Mid-band from below)
        let golden_cross = (st_line[pre] <= mid_band[pre]) and (st_line[cur] > mid_band[cur])
        
        # --- LAYER 3: ANTI-REPAINT (PERSISTENCE) ---
        var stable_ticks = 0
        for i in range(-3, 0):
            if ohlc.close[i] > st_line[i]: stable_ticks += 1
        let is_persistent = stable_ticks == 3

        # Final Decision
        let is_diamond = trend_up and rsi_70 and above_mid and golden_cross and is_persistent

        return {
            "ltp": ohlc.close[cur],
            "rsi": rsi[cur],
            "st_val": st_line[cur],
            "mid": mid_band[cur],
            "is_diamond": is_diamond,
            "debug": self.get_debug(trend_up, rsi_70, above_mid, golden_cross, is_persistent)
        }

    fn get_debug(self, c1: Bool, c2: Bool, c3: Bool, c4: Bool, c5: Bool) -> String:
        if not c1: return "WAITING_TREND_UP"
        if not c2: return "WAITING_RSI_70"
        if not c3: return "WAITING_MID_BAND"
        if not c4: return "WAITING_GOLDEN_CROSS"
        if not c5: return "WAITING_PERSISTENCE"
        return "DIAMOND_LOCKED"
