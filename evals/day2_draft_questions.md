# Day 2 draft questions — q031 to q040

Drafted from Ch5-9 of the missile-guidance corpus. **Not yet appended to
`groundtruth.jsonl`** — review each row, edit as needed, then I'll merge
the approved rows into the dataset and re-run the eval to recompute
pass-rate baselines on the expanded set.

## Review checklist per row

- [ ] Question phrasing reads like a real user, not a textbook header
- [ ] `expected_answer` is concise and factually anchored in the corpus
- [ ] `expected_chunks` matches actual section headings (verified against `## **X.Y SECTION**` lines)
- [ ] `question_type` matches the failure mode the row is meant to probe
- [ ] `notes` records *why* the row was included

## Spread

| Chapter | Hits |
|---|---|
| Ch5 | q031, q035, q040 |
| Ch6 | q032, q035, q036 |
| Ch7 | q033, q036 |
| Ch8 | q034, q037, q040 |
| Ch9 | q037 (only) |

Ch9 only appears in one multi-hop row. Consider replacing one row with a
Ch9-specific single-hop on §9.3 SYNTHESIS OF CONTROL LAWS (integrated
guidance-and-control law derivation) if Ch9 coverage feels light.

## Distribution

4 single_hop · 3 multi_hop · 2 no_answer · 1 ambiguous — matches the
authoring brief.

## Known fragile rows

- **q032** references equation 6.14 specifically. If the chunker doesn't
  surface equation numbers cleanly, this becomes a hard row. The prose
  around the equation (Re[W(iω)] frequency-domain condition) still
  carries the answer, so the row is valid but expect lower correctness
  than the easier single-hop rows.
- **q039** assumes "SM-3" appears at least in passing in Ch8. Not
  independently verified yet — grep before final append. If SM-3 is
  absent, the row is still a valid no_answer, just less
  keyword-match-but-no-answer-flavored.

## Raw JSONL — paste into `groundtruth.jsonl` after approval

```jsonl
{"id":"q031","question":"In the Lyapunov guidance law, what's the point of adding the cubic term in LOS rate? How does it help vs regular PN?","expected_answer":"The cubic term creates a variable gain that is larger when the LOS rate is large and smaller when it is small. This allows faster reduction of LOS rate when needed while reducing noise sensitivity and avoiding excessive gain when the LOS rate is already small.","expected_chunks":["05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN"],"question_type":"single_hop","notes":"Probes understanding of the specific nonlinear modification (cubic term) derived via Lyapunov, distinct from standard PN linearity."}
{"id":"q032","question":"For pseudoclassical guidance, what condition does the new transfer function need to satisfy to actually give smaller peak miss than PN?","expected_answer":"The integral from 0 to infinity of (Re[W(iω)] − Re[W_Σ(iω)])/ω² dω must be positive (equation 6.14), or equivalently Re[W_Σ(iω)] > Re[W(iω)] over the relevant frequency band.","expected_chunks":["06-Chapter-6---Design-of-Guidance-Laws.md#6.3 PSEUDOCLASSICAL MISSILE GUIDANCE"],"question_type":"single_hop","notes":"Tests recall of the frequency-domain condition (eq 6.14) for miss reduction in the pseudoclassical framework. Fragile if chunker drops equation numbers."}
{"id":"q033","question":"Why do Kalman filters struggle with glint noise in radar seekers?","expected_answer":"Glint noise is non-Gaussian (heavy-tailed) and can be highly correlated, whereas the Kalman filter assumes Gaussian, white perturbations. The mismatch degrades the filter's estimate.","expected_chunks":["07-Chapter-7---Guidance-Law-Performance.md#7.4 ANALYSIS OF INFLUENCE OF NOISES ON MISS DISTANCE"],"question_type":"single_hop","notes":"Checks recognition of filter-vs-noise assumption mismatch."}
{"id":"q034","question":"What causes the radome effect and why is it worse at high altitudes?","expected_answer":"A nonhemispheric radome refracts incoming electromagnetic waves, causing aberration of the measured LOS angles. The aberration has a destabilizing effect on the guidance loop, and the effect is more severe at high altitudes.","expected_chunks":["08-Chapter-8---Testing-Guidance-Laws.md#8.6 SEEKER MODEL"],"question_type":"single_hop","notes":"Hardware/aero question — tests seeker model recall."}
{"id":"q035","question":"How does adding a cubic term to the Lyapunov guidance law compare to using it in the pseudoclassical method? Do they achieve the same thing?","expected_answer":"Both approaches add a nonlinear cubic term in LOS rate to improve on standard PN, but their derivation is different: the Lyapunov approach derives the cubic term from stability conditions in the time domain (§5.3), while the pseudoclassical approach uses it as part of frequency-domain feedforward/feedback compensation to improve miss distance (§6.4). The mechanism is the same modification, the framing is different.","expected_chunks":["05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN","06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS"],"question_type":"multi_hop","notes":"Requires connecting the same nonlinear modification across two different theoretical frameworks (time-domain Lyapunov vs frequency-domain pseudoclassical)."}
{"id":"q036","question":"What's the difference between miss distance for a deterministic weaving target versus a random-phase sinusoidal maneuver?","expected_answer":"Deterministic weaving uses the frequency response magnitude to find peak miss distance (Ch6 §6.4), while a random-phase sinusoidal maneuver is treated as white noise through a shaping filter, yielding RMS miss distance (Ch7 §7.5). One is a peak metric, the other is a statistical one.","expected_chunks":["06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS","07-Chapter-7---Guidance-Law-Performance.md#7.5 EFFECT OF RANDOM TARGET MANEUVERS ON MISS DISTANCE"],"question_type":"multi_hop","notes":"Contrasts deterministic frequency-domain analysis with stochastic treatment of similar maneuver geometry."}
{"id":"q037","question":"How does the traditional 6-DOF simulation structure differ from the integrated guidance-and-control architecture?","expected_answer":"The 6-DOF model uses a sequential architecture where guidance and autopilot are designed separately and connected in series (Ch8 §8.9.1). The integrated architecture combines them into a unified system with coupled state variables and joint feedback (Ch9 §9.2).","expected_chunks":["08-Chapter-8---Testing-Guidance-Laws.md#8.9.1 6-DOF SIMULATION MODEL","09-Chapter-9---Integrated-Missile-Design.md#9.2 INTEGRATED MISSILE GUIDANCE AND CONTROL MODEL"],"question_type":"multi_hop","notes":"Compares the modular sequential design of Ch8 with the unified integrated approach of Ch9."}
{"id":"q038","question":"What machine learning techniques are used for target classification in the seeker algorithms here?","expected_answer":null,"expected_chunks":[],"question_type":"no_answer","notes":"Plausibly modern but Ch5-9 only discuss Kalman and alpha-beta filters — no ML. Tests hallucination resistance on a topic the agent is likely to want to find."}
{"id":"q039","question":"How does the SM-3 interceptor perform boost-phase discrimination using multi-spectral seekers?","expected_answer":null,"expected_chunks":[],"question_type":"no_answer","notes":"Even if SM-3 is mentioned in passing, boost-phase discrimination via multi-spectral seekers is not covered. Tests refusal when there's a partial keyword match."}
{"id":"q040","question":"What does the shaping term do in missile guidance?","expected_answer":"The system should recognize that 'shaping term' is overloaded in this corpus and surface the alternatives. In Chapter 5 (Lyapunov guidance, §5.3) it refers to N₂·r̈·λ, a correction term acting along the LOS to shape the trajectory; in Chapter 8 (Kappa guidance, §8.8) it refers to K₂·(v_PIP − v_M), the term shaping trajectory toward a desired terminal velocity vector. Silently committing to one without surfacing the multiplicity is a failure.","expected_chunks":[],"question_type":"ambiguous","notes":"Term-overload ambiguity. 'Shaping term' has distinct meanings in §5.3 (Lyapunov) vs §8.8 (Kappa). Tests whether the agent recognizes a single technical term carrying two distinct senses within the same corpus."}
```
