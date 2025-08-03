# Playlist Evaluator – Development Checklist (TDD-Oriented)

This checklist outlines the key tasks and corresponding test-driven development steps for the `playlist-evaluator` project.

---

## Phase 1: Project Setup & Test Harness

- [x] Create GitHub repository and local folder structure
- [x] Add `requirements.txt` or `pyproject.toml` with:
  - `pytest`
  - `requests` 
  - `openai`
  - `tqdm`
- [x] Create basic test runner using `pytest`
- [x] Write dummy test to confirm setup

---

## Phase 2: Define Core Data Models

- [ ] Create `models.py` with:
  - `Track` – includes title, artist, audio features, genres
  - `PlaylistInput` – list of `Track` objects + prompt
  - `EvaluationResult` – final score and sub-scores
- [ ] Write unit tests to validate default values and types
- [ ] Test data integrity with missing or malformed input

---

## Phase 3: Prompt Alignment Module

- [ ] Create `alignment.py` to:
  - Call OpenAI embedding API
  - Compute similarity between prompt and song metadata
- [ ] Add caching for prompt and title embeddings
- [ ] Write tests with:
  - Mocked API response
  - Valid and invalid prompts
  - Correct shape and range of output

---

## Phase 4: Musical Cohesion Module

- [ ] Create `cohesion.py` to:
  - Analyze genre overlap
  - Compare numeric features like tempo, valence, energy
- [ ] Write tests using sample audio feature dicts
- [ ] Validate cohesion score computation

---

## Phase 5: Humor & Cleverness Detection

- [ ] Create `humor.py` to:
  - Use regexes, heuristics, or ML to find puns and thematic references
- [ ] Write tests with:
  - Obvious jokes and puns
  - Neutral song titles
  - Edge cases (e.g. unrelated references)

---

## Phase 6: Aggregation & Final Scoring

- [ ] Create `scorer.py` with main `evaluate_playlist()` function
- [ ] Combine scores from alignment, cohesion, and humor
- [ ] Allow weighting via config or function parameters
- [ ] Test:
  - Correctness of combined score
  - Weighted average logic
  - Output matches expected data format

---

## Phase 7: Integration & Regression Testing

- [ ] Create test fixtures with full playlists and prompts
- [ ] Run evaluation end-to-end
- [ ] Validate:
  - Overall score range and consistency
  - Sub-scores by category
  - Regression consistency with snapshot tests

