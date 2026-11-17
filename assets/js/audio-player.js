"use strict";

const audioElements = [...document.querySelectorAll("audio")];
const audioButtons = [...document.querySelectorAll(".audio-button")];

function resetPlaybackState() {
  audioButtons.forEach((button) => {
    const word = button.getAttribute("data-audio");
    button.setAttribute("aria-label", `Écouter ${word}`);
    button.setAttribute("aria-pressed", "false");
  });

  document.querySelectorAll(".playback-status").forEach((status) => {
    status.textContent = "";
  });
}

function stopAllExcept(activeAudio) {
  audioElements.forEach((audio) => {
    if (audio !== activeAudio) {
      audio.pause();
      audio.currentTime = 0;
    }
  });
}

audioButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const audioId = button.getAttribute("data-audio");
    const audio = document.getElementById(audioId);
    const status = document.getElementById(`status-${audioId}`);

    if (!audio || !status) return;

    if (!audio.paused) {
      audio.pause();
      audio.currentTime = 0;
      resetPlaybackState();
      return;
    }

    stopAllExcept(audio);
    resetPlaybackState();

    try {
      await audio.play();
      status.textContent = "Lecture…";
      button.setAttribute("aria-label", "Arrêter la lecture");
      button.setAttribute("aria-pressed", "true");
    } catch {
      status.textContent = "Le fichier audio est introuvable.";
    }
  });
});

audioElements.forEach((audio) => {
  audio.addEventListener("ended", resetPlaybackState);
});
