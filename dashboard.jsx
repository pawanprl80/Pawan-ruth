// Dashboard.jsx
import { For, Show } from 'solid-js';

export default function DiamondUI(props) {
  return (
    <div class="min-h-screen bg-[#0a0c10] text-white font-sans p-6 overflow-hidden">
      {/* Background Glows for Glassmorphism Effect */}
      <div class="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full" />
      <div class="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full" />

      {/* TOP HEADER: Orderbook & Global P&L */}
      <header class="relative z-10 flex justify-between items-center mb-8 backdrop-blur-md bg-white/5 border border-white/10 p-6 rounded-3xl shadow-2xl">
        <div>
          <h1 class="text-2xl font-black tracking-tighter italic text-blue-400">DIAMOND_V3</h1>
          <p class="text-[10px] uppercase opacity-50">Heart Engine Status: <span class="text-green-400">Active</span></p>
        </div>
        
        <div class="flex gap-10 items-center">
          <div class="text-right">
            <p class="text-[10px] opacity-50 uppercase">Total Profit</p>
            <p class={`text-xl font-mono ${props.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              ₹{props.totalPnL}
            </p>
          </div>
          <button onClick={props.triggerPanic} class="bg-red-500/20 border border-red-500/50 text-red-500 px-6 py-3 rounded-2xl font-bold hover:bg-red-500 hover:text-white transition-all animate-pulse">
            🚨 PANIC CANCEL ALL
          </button>
        </div>
      </header>

      {/* THE HEATMAP GRID */}
      <div class="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <For each={props.stocks}>{(s) => (
          <div class={`relative backdrop-blur-xl bg-white/5 border rounded-3xl p-5 transition-all duration-500 
            ${s.is_diamond ? 'border-blue-500/50 shadow-[0_0_30px_rgba(59,130,246,0.2)]' : 'border-white/10'}`}>
            
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="font-bold text-lg">{s.symbol}</h3>
                <p class="text-[10px] opacity-40 italic">ATM: {s.strike} | EXP: {s.expiry}</p>
              </div>
              <p class="text-blue-400 font-mono font-bold">{s.ltp}</p>
            </div>

            {/* 10-DOT VISUAL VALIDATOR */}
            <div class="flex justify-between gap-1 mb-4 bg-black/20 p-2 rounded-xl border border-white/5">
              <For each={s.dots}>{(active) => (
                <div class={`h-2 w-full rounded-full transition-all duration-300 ${active ? 'bg-blue-500 shadow-[0_0_10px_#3b82f6]' : 'bg-white/10'}`} />
              )}</For>
            </div>

            {/* DEBUG VALUES & POSITION */}
            <div class="grid grid-cols-2 gap-2 text-[10px] font-mono opacity-70 mb-4">
               <div>RSI: {s.rsi}</div>
               <div>VOL: {s.vol_surge}x</div>
               <div>ST: {s.st_val}</div>
               <div>SLOPE: {s.slope}</div>
            </div>

            {/* POSITION STATUS */}
            <Show when={s.in_position} fallback={<div class="text-[10px] text-center opacity-30">SCANNING...</div>}>
              <div class="flex justify-between items-center bg-blue-500/10 border border-blue-500/20 p-3 rounded-2xl">
                <span class="text-[10px] font-bold text-blue-400">ACTIVE POSITION</span>
                <span class="font-mono text-green-400">+{s.pnl}%</span>
              </div>
            </Show>
          </div>
        )}</For>
      </div>
    </div>
  );
}
