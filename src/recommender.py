import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its audio/categorical attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    speechiness: float
    instrumentalness: float
    liveness: float

@dataclass
class UserProfile:
    """Stores a listener's taste preferences used for scoring."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_instrumentalness: float = 0.0

# ---------------------------------------------------------------------------
# CSV loader
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dicts with typed values."""
    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness",
                    "speechiness", "instrumentalness", "liveness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            typed: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    typed[key] = int(float(value))
                elif key in float_fields:
                    typed[key] = float(value)
                else:
                    typed[key] = value
            songs.append(typed)
    print(f"Loaded songs: {len(songs)}")
    return songs

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons)."""
    score = 0.0
    reasons = []

    # Categorical matches
    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy proximity
    energy_sim = (1.0 - abs(song["energy"] - user_prefs.get("target_energy", 0.5))) * 1.0
    score += energy_sim
    reasons.append(f"energy proximity (+{energy_sim:.2f})")

    # Valence proximity
    valence_sim = (1.0 - abs(song["valence"] - user_prefs.get("target_valence", 0.5))) * 0.5
    score += valence_sim
    reasons.append(f"valence proximity (+{valence_sim:.2f})")

    # Instrumentalness proximity
    inst_sim = (1.0 - abs(song["instrumentalness"] - user_prefs.get("target_instrumentalness", 0.0))) * 0.5
    score += inst_sim
    reasons.append(f"instrumentalness proximity (+{inst_sim:.2f})")

    # Acousticness preference
    acoustic_target = 1.0 if user_prefs.get("likes_acoustic", False) else 0.0
    acoustic_sim = (1.0 - abs(song["acousticness"] - acoustic_target)) * 0.3
    score += acoustic_sim
    reasons.append(f"acousticness match (+{acoustic_sim:.2f})")

    return round(score, 3), reasons

# ---------------------------------------------------------------------------
# Recommender (functional)
# ---------------------------------------------------------------------------

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, then return the top-k results sorted highest score first.
    Deduplicates by song id so repeated CSV rows never pollute the output.
    """
    seen_ids = set()
    unique_songs = []
    for song in songs:
        if song["id"] not in seen_ids:
            seen_ids.add(song["id"])
            unique_songs.append(song)

    scored = [(song, *score_song(user_prefs, song)) for song in unique_songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]

# ---------------------------------------------------------------------------
# OOP interface (used by tests)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP wrapper around the functional scoring logic."""

    def __init__(self, songs: List[Song]):
        """Initialise the recommender with a list of Song dataclass instances."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects ranked by score for the given UserProfile."""
        user_prefs = {
            "favorite_genre":        user.favorite_genre,
            "favorite_mood":         user.favorite_mood,
            "target_energy":         user.target_energy,
            "likes_acoustic":        user.likes_acoustic,
            "target_valence":        user.target_valence,
            "target_instrumentalness": user.target_instrumentalness,
        }
        song_dicts = [vars(s) for s in self.songs]
        ranked = recommend_songs(user_prefs, song_dicts, k=k)
        ranked_ids = {r[0]["id"] for r in ranked}
        order = {r[0]["id"]: i for i, r in enumerate(ranked)}
        matched = [s for s in self.songs if s.id in ranked_ids]
        return sorted(matched, key=lambda s: order[s.id])

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_prefs = {
            "favorite_genre":        user.favorite_genre,
            "favorite_mood":         user.favorite_mood,
            "target_energy":         user.target_energy,
            "likes_acoustic":        user.likes_acoustic,
            "target_valence":        user.target_valence,
            "target_instrumentalness": user.target_instrumentalness,
        }
        _, reasons = score_song(user_prefs, vars(song))
        return " | ".join(reasons)
