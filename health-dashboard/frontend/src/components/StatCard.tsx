interface Props {
  label: string;
  value: string | number | null;
  unit?: string;
  icon: string;
  color: string;
  sub?: string;
}

export function StatCard({ label, value, unit, icon, color, sub }: Props) {
  return (
    <div className="bg-surface rounded-xl p-4 border border-border flex items-start gap-3">
      <div className={`text-2xl w-10 h-10 flex items-center justify-center rounded-lg bg-opacity-10`} style={{ backgroundColor: color + "22" }}>
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-muted text-xs font-medium uppercase tracking-wide">{label}</p>
        <p className="text-2xl font-bold mt-0.5" style={{ color }}>
          {value ?? "—"}
          {value != null && unit && <span className="text-sm font-normal text-muted ml-1">{unit}</span>}
        </p>
        {sub && <p className="text-muted text-xs mt-0.5">{sub}</p>}
      </div>
    </div>
  );
}
