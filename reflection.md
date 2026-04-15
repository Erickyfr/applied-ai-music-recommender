# Reflection: Profile Comparisons

## Chill Lofi vs. High-Energy Pop

These two profiles are opposites in almost every way — one wants calm, acoustic,
instrumental background music; the other wants loud, produced, vocal pop. The
system handled them cleanly. Lofi got Library Rain and Midnight Coding (both
scored ~5.15); Pop got Sunrise City (5.21). There was zero overlap in the top 5
for either profile. This makes sense because genre and mood together account for
3.0 out of a possible 5.3 points — once those two match, the numeric features
just sort within the matched group.

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy (0.85 and 0.90) and low acousticness, so the
numeric features are very similar. What separates them is genre and mood: Pop
wants "happy," Rock wants "intense." Gym Hero (pop/intense) appeared in both top
5 lists — it is an energy match for both but a mood match for neither. This
shows that when a song sits at a genre boundary (Gym Hero could plausibly be
called either pop or workout rock), the system will always surface it for
high-energy seekers regardless of their mood preference. It is not wrong, but
it is a sign that energy can drag songs up even when the categorical fit is weak.

## Deep Intense Rock vs. Conflicted (high energy + sad blues)

Both profiles want high energy (0.90), but one wants rock/intense and the other
wants blues/sad. The rock profile scored Storm Runner at 5.22 — nearly perfect.
The blues profile scored Empty Barstool at 4.59, even though Empty Barstool has
energy=0.30, which is the furthest possible distance from the target of 0.90.
The genre+mood bonus (+3.0) was so powerful it overrode the energy signal
entirely. For the rock user, genre and numeric features pointed in the same
direction. For the blues user, they pointed in opposite directions — and genre
won. This is the clearest example of the system's core bias: category labels
always outweigh how the music actually sounds.

## Omnivore (mid everything) vs. Niche Genre (bossa nova)

The omnivore profile asked for "ambient/chill" with all numeric targets set to
0.5 — the most average possible request. Spacewalk Thoughts won easily on
genre+mood (+3.0) and the results felt fine but uninspiring. No surprises.

The bossa nova profile had no genre match anywhere in the catalog. Without the
+2.0 bonus ever firing, the highest score any song could reach was about 3.0.
Velvet Hours (r&b/romantic) took #1 on a mood match alone. The results were
reasonable — jazz, folk, and reggae are acoustically closer to bossa nova than
rock or metal — but the system found them through energy and acousticness
similarity, not musical knowledge. It worked by accident rather than by design.
This is the most honest demonstration of what content-based filtering cannot do:
it cannot understand musical relationships it was never told about.

## What changed in the weight experiment

Halving the genre weight (2.0 → 1.0) and doubling the energy weight (1.0 → 2.0)
had the most visible effect on the conflicted profile. Empty Barstool still won,
but its lead shrank and the high-energy songs behind it (Storm Runner, Rust and
Thunder) scored much higher than before. For a user whose energy target genuinely
conflicts with their genre, the experimental weights feel more honest — they
surface the contradiction instead of hiding it behind a category bonus. For
typical users with consistent profiles, the change mostly reshuffled positions
2–5 without meaningfully improving results.
