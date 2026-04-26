from ai_logic import analyze_user_request

TEST_CASES = [
    ("I am tired and want calm music", "chill"),
    ("I need music for the gym", "happy"),
    ("I need focus music for homework", "chill"),
]

passed = 0

for user_input, expected_mood in TEST_CASES:
    prefs = analyze_user_request(user_input)
    actual_mood = prefs["favorite_mood"]

    if actual_mood == expected_mood:
        result = "PASS"
        passed += 1
    else:
        result = "FAIL"

    print(f"Input: {user_input}")
    print(f"Expected mood: {expected_mood}")
    print(f"Actual mood: {actual_mood}")
    print(f"Result: {result}")
    print("-" * 40)

print(f"Reliability Score: {passed}/{len(TEST_CASES)} tests passed")