"use strict";

function resetPlaybackState(container) {
  container.querySelectorAll(".audio-button").forEach((button) => {
    const audioId = button.dataset.audio;
    const label = button.dataset.audioLabel ?? `Écouter ${audioId}`;
    button.setAttribute("aria-label", label);
    button.setAttribute("aria-pressed", "false");
  });

  container.querySelectorAll(".playback-status").forEach((status) => {
    status.textContent = "";
  });
}

export function stopAudio(container) {
  container.querySelectorAll("audio").forEach((audio) => {
    audio.pause();
    audio.currentTime = 0;
  });
  resetPlaybackState(container);
}

export function initAudioPlayer(container) {
  container.addEventListener("click", async (event) => {
    const button = event.target.closest(".audio-button");
    if (!button || !container.contains(button)) return;

    const audioId = button.dataset.audio;
    const statusId = button.dataset.statusId ?? audioId;
    const audio = container.querySelector(`#${CSS.escape(audioId)}`);
    const status = container.querySelector(`#status-${CSS.escape(statusId)}`);
    if (!audio || !status) return;

    if (!audio.paused) {
      stopAudio(container);
      return;
    }

    container.querySelectorAll("audio").forEach((otherAudio) => {
      if (otherAudio !== audio) {
        otherAudio.pause();
        otherAudio.currentTime = 0;
      }
    });
    resetPlaybackState(container);

    try {
      await audio.play();
      status.textContent = "Lecture…";
      button.setAttribute("aria-label", "Arrêter la lecture");
      button.setAttribute("aria-pressed", "true");
    } catch {
      status.textContent = "Le fichier audio est introuvable.";
    }
  });

  container.addEventListener("ended", () => resetPlaybackState(container), true);
}
