import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useData } from "../hooks/useData";
import {
  getStravaActivities,
  getStravaStats,
  getStravaWeekly,
} from "../services/api";
import { ErrorMsg, LoadingSpinner } from "./LoadingSpinner";
import { SectionHeader } from "./SectionHeader";
import { StatCard } from "./StatCard";

const COLOR = "#fc4c02";

function fmtKm(m: number) { return (m / 1000).toFixed(1); }
function fmtPace(mps: number) {
  if (!mps) return "—";
  const minPerKm = 1000 / 60 / mps;
  const min = Math.floor(minPerKm);
  const sec = Math.round((minPerKm - min) * 60);
  return `${min}:${sec.toString().padStart(2, "0")} /km`;
}
function fmtDuration(s: number) {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}
function sportEmoji(type: string) {
  const t = type.toLowerCase();
  if (t.includes("run")) return "🏃";
  if (t.includes("ride") || t.includes("cycling")) return "🚴";
  if (t.includes("swim")) return "🏊";
  if (t.includes("hike") || t.includes("walk")) return "🥾";
  return "🏋️";
}

export function StravaSection({ connected }: { connected: boolean }) {
  const stats = useData(getStravaStats);
  const activities = useData(() => getStravaActivities(15));
  const weekly = useData(() => getStravaWeekly(10));

  return (
    <section>
      <SectionHeader logo="🟠" name="Strava" color={COLOR} connected={connected} authPath="/auth/strava" />

      {!connected && (
        <div className="bg-surface rounded-xl p-6 border border-border text-center text-muted">
          Connect Strava above to see your activities.
        </div>
      )}

      {connected && (
        <>
          {/* YTD stats */}
          {stats.status === "loading" && <LoadingSpinner color={COLOR} />}
          {stats.status === "error" && <ErrorMsg msg={stats.error!} />}
          {stats.data && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
              <StatCard label="YTD Run" value={fmtKm(stats.data.ytd_run_distance)} unit="km" icon="🏃" color={COLOR} />
              <StatCard label="YTD Ride" value={fmtKm(stats.data.ytd_ride_distance)} unit="km" icon="🚴" color={COLOR} />
              <StatCard label="YTD Swim" value={fmtKm(stats.data.ytd_swim_distance)} unit="km" icon="🏊" color={COLOR} />
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Weekly distance chart */}
            <div className="bg-surface rounded-xl p-4 border border-border">
              <h3 className="text-sm font-medium text-muted mb-3">Weekly Distance – last 10 weeks</h3>
              {weekly.status === "loading" && <LoadingSpinner color={COLOR} />}
              {weekly.status === "error" && <ErrorMsg msg={weekly.error!} />}
              {weekly.data && (
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={weekly.data.map(w => ({
                    week: w.week.slice(5),
                    km: +(w.distance_meters / 1000).toFixed(1),
                    count: w.count,
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="week" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} />
                    <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} unit=" km" />
                    <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                    <Bar dataKey="km" fill={COLOR} radius={[3, 3, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>

            {/* Recent activities list */}
            <div className="bg-surface rounded-xl p-4 border border-border">
              <h3 className="text-sm font-medium text-muted mb-3">Recent Activities</h3>
              {activities.status === "loading" && <LoadingSpinner color={COLOR} />}
              {activities.status === "error" && <ErrorMsg msg={activities.error!} />}
              {activities.data && (
                <div className="space-y-2 max-h-[200px] overflow-y-auto pr-1">
                  {activities.data.slice(0, 8).map((act) => (
                    <div key={act.id} className="flex items-center gap-3 py-1.5 border-b border-border last:border-0">
                      <span className="text-lg">{sportEmoji(act.type)}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{act.name}</p>
                        <p className="text-xs text-muted">
                          {fmtKm(act.distance_meters)} km · {fmtDuration(act.duration_seconds)}
                          {act.avg_speed_mps ? ` · ${fmtPace(act.avg_speed_mps)}` : ""}
                        </p>
                      </div>
                      <span className="text-xs text-muted whitespace-nowrap">
                        {new Date(act.start_date).toLocaleDateString("en-GB", { month: "short", day: "numeric" })}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
