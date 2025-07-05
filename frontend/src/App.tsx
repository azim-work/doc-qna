import Sidebar from "./components/Sidebar";
import QNASection from "./components/QNASection";

function App() {
  return (
    <div className="min-h-screen flex bg-gray-100 text-gray-800">
      {/* Left column */}
      <Sidebar />

      {/* Right column */}
      <QNASection />
    </div>
  );
}

export default App;
