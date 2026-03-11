interface Props {
  logo: string;
  name: string;
  color: string;
  connected?: boolean;
  authPath?: string;
}

export function SectionHeader({ logo, name, color, connected, authPath }: Props) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <span className="text-2xl">{logo}</span>
      <h2 className="text-lg font-semibold" style={{ color }}>{name}</h2>
      {connected === false && authPath && (
        <a
          href={authPath}
          className="ml-auto text-xs px-3 py-1 rounded-full border font-medium hover:opacity-80 transition-opacity"
          style={{ borderColor: color, color }}
        >
          Connect →
        </a>
      )}
      {connected === true && (
        <span className="ml-auto text-xs text-emerald-400 font-medium">● Connected</span>
      )}
    </div>
  );
}
