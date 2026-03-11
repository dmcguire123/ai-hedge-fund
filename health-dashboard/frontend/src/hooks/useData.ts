import { useEffect, useState } from "react";

type Status = "loading" | "ok" | "error";

export function useData<T>(fetcher: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [status, setStatus] = useState<Status>("loading");
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setStatus("loading");
    setError(null);
    fetcher()
      .then((d) => { setData(d); setStatus("ok"); })
      .catch((e) => { setError(e.message); setStatus("error"); });
  };

  useEffect(load, deps);

  return { data, status, error, reload: load };
}
