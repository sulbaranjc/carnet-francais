const SPEAKER_ICON = `
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M3 9v6h4l5 4V5L7 9H3zm12.5 3a4.5 4.5 0 0 0-2.5-4.03v8.05A4.5 4.5 0 0 0 15.5 12zm0-8.5v2.05a7 7 0 0 1 0 12.9v2.05a9 9 0 0 0 0-16.95z"/>
  </svg>`;

export function normalizeSearch(value) {
  return value
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .trim()
    .toLocaleLowerCase("fr-FR");
}

export function filterVocabulary(entries, query) {
  const normalizedQuery = normalizeSearch(query);
  if (!normalizedQuery) return entries;

  return entries.filter((entry) => normalizeSearch(entry.word).startsWith(normalizedQuery));
}

function element(tagName, { className, text, attributes = {} } = {}) {
  const node = document.createElement(tagName);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  Object.entries(attributes).forEach(([name, value]) => node.setAttribute(name, value));
  return node;
}

function labelAndText(label, value, className) {
  const fragment = document.createDocumentFragment();
  fragment.append(
    element("p", { className: "label", text: label }),
    element("p", { className, text: value }),
  );
  return fragment;
}

function createAudioButton(audioId, label, small = false, statusId = audioId) {
  const audioButton = element("button", {
    className: `audio-button${small ? " audio-button--small" : ""}`,
    attributes: {
      type: "button",
      "data-audio": audioId,
      "data-audio-label": label,
      "data-status-id": statusId,
      "aria-label": label,
      "aria-pressed": "false",
    },
  });
  audioButton.innerHTML = SPEAKER_ICON;
  return audioButton;
}

export function createVocabularyCard(entry) {
  const card = element("article", { className: "vocabulary-card" });
  card.append(element("span", { className: "card-number", text: String(entry.number).padStart(2, "0") }));

  if (entry.article) {
    card.append(element("p", { className: "article", text: entry.article.toLocaleUpperCase("fr-FR") }));
  }

  card.append(element("h2", { text: entry.word }));
  card.append(element("p", { className: "label", text: "Prononciation" }));

  const pronunciation = element("div", { className: "pronunciation-row" });
  pronunciation.append(
    element("span", { className: "ipa", text: entry.ipa }),
    createAudioButton(entry.id, `Écouter ${entry.word}`),
  );
  card.append(pronunciation);

  card.append(
    element("p", {
      className: "playback-status",
      attributes: { id: `status-${entry.id}`, "aria-live": "polite" },
    }),
  );
  card.append(element("p", { className: "label", text: "Une phrase" }));
  const sentenceRow = element("div", { className: "sentence-row" });
  sentenceRow.append(
    element("p", { className: "sentence", text: entry.sentence }),
    createAudioButton(
      `sentence-${entry.id}`,
      `Écouter la phrase : ${entry.sentence}`,
      true,
      entry.id,
    ),
  );
  card.append(sentenceRow);
  card.append(labelAndText("À retenir", entry.rule, "rule"));
  card.append(
    element("img", {
      className: "scene",
      attributes: { src: entry.image.src, alt: entry.image.alt },
    }),
    element("audio", {
      attributes: { id: entry.id, preload: "metadata", src: entry.audio.src },
    }),
    element("audio", {
      attributes: {
        id: `sentence-${entry.id}`,
        preload: "metadata",
        src: entry.sentenceAudio.src,
      },
    }),
  );

  return card;
}

export function renderVocabulary(entries, container) {
  container.replaceChildren(...entries.map(createVocabularyCard));
}
