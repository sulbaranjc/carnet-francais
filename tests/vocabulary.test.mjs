import test from "node:test";
import assert from "node:assert/strict";

import { filterVocabulary, normalizeSearch } from "../assets/js/vocabulary.js";

const vocabulary = [
  { id: "tante", word: "tante" },
  { id: "the", word: "thé" },
  { id: "bonjour", word: "Bonjour !" },
];

test("normaliza acentos y mayúsculas para la búsqueda", () => {
  assert.equal(normalizeSearch(" THÉ "), "the");
  assert.equal(normalizeSearch("Bonjour !"), "bonjour !");
});

test("filtra las palabras cuyo inicio coincide con la consulta", () => {
  assert.deepEqual(
    filterVocabulary(vocabulary, "t").map((entry) => entry.id),
    ["tante", "the"],
  );
  assert.deepEqual(
    filterVocabulary(vocabulary, "thé").map((entry) => entry.id),
    ["the"],
  );
});

test("una consulta vacía conserva todas las palabras", () => {
  assert.deepEqual(filterVocabulary(vocabulary, ""), vocabulary);
});
