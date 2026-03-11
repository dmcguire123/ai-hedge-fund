import { useEffect, useState } from "react";
import { GarminSection } from "./components/GarminSection";
import { RemphoSection } from "./components/RemphoSection";
import { StravaSection } from "./components/StravaSection";
import { getGoogleStatus, getStravaStatus } from "./services/api";

function RefreshIcon({ spinning }: { spinning: boolean }) {
  return (
    <svg
      className={`w-4 h-4 ${spinning ? "animate-spin" : ""}`}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path d="M23 4v6h-6M1 20v-6h6" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function App() {
  const [stravaConnected, setStravaConnected] = useState<boolean>(false);
  const [googleConnected, setGoogleConnected] = useState<boolean>(false);
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    Promise.all([
      getStravaStatus().then((s) => setStravaConnected(s.connected)).catch(() => {}),
      getGoogleStatus().then((s) => setGoogleConnected(s.connected)).catch(() => {}),
    ]).then(() => setLastSync(new Date()));
  }, [refreshKey]);

  const handleRefresh = () => {
    setRefreshing(true);
    setRefreshKey((k) => k + 1);
    setTimeout(() => setRefreshing(false), 1500);
  };

  return (
    <div className="min-h-screen bg-bg text-slate-200">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-bg/90 backdrop-blur border-b border-border px-4 py-3 flex items-center gap-3">
        <span className="text-xl">❤️</span>
        <h1 className="text-base font-bold tracking-tight">Health Dashboard</h1>
        <div className="flex-1" />
        {lastSync && (
          <span className="text-xs text-muted hidden sm:block">
            Synced {lastSync.toLocaleTimeString()}
          </span>
        )}
        <button
          onClick={handleRefresh}
          className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-surface border border-border hover:border-slate-400 transition-colors"
        >
          <RefreshIcon spinning={refreshing} />
          Refresh
        </button>
      </header>

      {/* Main content */}
      <main className="max-w-5xl mx-auto px-4 py-6 space-y-10" key={refreshKey}>
        <GarminSection />
        <div className="border-t border-border" />
        <StravaSection connected={stravaConnected} />
        <div className="border-t border-border" />
        <RemphoSection connected={googleConnected} />
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-muted py-6 border-t border-border mt-8">
        Local Health Dashboard · Data stays on your machine
      </footer>
    </div>
  );
}
