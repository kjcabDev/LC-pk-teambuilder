import { capitalize } from './utils.js';
import { withButtonLoading } from './loader.js';
import { fetchPokemonMatchupDetail, fetchTrainerPersonality } from './api.js';

export function initLightbox({
  lightboxEl,
  tabButtons,
  tabPanels,
  closeBtn,
  matchupRosterEl,
  matchupDetailEl,
  personalityDetailEl,
}) {
  let currentTeam = [];

  function open(team, evaluationResult) {
    currentTeam = team;
    personalityDetailEl.innerHTML = '';
    delete personalityDetailEl.dataset.loaded;

    renderMatchupRoster();
    matchupDetailEl.innerHTML = renderTeamSummary(evaluationResult);
    switchTab('matchups');
    lightboxEl.classList.add('is-open');
  }

  function close() {
    lightboxEl.classList.remove('is-open');
  }

  // Deliberately no backdrop-click listener here — the close button is the
  // only way out, per spec, so an accidental tap outside the panel doesn't
  // lose the evaluation the user just waited for.
  closeBtn.addEventListener('click', close);

  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab, btn));
  });

  function switchTab(tabName, btnEl) {
    tabButtons.forEach((b) => b.classList.toggle('is-active', b.dataset.tab === tabName));
    tabPanels.forEach((p) => p.classList.toggle('is-active', p.id === `tab-${tabName}`));

    if (tabName === 'personality' && !personalityDetailEl.dataset.loaded) {
      const button = btnEl || tabButtons.find((b) => b.dataset.tab === 'personality');
      loadPersonality(button);
    }
  }

  async function loadPersonality(button) {
    try {
      const result = await withButtonLoading(button, fetchTrainerPersonality(currentTeam));
      personalityDetailEl.innerHTML = renderPersonality(result);
      personalityDetailEl.dataset.loaded = 'true';
    } catch (err) {
      personalityDetailEl.innerHTML = `<p class="error-text">Couldn't load your trainer type — ${err.message}.</p>`;
    }
  }

  function renderMatchupRoster() {
    matchupRosterEl.innerHTML = '';
    currentTeam.forEach((pokemon) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.setAttribute('aria-label', capitalize(pokemon.name));
      btn.innerHTML = `<img src="${pokemon.sprite}" alt="${capitalize(pokemon.name)}" width="32" height="32">`;
      btn.addEventListener('click', () => loadPokemonDetail(pokemon, btn));
      matchupRosterEl.appendChild(btn);
    });
  }

  async function loadPokemonDetail(pokemon, btn) {
    try {
      const detail = await withButtonLoading(btn, fetchPokemonMatchupDetail(currentTeam, pokemon.id));
      matchupDetailEl.innerHTML = renderPokemonDetail(pokemon, detail);
    } catch (err) {
      matchupDetailEl.innerHTML = `<p class="error-text">Couldn't load ${capitalize(pokemon.name)}'s matchup — ${err.message}.</p>`;
    }
  }

  // Rendering below is intentionally generic since the server's response
  // shape isn't finalized yet — swap these for real field names once it is.
  function renderTeamSummary(result) {
    return `<p>${result?.summary ?? 'Team evaluation loaded.'}</p>`;
  }

  function renderPokemonDetail(pokemon, detail) {
    return `<p>${capitalize(pokemon.name)}: ${detail?.summary ?? 'No details returned.'}</p>`;
  }

  function renderPersonality(result) {
    return `<p><strong>${result?.type ?? 'Trainer'}</strong></p><p>${result?.description ?? ''}</p>`;
  }

  return { open, close };
}
