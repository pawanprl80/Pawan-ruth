// src/App.jsx
import RuthPro from './components/RuthPro';

function App() {
  // These are the props (data) that the Ruth UI is looking for
  const [stocks, setStocks] = createSignal([]); 
  const [totalPnL, setTotalPnL] = createSignal(0);

  return (
    <RuthPro 
      stocks={stocks()} 
      totalPnL={totalPnL()} 
      usedSlots={stocks().filter(s => s.in_position).length}
      globalPanic={() => console.log("TERMINATING ALL")}
    />
  );
}
