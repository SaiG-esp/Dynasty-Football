// Thin client for the FastAPI backend (data-engine/main.py).
// Base URL is configurable via VITE_API_BASE_URL so the same build can
// point at a local dev API or a deployed one.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function apiGet(path) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`);
  } catch (err) {
    throw new ApiError(`Could not reach the API at ${API_BASE_URL} (${err.message})`, 0);
  }

  if (!response.ok) {
    throw new ApiError(`API request to ${path} failed with status ${response.status}`, response.status);
  }

  return response.json();
}

/**
 * Fetches every team's defensive intel (havoc score, sacks/game,
 * turnovers/game, last updated timestamp), populated by
 * data-engine/matchup_data3.py into Postgres.
 */
export function fetchDefenses() {
  return apiGet('/defenses');
}

export { ApiError, API_BASE_URL };
