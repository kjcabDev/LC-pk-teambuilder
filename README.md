# PKTB — Pokémon Team Builder

A for-fun LangChain project built for [bitknvs.com](https://bitknvs.com) by **Kevin Joseff Cabrera**.

PKTB lets you search for Pokémon, build a team of up to six, and send it off to an AI agent for evaluation. The agent breaks down which types your team is strong and weak against, lets you dig into how each individual Pokémon fits into the lineup, and takes a (not-too-serious) guess at what your picks say about your personality as a trainer.

## How it works

1. **Search or browse** — type a name in the search bar, or grab one of the random suggestion cards, to add a Pokémon to your roster.
2. **Build your team** — up to six Pokémon at a time. Remove or clear the roster at any point.
3. **Rate my team** — sends the roster to the LangChain-powered backend for evaluation.
4. **Team matchups** — see a chart of which types your team is strong against and weak against, then tap any individual Pokémon in the lineup for its own breakdown.
5. **Personality** — a lighthearted read on what kind of trainer your team choices suggest, including a guess at your Myers-Briggs type.

## Tech stack

**Frontend**
- Vanilla HTML, CSS, and JavaScript (ES modules) — no framework, no build step
- [Chart.js](https://www.chartjs.org/) for the pros/cons type charts
- [html2canvas](https://html2canvas.hertzen.com/) for the "save rating" screenshot feature
- [PokéAPI](https://pokeapi.co/) for Pokémon names, sprites, and data

**Backend**
- Flask
- LangChain
- Anthropic's Claude
- ChromaDB (vector store for the team-evaluation RAG pipeline)

## Project structure

```
Client/html5/
├── webapp.html          # entry point
├── css/
│   └── styles.css
├── html/
│   ├── sidebar.html      # nav drawer fragment
│   └── footer.html       # footer fragment
├── js/
│   ├── app.js            # singleton manager — wires every component together
│   ├── config.js         # shared constants (server URLs, timeouts, team size, etc.)
│   ├── api.js             # calls to the LangChain server
│   ├── pokeapi.js         # calls to the public PokeAPI
│   ├── search.js          # search bar + typeahead suggestions
│   ├── randomSuggestions.js
│   ├── roster.js          # team state management
│   ├── lightbox.js        # evaluation lightbox (matchups + personality)
│   ├── charts.js          # Chart.js wrapper for the pros/cons charts
│   ├── sidebar.js         # hamburger/nav drawer behavior
│   ├── aboutModal.js      # About PKTB modal
│   ├── screenshot.js      # save-rating screenshot behavior
│   ├── loader.js          # shared loading/disable-button behavior
│   └── utils.js
└── static/                # image assets
```

## Notes

This is a hobby project, not a production service — the personality readout and team ratings are for fun and shouldn't be taken as anything more serious than that.
