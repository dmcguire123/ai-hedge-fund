import {
  Area,
  AreaChart,
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
  getGarminHR,
  getGarminSleep,
  getGarminSteps,
  getGarminToday,
} from "../services/api";
import { ErrorMsg, LoadingSpinner } from "./LoadingSpinner";
import { SectionHeader } from "./SectionHeader";
import { StatCard } from "./StatCard";

const COLOR = "#00b3e6";

function fmtDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-GB", { month: "short", day: "numeric" });
}
function fmtHours(seconds: number) {
  return (seconds / 3600).toFixed(1);
}

export function GarminSection() {
  const today = useData(getGarminToday);
  const sleep = useData(() => getGarminSleep(7));
  const hr = useData(() => getGarminHR(14));
  const steps = useData(() => getGarminSteps(30));

  const d = today.data;

  return (
    <section>
      <SectionHeader logo="🟦" name="Garmin" color={COLOR} />

      {/* Today stats */}
      {today.status === "loading" && <LoadingSpinner color={COLOR} />}
      {today.status === "error" && <ErrorMsg msg={today.error!} />}
      {d && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-6">
          <StatCard label="Steps" value={d.steps.toLocaleString()} icon="👟" color={COLOR} />
          <StatCard label="Calories" value={d.calories} unit="kcal" icon="🔥" color={COLOR} />
          <StatCard label="Distance" value={(d.distance_meters / 1000).toFixed(1)} unit="km" icon="📍" color={COLOR} />
          <StatCard label="Active" value={Math.round(d.active_seconds / 60)} unit="min" icon="⚡" color={COLOR} />
          <StatCard label="Floors" value={d.floors} icon="🏢" color={COLOR} />
          <StatCard label="Resting HR" value={d.resting_heart_rate} unit="bpm" icon="❤️" color={COLOR} />
          <StatCard label="Stress" value={d.stress_avg} icon="🧘" color={COLOR} />
          <StatCard label="Active Cal" value={d.active_calories} unit="kcal" icon="💪" color={COLOR} />
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Steps chart */}
        <div className="bg-surface rounded-xl p-4 border border-border">
          <h3 className="text-sm font-medium text-muted mb-3">Steps – last 30 days</h3>
          {steps.status === "loading" && <LoadingSpinner color={COLOR} />}
          {steps.status === "error" && <ErrorMsg msg={steps.error!} />}
          {steps.data && (
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={steps.data.map(d => ({ ...d, date: fmtDate(d.date) }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} interval="preserveStartEnd" />
                <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                <Bar dataKey="steps" fill={COLOR} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Sleep chart */}
        <div className="bg-surface rounded-xl p-4 border border-border">
          <h3 className="text-sm font-medium text-muted mb-3">Sleep – last 7 nights</h3>
          {sleep.status === "loading" && <LoadingSpinner color={COLOR} />}
          {sleep.status === "error" && <ErrorMsg msg={sleep.error!} />}
          {sleep.data && (
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={sleep.data.map(d => ({
                date: fmtDate(d.date),
                Deep: +(fmtHours(d.deep_seconds)),
                REM: +(fmtHours(d.rem_seconds)),
                Light: +(fmtHours(d.light_seconds)),
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} />
                <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} unit="h" />
                <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                <Bar dataKey="Deep" stackId="a" fill="#6366f1" radius={[0, 0, 0, 0]} />
                <Bar dataKey="REM" stackId="a" fill="#8b5cf6" />
                <Bar dataKey="Light" stackId="a" fill="#a78bfa" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* HR trend */}
        <div className="bg-surface rounded-xl p-4 border border-border md:col-span-2">
          <h3 className="text-sm font-medium text-muted mb-3">Resting Heart Rate – last 14 days</h3>
          {hr.status === "loading" && <LoadingSpinner color={COLOR} />}
          {hr.status === "error" && <ErrorMsg msg={hr.error!} />}
          {hr.data && (
            <ResponsiveContainer width="100%" height={160}>
              <AreaChart data={hr.data.map(d => ({ date: fmtDate(d.date), HR: d.resting_hr }))}>
                <defs>
                  <linearGradient id="hrGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={COLOR} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={COLOR} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} />
                <YAxis tick={{ fill: "#64748b", fontSize: 11 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} unit=" bpm" />
                <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }} />
                <Area type="monotone" dataKey="HR" stroke={COLOR} fill="url(#hrGrad)" strokeWidth={2} dot={{ r: 3, fill: COLOR }} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </section>
  );
}
