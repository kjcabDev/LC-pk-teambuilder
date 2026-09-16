import { CONFIG } from './config.js';

// Generic fetch wrapper that aborts and rejects after RESPONSE_TIMEOUT_MS,
// so any caller (and withButtonLoading, which just awaits the promise) knows
// within a bounded time whether the request succeeded, failed, or timed out.
async function fetchWithTimeout(url, options = {}, timeoutMs = CONFIG.RESPONSE_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    if (!res.ok) {
      throw new Error(`Server responded with ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out');
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

function post(path, body) {
  return fetchWithTimeout(`${CONFIG.LANGCHAIN_SERVER_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

// team: array of { id, name, sprite }
export function evaluateTeam(team) {
  return post(CONFIG.ENDPOINTS.EVALUATE_TEAM, { team });
}

export function fetchPokemonMatchupDetail(team, pokemonId) {
  return post(CONFIG.ENDPOINTS.POKEMON_DETAIL, { team, pokemonId });
}

export function fetchTrainerPersonality(team) {
  return post(CONFIG.ENDPOINTS.PERSONALITY, { team });
}
