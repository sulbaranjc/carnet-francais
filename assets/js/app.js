import { initAudioPlayer, stopAudio } from "./audio-player.js";
import { filterVocabulary, renderVocabulary } from "./vocabulary.js";

const searchInput = document.querySelector("#word-search");
const searchStatus = document.querySelector("#search-status");
const vocabularyGrid = document.querySelector("#vocabulary-grid");

function setSearchStatus(entries, query) {
  const normalizedQuery = query.trim();
  if (!normalizedQuery) {
    searchStatus.textContent = `${entries.length} mots à pratiquer.`;
    return;
  }

  if (!entries.length) {
    searchStatus.textContent = `Aucun mot ne commence par « ${normalizedQuery} ».`;
    return;
  }

  const noun = entries.length === 1 ? "mot" : "mots";
  searchStatus.textContent = `${entries.length} ${noun} commence${entries.length === 1 ? "" : "nt"} par « ${normalizedQuery} ».`;
}

async function loadVocabulary() {
  const response = await fetch("assets/data/vocabulary.json");
  if (!response.ok) throw new Error(`Vocabulary data unavailable (${response.status})`);
  const payload = await response.json();
  return payload.entries;
}

async function bootstrap() {
  try {
    const entries = await loadVocabulary();
    initAudioPlayer(vocabularyGrid);

    const updateView = () => {
      const filteredEntries = filterVocabulary(entries, searchInput.value);
      stopAudio(vocabularyGrid);
      renderVocabulary(filteredEntries, vocabularyGrid);
      setSearchStatus(filteredEntries, searchInput.value);
    };

    searchInput.addEventListener("input", updateView);
    updateView();
  } catch {
    searchStatus.textContent = "Les mots ne sont pas disponibles pour le moment.";
  }
}

bootstrap();
