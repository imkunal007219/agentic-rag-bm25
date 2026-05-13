# Judge calibration key — v4-three-policies

DO NOT OPEN until worksheet is filled in.

## 1. `q001` — `single_hop`
- Judge score: **1.00**
- Judge rationale: correctness=1.00 (recall=0.00): The system answer correctly identifies the guidance law as an algorithm (matching the reference), explicitly states it generates commanded acceleration, and provides accurate additional context about geometric rules and PN implementation without contradicting the reference.

## 2. `q002` — `single_hop`
- Judge score: **0.00**
- Judge rationale: correctness=0.00 (recall=0.00): The system answer fails to provide any answer to the question, stating the information is not in its knowledge base, while the correct answer (Lark missile, 1950) was expected.

## 3. `q005` — `single_hop`
- Judge score: **1.00**
- Judge rationale: correctness=1.00 (recall=1.00): The system answer correctly identifies all four functions—launch, targeting, missile guidance, and flight control—matching the reference answer exactly, and provides additional accurate elaboration on each function.

## 4. `q011` — `single_hop`
- Judge score: **1.00**
- Judge rationale: correctness=1.00 (recall=1.00): The system answer captures all key facts from the reference—linearization of system equations yielding a linear time-varying system, validity on a near-collision course close to interception with constant closing velocity and range as a linear function of time—and adds appropriate but non-contradictory extra context.

## 5. `q012` — `single_hop`
- Judge score: **1.00**
- Judge rationale: correctness=1.00 (recall=1.00): The system answer correctly identifies the method of adjoints as a simulation tool for computing impulse responses of time-varying linear systems at a fixed observation time, explains its use for linearized engagement models, and explicitly states the key efficiency benefit of obtaining results for many impulse application times in a single simulation run—capturing all central facts from the reference with additional correct technical detail.

## 6. `q017` — `multi_hop`
- Judge score: **1.00**
- Judge rationale: recall=1.00 of 2 chunks, correctness=1.00: The system answer correctly identifies the near-collision course assumption as the shared foundation, accurately explains its implications for both the N=3 optimality result (constant closing velocity, non-maneuvering target, tractable linear form enabling optimal control derivation) and the linearization (reducing nonlinear PN equations to a linear time-varying system), and notes that missile dynamics are ignored—matching all key facts in the reference answer.

## 7. `q019` — `multi_hop`
- Judge score: **1.00**
- Judge rationale: recall=1.00 of 2 chunks, correctness=1.00: The system answer accurately captures all key facts from the reference: Chapter 4 treats the maneuver deterministically with known phase/starting time, Chapter 7 treats starting time as random (uniformly distributed), the Chapter 7 approach yields RMS miss distance versus worst-case peak miss, and the realism argument centers on the missile having no a-priori knowledge of when the maneuver begins—with additional correct technical detail about shaping filters that goes beyond but does not contradict the reference.

## 8. `q022` — `multi_hop`
- Judge score: **1.00**
- Judge rationale: recall=0.50 of 2 chunks, correctness=1.00: The system answer correctly identifies Kappa guidance as the dominant midcourse law in endoatmospheric engagements, accurately states it optimizes terminal missile velocity, covers both operational significance cases (long-range/low-altitude and close-in timelines), and correctly cites the SM2 deployment, matching all key facts in the reference answer.

## 9. `q024` — `no_answer`
- Judge score: **1.00**
- Judge rationale: The system explicitly states the knowledge base does not cover GPS-denied vision-only guidance or computer vision techniques, accurately describes what related material is present, and avoids fabricating any answer to the out-of-corpus question.

## 10. `q030` — `ambiguous`
- Judge score: **1.00**
- Judge rationale: The system response explicitly recognizes the ambiguity, surfaces all major parameter dependencies (model order, guidance law type, deterministic vs. stochastic analysis, noise sources, seeker dynamics), and asks clarifying questions rather than silently committing to one interpretation.
