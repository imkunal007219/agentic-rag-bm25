# Partial-credit judge calibration — key (judge scores)

## 1. `q003` — run:v4
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly identifies midcourse and terminal/homing phases, but renames 'boost' as 'launch phase,' which is a minor terminological discrepancy from the reference; otherwise the content is substantively correct and well-elaborated.

## 2. `q003` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly identifies midcourse and terminal/homing phases, but labels the first phase 'Launch' instead of 'Boost,' and while the description of an uncontrolled rocket motor boost is consistent with the boost phase, the terminology mismatch is a minor deviation from the reference answer.

## 3. `q004` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=1.00): The system answer correctly captures the core distinction (rendezvous requires both position and velocity matching; intercept requires only position coincidence), but contains a minor error in point 2 under Intercept, stating 'the target velocity should be sufficient to destroy the target' when it should be the missile's terminal velocity, and adds some extraneous elaboration not in the reference.

## 4. `q007` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=1.00): The system answer correctly identifies the collision triangle as the engagement triangle formed by missile position, target position, and the LOS vector, and correctly notes the parallel navigation rule context, but adds substantial extra detail about collinearity conditions and closing velocity that distracts from the core definition, and only briefly implies rather than explicitly states that the LOS direction remains constant under parallel navigation.

## 5. `q009` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=1.00): The system answer correctly identifies N=3 and most key assumptions (constant closing velocity, negligible missile dynamics, near-collision course) but omits the reference's explicit assumption of a non-maneuvering target and planar engagement, and adds extra detail about the quadratic cost functional that, while not wrong, goes beyond the reference.

## 6. `q016` — run:v4
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly and thoroughly explains how PN implements the parallel-navigation principle (LOS rate must be zero, acceleration commanded proportional to LOS rate), but explicitly states it cannot find when PN was first used operationally, omitting the key historical fact that it was first used on the Lark missile in 1950.

## 7. `q016` — run:v5
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly and thoroughly explains how proportional navigation implements the parallel-navigation principle (LOS rate must be zero, acceleration commanded proportional to LOS rate), but explicitly states it cannot find when PN was first used in a missile system, omitting the key historical fact about the Lark missile in 1950.

## 8. `q018` — run:v4
Judge score: **0.2**
Rationale: recall=0.00 of 2 chunks, correctness=0.40: The system answer partially addresses the question by noting frequency-domain methods enable analysis of more general target maneuvers beyond step inputs, but it misses the central facts from the reference: that time-domain analysis fails to yield closed-form analytical expressions for miss distance with high-order, time-varying models, forcing reliance on simulation, and that frequency-domain transfer-function methods solve this by enabling analytical miss-distance expressions and direct bandwidth control.

## 9. `q018` — run:v5
Judge score: **0.75**
Rationale: recall=0.50 of 2 chunks, correctness=1.00: The system answer correctly identifies all key points from the reference: time-domain analysis cannot yield closed-form analytical expressions for miss distance with high-order, time-varying models; designers are forced to rely on simulation (method of adjoints); frequency-domain analysis overcomes this by enabling analytical expressions for miss distance with higher-order models; and it gives designers control over system bandwidth.

## 10. `q020` — run:v4
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly captures the two core additions identified in the reference—(1) |Q̇| as a performance index for comparing/creating guidance laws and (2) extension to maneuvering targets via a stability framework—but embeds them amid substantial extra material (impact-angle constraints, nonlinear corrections, 3D treatment, correction-term decomposition) that goes well beyond the reference and risks distorting the focus, and it incorrectly implies Chapter 2 itself already uses a Lyapunov approach rather than a control-problem formulation that the Lyapunov treatment in Chapter 5 then reframes.

## 11. `q020` — run:v5
Judge score: **0.2**
Rationale: recall=0.00 of 2 chunks, correctness=0.40: The system answer correctly identifies that Chapter 5 adds a comparison criterion via the Lyapunov function derivative module and a design methodology for creating new guidance laws, but it mischaracterizes Chapter 2 as an inverse optimal control derivation (minimizing a quadratic cost) rather than a control-problem formulation using LOS angle/derivative as state variables, and critically omits the reference's key point that the Lyapunov treatment extends naturally to maneuvering targets, enabling augmented PN and other modifications to be derived as stability solutions rather than ad-hoc extensions.

## 12. `q022` — run:v4
Judge score: **0.75**
Rationale: recall=0.50 of 2 chunks, correctness=1.00: The system answer correctly identifies Kappa guidance as the dominant midcourse law in endoatmospheric engagements, accurately states it optimizes terminal missile velocity, covers all operational significance points (far/low-altitude targets, close-in timeline criticality, SM2 deployment), and even adds appropriate technical detail about the guidance law formulation without contradicting the reference.

## 13. `q022` — run:v5
Judge score: **0.75**
Rationale: recall=0.50 of 2 chunks, correctness=1.00: The system answer correctly identifies Kappa guidance as dominating the endoatmospheric midcourse phase, accurately states it optimizes terminal missile velocity, covers both operational scenarios (long-range/low-altitude and close-in targets), and confirms the SM2 implementation, matching all key facts in the reference answer with additional technical detail.

## 14. `q029` — run:v4
Judge score: **0.5**
Rationale: The response correctly surfaces multiple interpretations (PN with N=3 and Kappa guidance) and explicitly states there is no single optimal law, but it misses three of the five distinct senses described in the expected behavior — Lyapunov-based optimality (Ch5), neoclassical guidance optimality (Ch6), and integrated guidance-and-control optimality (Ch9) — making it a partial but incomplete treatment of the ambiguity.

## 15. `q029` — run:v5
Judge score: **0.5**
Rationale: The response correctly surfaces multiple senses of 'optimal' (PN with N=3, Kappa guidance, and general optimal control) and avoids silently committing to one, but it misses several interpretations described in the expected behavior — specifically Lyapunov-based guidance (Ch5 §5.3), neoclassical guidance and its counterintuitive failure mode (Ch6 §6.2), and integrated guidance-and-control design (Ch9 §9.3) as distinct senses of optimality.

## 16. `q030` — run:v4
Judge score: **0.5**
Rationale: The response surfaces several relevant dimensions of ambiguity (stochastic vs. deterministic, noise sources, airframe factors, input types) and ends with a clarifying question, but it presents this as a 'comprehensive explanation' rather than explicitly flagging that the question is unanswerable without more specifics, and it omits key parameter dependencies like guidance law choice (PN vs. APN vs. Kappa) and model order (first-order vs. higher-order), while implicitly treating the listed factors as an exhaustive tutorial rather than as reasons why no single miss distance can be given.

## 17. `q034` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=1.00): The system answer correctly identifies electromagnetic wave refraction from a nonhemispheric radome as the cause and correctly states it has a destabilizing effect on the guidance loop, but the explanation for why it is worse at high altitudes is speculative/indirect rather than simply stating the established fact, and the extra technical detail about coupling mechanisms, though not wrong, goes beyond what the reference confirms.

## 18. `q035` — run:v4
Judge score: **0.25**
Rationale: recall=0.50 of 2 chunks, correctness=0.00: The system failed to produce any answer, returning only an error message about exceeding maximum turns, so no relevant information was provided.

## 19. `q035` — run:v5
Judge score: **0.5**
Rationale: recall=1.00 of 2 chunks, correctness=0.00: The system failed to produce any answer, returning only an error message about exceeding maximum turns, so no relevant information was conveyed.

## 20. `q036` — run:v4
Judge score: **0.75**
Rationale: recall=0.50 of 2 chunks, correctness=1.00: The system answer correctly identifies the core distinction: deterministic weaving yields a peak/worst-case miss distance via frequency-domain analysis, while the random-phase sinusoidal maneuver is treated stochastically (modeled as white noise through a shaping filter) to yield RMS miss distance, matching all key facts in the reference answer.

## 21. `q036` — run:v5
Judge score: **0.6**
Rationale: recall=0.50 of 2 chunks, correctness=0.70: The system answer correctly identifies the core distinction—deterministic weaving yields a peak miss distance via frequency response analysis while random-phase sinusoidal maneuver yields an RMS miss distance treated statistically—matching the reference's central claim, but it cites different section numbers (4.5, 7.3, 7.7) than the reference (Ch6 Section 6.4, Ch7 Section 7.5) and adds numerous specific numerical details and equations that appear fabricated, which distracts without being definitively wrong on the main concept.

## 22. `q046` — run:v4
Judge score: **0.7**
Rationale: correctness=0.70 (recall=1.00): The system answer correctly identifies Ixz = 0 due to symmetry about both xy and xz planes as the key simplification, but it overstates by claiming all three products of inertia vanish specifically due to cruciform symmetry (Ixy and Iyz would vanish for any planar-symmetric body, not just cruciform), and it omits the reference's secondary point about further simplification when Iyy = Izz for circular cross-sections.

## 23. `q050` — run:v4
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly captures the core BIBO stability definition and the key analytical condition (absolute integrability of inverse Laplace transform, analyticity in right half-plane, limit at infinity equals zero) matching the reference, but adds a specific inequality formula (equation 4.64) and corollary that appear to be additional fabricated or extraneous details not present in the reference answer, which distracts from the main result.

## 24. `q050` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly captures the core BIBO stability conditions (bounded miss distance, analyticity in the right half-plane, and lim P(tF,s)=0 as s→∞) and the absolute integrability requirement, but adds a specific algebraic condition with parameters Bk, Cj, τk, ωj, ζj that appears to be additional detail not present in the reference answer, which slightly distracts while not being outright wrong given it may reflect the textbook's more detailed theorem.

## 25. `q051` — run:v4
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly defines the miss step response as miss distance due to a step target maneuver and explains its importance for evaluating PN guidance systems, but omits the reference's key point that closed-form time-domain solutions exist only for simple models and not for high-order systems with realistic autopilot and airframe dynamics, while adding substantial correct but extraneous frequency-domain detail not emphasized in the reference.

## 26. `q051` — run:v5
Judge score: **0.7**
Rationale: correctness=0.70 (recall=0.00): The system answer correctly identifies the miss step response as miss distance due to a step target maneuver and explains its importance for evaluating PN guidance systems, but it adds extensive technical detail (frequency-domain integrals, bandwidth rules, adjoint methods) not present in the reference, and omits the reference's key point that closed-form time-domain solutions exist only for simple models, not high-order ones with realistic autopilot and airframe dynamics.

## 27. `q052` — run:v4
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly captures the core connection—inertialess case is the ideal baseline (zero miss for N>2) and the first-order system introduces finite rms miss due to lag—but adds substantial extra detail (adjoint method, specific equation numbers, glint noise counter-intuitive behavior) that goes well beyond the reference, and the final quoted claim that 'first-order system analysis gives a significantly lower miss estimate than a more realistic model' slightly contradicts the reference's implication that the first-order model yields higher/finite miss versus the ideal.

## 28. `q052` — run:v5
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly identifies the core connection—inertialess PN gives zero miss for N>2 as the idealized baseline, while the first-order system introduces a flight-control time constant making rms miss finite and dependent on τ and flight time—but adds considerable extraneous detail (glint noise formulas, tables, counter-intuitive τ behavior) that goes well beyond the reference and risks distraction, while not misstating the central facts.

## 29. `q053` — run:v5
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly captures the Lyapunov approach as a stabilization method ensuring negative definiteness of the Lyapunov function derivative and the Bellman approach as an optimization over a cost functional, but omits the reference's specific emphasis on 'partial stability of the LOS rate' for Lyapunov and the 'state-dependent Riccati equation' coupling guidance and control for the Bellman approach, while adding substantial extra detail not in the reference.

## 30. `q054` — run:v4
Judge score: **0.45**
Rationale: recall=0.50 of 2 chunks, correctness=0.40: The system answer correctly identifies that the commanded acceleration must be decomposed into components relative to the velocity vector and body axis, but it misses the central fact from the reference: that the key extra step is determining the angle of attack (via aerodynamic coefficient regression models) to resolve the commanded acceleration onto body axes — the iterative step that distinguishes the 3-DOF implementation from the idealized PN derivation.

## 31. `q055` — run:v4
Judge score: **0.6**
Rationale: recall=0.50 of 2 chunks, correctness=0.70: The system answer correctly captures the core mechanism—neoclassical guidance zeroes out the target-maneuver response P_T, which eliminates receiver noise contributions, while glint noise enters through a different transfer function that is not nullified—but adds equation-level technical detail (some of which may be fabricated or imprecise) and slightly mischaracterizes the glint mechanism by framing it as P_g → 1 for long flight times rather than simply stating glint's miss contribution does not vanish as flight time increases.

## 32. `q056` — run:v4
Judge score: **0.85**
Rationale: recall=1.00 of 2 chunks, correctness=0.70: The system answer correctly describes the geometric relationship between LOS angles and seeker gimbal angles and mentions the body-frame transformation implicitly, but omits the explicit intermediate step highlighted in the reference—that the LOS direction is first transformed into the missile body frame via body Euler angles before the seeker gimbal rotations are applied—and also omits the mention of radome refraction as a real-effect added in Chapter 8.

## 33. `q056` — run:v5
Judge score: **0.5**
Rationale: recall=1.00 of 2 chunks, correctness=0.00: The system produced no answer at all (agent timeout), so it fails to address any aspect of the question.

## 34. `q060` — run:v4
Judge score: **0.5**
Rationale: The system correctly recognizes ambiguity and asks for clarification, but it conflates actuator and autopilot time constants into a single 'flight control system' category, misses the seeker time constant as a distinct sense, and then commits to specific numerical values (τ = 0.5 s from Ch4's flight-control model) without surfacing the autopilot lag, seeker, and actuator time constants from Ch8 as separate, distinct interpretations as required by the expected behavior.

## 35. `q060` — run:v5
Judge score: **0.5**
Rationale: The system does ask for clarification and surfaces some ambiguity around the flight-control time constant τ, but it silently commits to the Ch3-4 first-order guidance/flight-control time constant without acknowledging the other distinct senses described in the expected behavior: the autopilot lag time constant, the seeker time constant, and the actuator time constant from Ch8 models.
