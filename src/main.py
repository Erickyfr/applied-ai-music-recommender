"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = {
    "Chill Lofi": {
        "favorite_genre":          "lofi",
        "favorite_mood":           "chill",
        "target_energy":           0.40,
        "likes_acoustic":          True,
        "target_valence":          0.60,
        "target_instrumentalness": 0.80,
    },
    "High-Energy Pop": {
        "favorite_genre":          "pop",
        "favorite_mood":           "happy",
        "target_energy":           0.85,
        "likes_acoustic":          False,
        "target_valence":          0.82,
        "target_instrumentalness": 0.00,
    },
    "Deep Intense Rock": {
        "favorite_genre":          "rock",
        "favorite_mood":           "intense",
        "target_energy":           0.90,
        "likes_acoustic":          False,
        "target_valence":          0.40,
        "target_instrumentalness": 0.00,
    },
    # --- Adversarial / edge-case profiles ---
    "Conflicted (high energy + sad mood)": {
        "favorite_genre":          "blues",
        "favorite_mood":           "sad",
        "target_energy":           0.90,
        "likes_acoustic":          True,
        "target_valence":          0.20,
        "target_instrumentalness": 0.10,
    },
    "Omnivore (mid everything)": {
        "favorite_genre":          "ambient",
        "favorite_mood":           "chill",
        "target_energy":           0.50,
        "likes_acoustic":          False,
        "target_valence":          0.50,
        "target_instrumentalness": 0.50,
    },
    "Niche Genre (no catalog match)": {
        "favorite_genre":          "bossa nova",
        "favorite_mood":           "romantic",
        "target_energy":           0.45,
        "likes_acoustic":          True,
        "target_valence":          0.75,
        "target_instrumentalness": 0.30,
    },
}


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_profile(name: str, prefs: dict, results: list) -> None:
    print(f"\n{'='*60}")
    print(f"  Profile: {name}")
    print(f"{'='*60}")
    print(f"  Genre: {prefs['favorite_genre']}  |  Mood: {prefs['favorite_mood']}")
    print(f"  Energy: {prefs['target_energy']}  |  Acoustic: {prefs['likes_acoustic']}")
    print(f"  Valence: {prefs['target_valence']}  |  Instrumental: {prefs['target_instrumentalness']}")
    print(f"\n  Top 5 Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(results, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       [{song['genre']} / {song['mood']}]  Energy: {song['energy']}")
        print(f"       Score: {score:.3f}")
        print(f"       Why:   {', '.join(reasons)}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        results = recommend_songs(prefs, songs, k=5)
        print_profile(name, prefs, results)


if __name__ == "__main__":
    main()
