// Shared constants used across every component. Keep anything here that more
// than one module needs to agree on, so there's a single source of truth.

export const CONFIG = {
  // --- Your LangChain server ---
  LANGCHAIN_SERVER_URL: 'http://localhost:8000',
  ENDPOINTS: {
    // Placeholder contract — adjust once the real server API is finalized.
    EVALUATE_TEAM: '/evaluate-team',       // POST { team } -> team-wide matchup summary
    POKEMON_DETAIL: '/pokemon-detail',     // POST { team, pokemonId } -> single-pokemon breakdown
    PERSONALITY: '/trainer-personality',   // POST { team } -> trainer personality result
  },

  // How long we wait for any server response (LangChain or PokeAPI) before
  // treating it as timed out and re-enabling the UI.
  RESPONSE_TIMEOUT_MS: 15000,

  // --- Public PokeAPI ---
  POKEAPI_BASE_URL: 'https://pokeapi.co/api/v2',
  SPRITE_BASE_URL: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon',

  // --- App behavior ---
  MAX_TEAM_SIZE: 6,
  RANDOM_SUGGESTION_COUNT: 10,
  SEARCH_DEBOUNCE_MS: 250,
  SEARCH_SUGGESTION_LIMIT: 8,
};
