export function LoadingSpinner({ color = "#64748b" }: { color?: string }) {
  return (
    <div className="flex items-center justify-center py-8">
      <div
        className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
        style={{ borderColor: `${color}44`, borderTopColor: color }}
      />
    </div>
  );
}

export function ErrorMsg({ msg }: { msg: string }) {
  return (
    <div className="text-red-400 text-sm py-4 px-3 bg-red-400/10 rounded-lg">
      ⚠ {msg}
    </div>
  );
}
