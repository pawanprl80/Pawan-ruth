// Dashboard.jsx
import { createMemo, For } from "solid-js";

export default function VisualValidator(props) {
  // Heatmap Sort: Moves Validated Diamonds to top, then sorts by RSI
  const sorted = createMemo(() => 
    [...props.stocks].sort((a, b) => b.is_diamond - a.is_diamond || b.rsi - a.rsi)
  );

  return (
    <div class="p-6 bg-[#050505] text-white font-mono">
      <div class="grid grid-cols-4 gap-4">
        <For each={sorted()}>{(s) => (
          <div class={`p-4 rounded-xl border transition-all duration-500 ${s.is_diamond ? 'bg-blue-600/20 border-blue-500 shadow-blue' : 'bg-white/5 border-white/5'}`}>
            <div class="flex justify-between items-center">
              <span class="font-black text-lg">{s.symbol}</span>
              <span class="text-blue-400 font-bold">{s.ltp}</span>
            </div>

            {/* Indicator Value Advance View */}
            <div class="mt-4 grid grid-cols-2 gap-2 text-[10px] opacity-60">
              <span>RSI: {s.rsi.toFixed(2)}</span>
              <span>MID: {s.mid.toFixed(1)}</span>
            </div>

            {/* Signal Validator Debugger */}
            <div class="mt-3 py-1 px-2 bg-black/50 rounded border border-white/10">
              <span class={`text-[9px] font-black ${s.is_diamond ? 'text-blue-400' : 'text-gray-500'}`}>
                {s.is_diamond ? "💎 SIGNAL_VALIDATED" : `SCAN: ${s.debug}`}
              </span>
            </div>

            {/* Repainting/Persistence Progress */}
            <div class="h-1 w-full bg-white/5 mt-3 rounded-full overflow-hidden">
               <div class={`h-full transition-all duration-700 ${s.is_diamond ? 'bg-blue-500 w-full' : 'bg-gray-700 w-1/3'}`}></div>
            </div>
          </div>
        )}</For>
      </div>
    </div>
  );
}
