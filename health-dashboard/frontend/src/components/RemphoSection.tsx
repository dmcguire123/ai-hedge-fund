import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useData } from "../hooks/useData";
import {
  getBodyFatHistory,
  getLatestMetrics,
  getWeightHistory,
} from "../services/api";
import { ErrorMsg, LoadingSpinner } from "./LoadingSpinner";
import { SectionHeader } from "./SectionHeader";
import { StatCard } from "./StatCard";

const COLOR = "#7c3aed";

function fmtDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-GB", { month: "short", day: "numeric" });
}

export function RemphoSection({ connected }: { connected: boolean }) {
  const latest = useData(getLatestMetrics);
  const weight = useData(() => getWeightHistory(90));
  const bodyFat = useData(() => getBodyFatHistory(90));

  return (
    <section>
      <SectionHeader logo="⚖️" name="Rempho / Google Fit" color={COLOR} connected={connected} authPath="/auth/google" />

      {!connected && (
        <div className="bg-surface rounded-xl p-6 border border-border text-center text-muted">
          Connect Google Fit above to pull in your Rempho body composition data.
        </div>
      )}

      {connected && (
        <>
          {/* Latest metrics */}
          {latest.status === "loading" && <LoadingSpinner color={COLOR} />}
          {latest.status === "error" && <ErrorMsg msg={latest.error!} />}
          {latest.data && (
            <div className="grid grid-cols-2 gap-3 mb-6">
              <StatCard
                label="Weight"
                value={latest.data.weight_kg != null ? latest.data.weight_kg.toFixed(1) : null}
                unit="kg"
                icon="⚖️"
                color={COLOR}
                sub={latest.data.weight_date ? `Last: ${fmtDate(latest.data.weight_date)}` : undefined}
              />
              <StatCard
                label="Body Fat"
                value={latest.data.body_fat_pct != null ? latest.data.body_fat_pct.toFixed(1) : null}
                unit="%"
                icon="📊"
                color={COLOR}
                sub={latest.data.body_fat_date ? `Last: ${fmtDate(latest.data.body_fat_date)}` : undefined}
              />
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-6">
            {/* Weight trend */}
            <div className="bg-surface rounded-xl p-4 border border-border">
              <h3 className="text-sm font-medium text-muted mb-3">Weight – last 90 days</h3>
              {weight.status === "loading" && <LoadingSpinner color={COLOR} />}
              {weight.status === "error" && <ErrorMsg msg={weight.error!} />}
              {weight.data && weight.data.length === 0 && (
                <p className="text-muted text-sm py-4">No weight data found in Google Fit.</p>
              )}
              {weight.data && weight.data.length > 0 && (
                <ResponsiveContainer width="100%" height={180}>
                  <AreaChart data={weight.data.map(d => ({ date: fmtDate(d.date), kg: d.weight_kg }))}>
                    <defs>
                      <linearGradient id="weightGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={COLOR} stopOpacity={0.3} />
                        <stop offset="95%" stopColor={COLOR} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} interval="preserveStartEnd" />
                    <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} unit=" kg" />
                    <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                    <Area type="monotone" dataKey="kg" stroke={COLOR} fill="url(#weightGrad)" strokeWidth={2} dot={false} />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>

            {/* Body fat trend */}
            <div className="bg-surface rounded-xl p-4 border border-border">
              <h3 className="text-sm font-medium text-muted mb-3">Body Fat % – last 90 days</h3>
              {bodyFat.status === "loading" && <LoadingSpinner color={COLOR} />}
              {bodyFat.status === "error" && <ErrorMsg msg={bodyFat.error!} />}
              {bodyFat.data && bodyFat.data.length === 0 && (
                <p className="text-muted text-sm py-4">No body fat data found. Make sure Rempho is syncing to Google Fit.</p>
              )}
              {bodyFat.data && bodyFat.data.length > 0 && (
                <ResponsiveContainer width="100%" height={180}>
                  <LineChart data={bodyFat.data.map(d => ({ date: fmtDate(d.date), pct: d.body_fat_pct }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} interval="preserveStartEnd" />
                    <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} unit="%" />
                    <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                    <Line type="monotone" dataKey="pct" stroke={COLOR} strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
