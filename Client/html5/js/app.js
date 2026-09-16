import { CONFIG } from './config.js';
import { withButtonLoading } from './loader.js';
import { evaluateTeam } from './api.js';
import { initSearch } from './search.js';
import { initRandomSuggestions } from './randomSuggestions.js';
import { initRoster } from './roster.js';
import { initLightbox } from './lightbox.js';
import { initSidebar } from './sidebar.js';
import { initSaveRating } from './screenshot.js';

async function loadFragment(url, mountSelector) {
  const mount = document.querySelector(mountSelector);
  if (!mount) return;
  try {
    const res = await fetch(url);
    mount.innerHTML = await res.text();
  } catch (err) {
    console.error(`Failed to load fragment: ${url}`, err);
  }
}

async function init() {
  // Sidebar and footer are separate fragment files (html/sidebar.html,
  // html/footer.html) so every future page can share them without
  // duplicating markup — pull them in before wiring up anything that lives
  // inside them (the hamburger toggle needs #sidebar-overlay to exist).
  await Promise.all([
    loadFragment('html/sidebar.html', '#sidebar-include'),
    loadFragment('html/footer.html', '#footer-include'),
  ]);

  initSidebar({
    hamburgerBtn: document.getElementById('hamburger-btn'),
    overlayEl: document.getElementById('sidebar-overlay'),
  });

  const lightbox = initLightbox({
    lightboxEl: document.getElementById('lightbox'),
    tabButtons: Array.from(document.querySelectorAll('.tab-btn')),
    tabPanels: Array.from(document.querySelectorAll('.tab-panel')),
    closeBtn: document.getElementById('lightbox-close'),
    matchupRosterEl: document.getElementById('matchup-roster'),
    matchupDetailEl: document.getElementById('matchup-detail'),
    personalityDetailEl: document.getElementById('personality-detail'),
  });

  initSaveRating(
    document.getElementById('save-rating-btn'),
    document.querySelector('.lightbox-panel')
  );

  const rateBtn = document.getElementById('rate-team-btn');
  let randomSuggestions; // assigned below; referenced by roster's onChange

  const roster = initRoster({
    gridEl: document.getElementById('roster-grid'),
    countEl: document.getElementById('roster-count'),
    clearBtn: document.getElementById('clear-team-btn'),
    rateBtn,
    maxTeamSize: CONFIG.MAX_TEAM_SIZE,
    onChange: (count, max) => randomSuggestions?.setFull(count >= max),
    onRateTeam: async (team) => {
      try {
        const result = await withButtonLoading(rateBtn, evaluateTeam(team));
        lightbox.open(team, result);
      } catch (err) {
        alert(`Couldn't rate your team — ${err.message}.`);
      }
    },
  });

  initSearch({
    inputEl: document.getElementById('search-input'),
    clearBtn: document.getElementById('search-clear-btn'),
    suggestionsEl: document.getElementById('suggestions'),
    onSelect: roster.addPokemon,
  });

  randomSuggestions = initRandomSuggestions({
    gridEl: document.getElementById('random-suggestions'),
    shuffleBtn: document.getElementById('shuffle-btn'),
    onPick: roster.addPokemon,
  });
}

document.addEventListener('DOMContentLoaded', init);
