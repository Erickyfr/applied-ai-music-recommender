# Model Card — Applied AI Music Recommender

## Model Name

**VibeFinder 2.0** — Applied AI Music Recommendation System

---

## Goal / Task

Interpret a user's natural language mood description and return a ranked list of personalized song recommendations from a local catalog, with human-readable explanations for each result.

---

## Original Project

This model extends the **Music Recommender Simulation** (CodePath AI110, Module 1–3), which used hardcoded user profiles and a weighted scoring engine to rank songs from a CSV file. VibeFinder 2.0 adds a natural language input layer and an automated reliability testing system on top of that foundation.

---

## Data Used

- **Source:** Local CSV file (`data/songs.csv`)
- **Size:** ~20 songs
- **Features:** genre, mood, energy (0–1), valence (0–1), danceability, acousticness, speechiness, instrumentalness, liveness, tempo_bpm
- **Limits:** Small catalog. No real user listening history. All songs are pre-labeled by a human — labels are subjective and not validated at scale.

---

## Algorithm Summary

1. User types a mood description in plain English
2. The AI logic layer scans for keywords (e.g., "tired", "gym", "study") and maps them to a structured preference profile (genre, mood, energy target, etc.)
3. Every song in the catalog is scored against that profile using weighted math rules:
   - Genre match = +2.0 points
   - Mood match = +1.0 point
   - Energy/valence/instrumentalness proximity = up to +1.0 combined
4. Songs are ranked highest score first. Top 5 are returned with score and reason list.

---

## Observed Behavior / Biases

- **Genre dominance:** A genre match gives +2.0 points — the highest single weight. Songs that match genre almost always appear in the top results regardless of other attributes.
- **Filter bubble risk:** If the catalog has more pop songs than any other genre, pop-profile users will always get diverse results while niche-genre users (e.g., bossa nova) get no genre matches and fall back to numerical proximity alone.
- **Keyword brittleness:** The NLP layer only recognizes specific hardcoded words. "Exhausted," "drained," or "melancholy" return the default pop profile instead of the chill/lofi profile — a significant gap.
- **Fixed confidence score:** Confidence is hardcoded to 0.85 for every run regardless of how well the input matched any keyword pattern. This is misleading for ambiguous inputs.

---

## Evaluation Process

Three test cases were run through `evaluation.py`:

| Input | Expected Mood | Actual Mood | Result |
|---|---|---|---|
| "I am tired and want calm music" | chill | chill | ✅ PASS |
| "I need music for the gym" | happy | happy | ✅ PASS |
| "I need focus music for homework" | chill | chill | ✅ PASS |

**Reliability Score: 3/3 tests passed**
Additional manual testing revealed the fallback default (pop/happy) fires too aggressively for unrecognized inputs. A future version would return an "unclear input" warning instead of silently defaulting.

---

## Intended Use

- Learning tool to understand how content-based recommendation systems work
- Demonstration of how NLP input can drive structured algorithmic logic
- Portfolio project showing modular AI system design

## Non-Intended Use

- Not suitable for production music platforms — catalog is too small and NLP too limited
- Should not be used to make decisions about real user preferences at scale
- Not designed to handle multilingual input

---

## Ideas for Improvement

1. **Dynamic confidence scoring** — calculate confidence based on how many keywords matched rather than returning a fixed value
2. **Expanded NLP layer** — use synonym mapping or a small embedding model to handle words like "exhausted," "mellow," "pumped"
3. **Larger catalog** — integrate a real music API (Spotify, Last.fm) to score against thousands of songs instead of ~20
4. **Feedback loop** — let users rate recommendations and adjust weights over time

---

## AI Collaboration Reflection

**One instance where AI was helpful:**
When designing the scoring function, AI suggested using `(1.0 - abs(song_value - target_value))` as a proximity formula instead of a simple greater-than comparison. This was genuinely better — it rewards songs that are *close* to the target rather than just high or low, which made the recommendations feel more accurate.

**One instance where AI was wrong:**
AI initially suggested using `sorted()` with a lambda on a list of tuples but got the index wrong for the sort key, causing songs to sort by title instead of score. The output looked fine at first glance but the rankings were wrong. Catching this required manually checking a known high-score song and noticing it wasn't at the top.

---

## Limitations and Biases (Summary)

The system over-prioritizes genre due to its +2.0 weight. With a small catalog, this creates a strong filter bubble where users whose favorite genre is underrepresented in the data get worse results. The NLP layer is brittle and fails silently on unrecognized input. Confidence scores are not dynamically computed and should not be trusted as real probability estimates.
