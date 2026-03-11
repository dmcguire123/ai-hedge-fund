const BASE = "";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(BASE + path);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

// ── Auth status ───────────────────────────────────────────────────────────────
export const getStravaStatus = () => get<{ connected: boolean }>("/auth/strava/status");
export const getGoogleStatus = () => get<{ connected: boolean }>("/auth/google/status");

// ── Garmin ────────────────────────────────────────────────────────────────────
export interface GarminToday {
  steps: number;
  calories: number;
  active_calories: number;
  distance_meters: number;
  active_seconds: number;
  floors: number;
  resting_heart_rate: number | null;
  stress_avg: number | null;
  date: string;
}

export interface SleepDay {
  date: string;
  duration_seconds: number;
  deep_seconds: number;
  light_seconds: number;
  rem_seconds: number;
  awake_seconds: number;
  score: number | null;
}

export interface HRDay {
  date: string;
  resting_hr: number | null;
}

export interface GarminActivity {
  id: number;
  name: string;
  type: string;
  start_time: string;
  duration_seconds: number;
  distance_meters: number;
  calories: number;
  avg_hr: number | null;
  elevation_gain: number | null;
}

export interface StepsDay {
  date: string;
  steps: number;
  calories: number;
}

export const getGarminToday = () => get<GarminToday>("/garmin/today");
export const getGarminSleep = (days = 7) => get<SleepDay[]>(`/garmin/sleep?days=${days}`);
export const getGarminHR = (days = 14) => get<HRDay[]>(`/garmin/heart-rate?days=${days}`);
export const getGarminActivities = (limit = 10) => get<GarminActivity[]>(`/garmin/activities?limit=${limit}`);
export const getGarminSteps = (days = 30) => get<StepsDay[]>(`/garmin/steps?days=${days}`);

// ── Strava ────────────────────────────────────────────────────────────────────
export interface StravaActivity {
  id: number;
  name: string;
  type: string;
  start_date: string;
  distance_meters: number;
  duration_seconds: number;
  elevation_gain: number;
  avg_speed_mps: number;
  avg_heart_rate: number | null;
  calories: number | null;
  kudos: number;
}

export interface StravaStats {
  ytd_run_distance: number;
  ytd_ride_distance: number;
  ytd_swim_distance: number;
  all_run_distance: number;
  all_ride_distance: number;
  recent_run_distance: number;
  recent_ride_distance: number;
}

export interface WeekSummary {
  week: string;
  distance_meters: number;
  count: number;
  duration_seconds: number;
}

export const getStravaActivities = (limit = 15) => get<StravaActivity[]>(`/strava/activities?limit=${limit}`);
export const getStravaStats = () => get<StravaStats>("/strava/stats");
export const getStravaWeekly = (weeks = 8) => get<WeekSummary[]>(`/strava/weekly?weeks=${weeks}`);

// ── Google Fit / Rempho ───────────────────────────────────────────────────────
export interface WeightPoint { date: string; weight_kg: number; }
export interface BodyFatPoint { date: string; body_fat_pct: number; }
export interface LatestMetrics {
  weight_kg: number | null;
  weight_date: string | null;
  body_fat_pct: number | null;
  body_fat_date: string | null;
}

export const getWeightHistory = (days = 90) => get<WeightPoint[]>(`/googlefit/weight?days=${days}`);
export const getBodyFatHistory = (days = 90) => get<BodyFatPoint[]>(`/googlefit/bodyfat?days=${days}`);
export const getLatestMetrics = () => get<LatestMetrics>("/googlefit/latest");
