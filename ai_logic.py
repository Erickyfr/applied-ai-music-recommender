def analyze_user_request(user_input):
    user_input = user_input.lower()

    if "sad" in user_input or "tired" in user_input or "calm" in user_input:
        return {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "likes_acoustic": True,
            "target_valence": 0.50,
            "target_instrumentalness": 0.70,
        }

    if "happy" in user_input or "hype" in user_input or "workout" in user_input or "gym" in user_input:
        return {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "likes_acoustic": False,
            "target_valence": 0.85,
            "target_instrumentalness": 0.00,
        }

    if "focus" in user_input or "study" in user_input or "homework" in user_input:
        return {
            "favorite_genre": "ambient",
            "favorite_mood": "chill",
            "target_energy": 0.50,
            "likes_acoustic": False,
            "target_valence": 0.60,
            "target_instrumentalness": 0.80,
        }

    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.60,
        "likes_acoustic": False,
        "target_valence": 0.60,
        "target_instrumentalness": 0.20,
    }