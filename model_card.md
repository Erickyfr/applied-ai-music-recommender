# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

### VibeFinder 1.0

---

## 2. Intended Use

This system suggests up to 5 songs from an 18-song catalog based on a user's
preferred genre, mood, energy level, acoustic texture, emotional valence, and
preference for instrumental vs. vocal tracks. It is designed for classroom
exploration of content-based filtering — not for deployment with real users.

---

## 3. How the Model Works

Each song in the catalog has a set of descriptors: what genre it is, what mood
it creates, how intense it feels (energy), how happy or dark it sounds
(valence), how acoustic or electronic it is, and whether it has vocals or is
purely instrumental.

A user profile stores the same kinds of preferences — the genre they want,
the mood they are in, and target numbers for energy, valence, and
instrumentalness.

The recommender goes through every song and asks: "How closely does this song
match what the user wants?" Genre and mood are the strongest factors. For
numeric features like energy, it calculates the *distance* between the song's
value and the user's target — songs closest to the target score higher. All
the component scores are added up and the top 5 songs with the highest totals
are recommended.

---

## 4. Data

The catalog contains 18 songs across 15 genres and 14 moods. The original
starter file had 10 songs. Eight were added to improve diversity:
hip-hop, R&B, folk, classical, EDM, metal, reggae, and blues were all missing
from the starter set.

Each song has 13 attributes: id, title, artist, genre, mood, energy,
tempo_bpm, valence, danceability, acousticness, speechiness,
instrumentalness, and liveness.

Parts of musical taste still missing from the dataset: country, K-pop,
Latin, gospel, and electronic sub-genres like drum and bass or house. The
catalog also skews toward English-language Western music, so users with
preferences outside that space will always get poor recommendations.

---

## 5. Strengths

The system works best when the user has a clear, consistent taste profile.
Users who want "lofi/chill" or "rock/intense" receive results that feel very
accurate — the top-ranked songs match both the categorical labels and the
numeric feel of the request.

Genre and mood together form a strong enough filter that the system is
transparent and easy to explain. For every recommendation, the system prints
exactly which components contributed points, so it is never a black box.
This is a significant advantage over collaborative filtering, which cannot
explain why it recommends a song.

---

## 6. Limitations and Bias

**Genre wall:** Because a genre match is worth +2.0 points and the entire
numeric portion maxes out at ~2.3 points, a genre mismatch is almost
impossible to overcome no matter how perfectly the numeric features align.
A jazz song with energy=0.40, valence=0.60, and acousticness=0.86 will always
rank below a lofi song with worse numeric alignment, simply because it is not
labeled "lofi." This creates a hard filter bubble around genre that the system
cannot escape.

**Mood is binary, not a spectrum:** The system awards 1.0 for an exact mood
match and 0.0 for anything else. "Relaxed" and "chill" are emotionally almost
identical, but the system treats them as completely different. A user who wants
"chill" gets zero mood credit for "relaxed" songs.

**Cold-start and catalog size:** With only 18 songs, some genres appear once.
A metal fan will always get the same song at rank #3 regardless of how the
weights are set. The system cannot provide diversity within a genre it only
has one example of.

**The conflicted profile exposes a structural bias:** A user who wants
high energy (0.9) but listens to blues/sad music faces a contradiction — blues
songs in the catalog are all low energy. The genre+mood match wins so
decisively (+3.0 points for "blues/sad") that "Empty Barstool" (energy=0.30)
ranks #1 even though it is the furthest song from the user's energy preference.
The scoring formula has no way to express "I want high-energy blues" because
that combination does not exist in the catalog.

**No personalization over time:** The system treats every session identically.
It cannot learn that a user skipped all jazz recommendations last time, or that
they keep replaying the #1 result.

---

## 7. Evaluation

Six user profiles were tested:

| Profile | Key finding |
| ------- | ----------- |
| Chill Lofi | Top 2 results both scored ~5.15/5.3 — near-perfect match. Results felt right. |
| High-Energy Pop | Sunrise City ranked #1 with 5.206. Gym Hero (#2) has wrong mood (intense) but high energy dragged it up. |
| Deep Intense Rock | Storm Runner scored 5.220 — highest score of any profile. Only one rock song exists, so #2 onwards are cross-genre. |
| Conflicted (high energy + sad blues) | Empty Barstool won despite energy=0.30 vs. target=0.90. Genre+mood (+3.0) swamped the energy penalty. |
| Omnivore (mid everything) | Spacewalk Thoughts won on genre+mood. Results felt reasonable but uninspired — a "meh" profile gets "meh" results. |
| Niche Genre (bossa nova — not in catalog) | No genre match ever fired. Velvet Hours won purely on mood match + numeric proximity. The system degraded gracefully but cannot discover what it was never given. |

**Weight experiment (energy ×2, genre ÷2):**

For High-Energy Pop: Rooftop Lights (indie pop / happy) jumped from #3 to a
score competitive with #2, and Corner Store Chronicles and Overdrive Festival
entered the top 5. The recommendations became more energetically diverse but
less genre-pure. Whether that is better depends on the user.

For the Conflicted profile: Empty Barstool still ranked #1 but with a lower
dominance score (3.989 vs. 4.589), and high-energy songs like Storm Runner and
Rust and Thunder moved significantly up the list. This felt more accurate for
a user who said their target energy was 0.90.

**Conclusion:** Halving the genre weight produces more energetically honest
results for edge-case users but risks surprising genre-loyal users. The
original weights are better for typical use; the experimental weights are
better when the user's numeric preferences conflict with their genre label.

---

## 8. Future Work

- **Mood similarity groups:** Treat "chill," "relaxed," and "focused" as
  partially overlapping rather than fully separate. A partial mood match
  could award 0.5 instead of 0.0.
- **Catalog expansion:** The system needs at least 3–5 songs per genre to
  provide meaningful diversity. Doubling the catalog to ~40 songs would
  dramatically improve results for edge-case profiles.
- **Energy-genre conflict detection:** If the user's target energy is far
  from all songs in their preferred genre, the system should warn the user
  or suggest a secondary genre that better fits their numeric preferences.
- **Per-session history:** Even a simple "songs seen" set would prevent the
  same track from appearing every session for niche-genre users.
- **Diversity penalty:** Instead of always returning the top-k by score,
  apply a small penalty to consecutive songs by the same artist or in the
  same sub-genre to improve variety.

---

## 9. Personal Reflection

Building this recommender made the trade-off between "filter bubble" and
"discovery" feel concrete. The genre weight feels right most of the time —
a pop fan genuinely does not want jazz — but the conflicted profile showed
that a hard categorical filter can override every numeric signal the user
sends. The most surprising finding was that the system degrades gracefully
for unknown genres: with no "bossa nova" in the catalog, the niche profile
still surfaced Velvet Hours and Coffee Shop Stories, which are the closest
reasonable alternatives. That is a real strength of content-based filtering.
It also made clear why real platforms need collaborative filtering as a second
layer: the catalog ceiling is invisible to the scoring math, but a real user
would notice it immediately.
