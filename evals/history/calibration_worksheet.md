# Judge calibration worksheet — v4-three-policies

**Protocol:** read each question + reference + agent answer. Score on the rubric below WITHOUT looking at `calibration_key.md`. Fill in `**Your score:**` for each row, then run `python -m eval_harness.calibration` (or use the agreement script). Goal: ≥80% within-one-bucket agreement with the LLM-judge.

**Rubric (single_hop / multi_hop):**
- `1.0` — substantively correct, all key facts captured
- `0.7` — mostly correct, omits a secondary detail or adds extraneous-but-not-wrong content
- `0.4` — partially correct, misstates or omits the central fact
- `0.0` — incorrect, fabricated, or no answer

**Rubric (no_answer):** `1.0` clean refusal · `0.5` partial · `0.0` answers anyway.

**Rubric (ambiguous):** `1.0` surfaces ambiguity · `0.5` notes alternatives but commits · `0.0` silently commits.

## 1. `q001` — `single_hop`

**Question:** What is a guidance law?

**Reference / expected behavior:**

> A guidance law is an algorithm that determines the required commanded missile acceleration.

**Agent answer:**

```
Based on the knowledge base, I can provide you with a clear definition:

## Guidance Law

According to **Section 6.1** of Chapter 6 (Design of Guidance Laws):

> **"The guidance law is the algorithm by which the desired geometrical rule is implemented."**

### Key Characteristics

As described in the textbook:

1. **Control Function**: A guidance law "controls the flight of an object, that is, it presents a controlled input to the moving object" (Section 1.2, Chapter 1)

2. **Command Generation**: The guidance law generates **commanded acceleration** (denoted *a**c***) based on measured information. For example:
   - Proportional Navigation (PN) generates commanded acceleration proportional to the measured line-of-sight (LOS) rate
   - The command acts perpendicular to the instantaneous LOS

3. **Implementation of Geometric Rules**: The classic approach applies guidance laws derived from line-of-sight (LOS) geometrical rules. For instance, the parallel navigation rule requires the LOS rate to equal zero, and PN is the guidance law that implements this rule (Section 2.2, Chapter 2)

4. **Practical Formulation**: The PN guidance law is expressed as:

   *a**c***(t) = *Nv**cl***λ̇

   where *N* is the effective navigation ratio, *v**cl*** is the closing velocity, and λ̇ is the LOS rate

In practical missile systems, the guidance law acts as the interface between the geometric guidance objective (e.g., intercept, rendezvous) and the missile's flight control system that must execute the commanded acceleration.
```

**Your score:** __1.0___    **Notes:** _the agent answer is more rich in information , with comparision ot hte expected answer____

---

## 2. `q002` — `single_hop`

**Question:** What is the first missile system to use the parallel navigation principle, and in what year?

**Reference / expected behavior:**

> The Lark missile, in 1950.

**Agent answer:**

```
The knowledge base does not specifically cover which missile system was the first to use the parallel navigation principle or the year it was first deployed. Related material I found discusses the technical definition of parallel navigation (the "constant bearing" rule where line-of-sight direction remains constant, λ̇(t) = 0) and its implementation through Proportional Navigation (PN) guidance laws, but does not contain historical information about the first weapon system to employ this guidance approach.
```

**Your score:** __0___    **Notes:** _but it does covers this section so why we didnt got the answer , "The parallel navigation principle was first used in the Lark missiles in 1950 [2,3]. So-called proportional navigation (PN) was used to implement parallel navigation. Since that time PN has been used in almost all of the world’s tactical guided missiles. "___

---

## 3. `q005` — `single_hop`

**Question:** What four functions must be achieved to guide and control a missile?

**Reference / expected behavior:**

> Launch, targeting, missile guidance, and flight control.

**Agent answer:**

```
Based on my search of the knowledge base, I found the answer directly in the textbook. According to **Section 1.1 (Introduction)** of **Chapter 1 - Basics of Missile Guidance**, the four functions that must be achieved to guide and control a missile are:

## The Four Functions

1. **The Launch Function** – Monitors the launch events sequence and establishes the initial missile position and velocity after launch.

2. **The Targeting Function** – Establishes the basic geometry between the missile and target and operates in the coordinate system relative to which the missile targeting and guidance must be performed.

3. **The Missile Guidance Function** – Generates guidance commands directing a missile toward the target.

4. **The Flight Control Function** – Converts guidance commands into vehicle response; this function is performed by autopilots. The control actuator of a missile generally consists of thrusters that control the direction of the propulsion subsystem's thrust vector or mechanical devices that move external surfaces of the missile in order to alter the aerodynamic forces acting on it.

---

The text notes that while all four functions are necessary, the **missile guidance function** is the primary focus of the textbook, as the other functions can be considered auxiliary—they create conditions for the guidance function to operate and enable the missile to execute the guidance commands.
```

**Your score:** __1.0___    **Notes:** _____

---

## 4. `q011` — `single_hop`

**Question:** PN guidance is a nonlinear control problem — how is it analyzed using linear techniques, and when is the linearization valid?

**Reference / expected behavior:**

> The system equations are linearized, yielding a linear time-varying system. The linearization is valid when the missile and target are on a near-collision course, close to interception, where the closing velocity can be considered constant and range can be approximated as a linear function of time.

**Agent answer:**

```
This search result directly contains the answer to your question. According to **Section 3.2 (Inertialess PN Guidance System)** of Chapter 3—Analysis of Proportional Navigation Guided Missile Systems in the Time Domain:

## How PN Guidance is Linearized

Although PN guidance presents a **nonlinear control problem**, the system equations are **linearized** to apply known techniques of analysis and design. This linearization yields a **linear time-varying system**.

## When the Linearization is Valid

The linearization is valid under the following conditions:

1. **Collision Course Assumption**: The missile and target approach the so-called **collision course**.

2. **Close to Interception**: The linearized model faithfully represents the guidance system dynamics **close to the interception** point.

3. **Constant Closing Velocity**: Near interception, the **closing velocity can be considered constant**, allowing the range to be approximated by a **linear function of time**.

The textbook notes that simulation results of linear and nonlinear models demonstrate that the linearized model accurately captures the guidance system dynamics under these conditions.

## Practical Implications

The linearized approach enables analytical treatment of the PN guidance problem. For example, with the idealized inertialess model, the analysis shows that choosing an effective navigation ratio **N > 2** guarantees zero miss distance against a step target maneuver. However, the text also cautions that even slightly more complicated linear models (e.g., incorporating first-order autopilot lag) significantly complicate the miss distance analysis, often requiring numerical methods like the method of adjoints to solve the resulting time-varying equations with singularities at the final time *tF*.
```

**Your score:** _1____    **Notes:** _____

---

## 5. `q012` — `single_hop`

**Question:** What is the method of adjoints, and why is it used in missile guidance system analysis?

**Reference / expected behavior:**

> A simulation tool for computing the impulse response of time-varying linear systems at a fixed observation time. It is widely used in missile guidance system design and analysis for linearized engagement models because it allows the system to be simulated for many impulse application times in a single computer run, avoiding multiple simulation trials.

**Agent answer:**

```
Based on the knowledge base, I can provide a comprehensive answer about the method of adjoints and its application in missile guidance analysis.

## What is the Method of Adjoints?

The **method of adjoints** is a mathematical technique for simulating the impulse response **P**(σ, *t*) of time-varying linear systems—specifically for a fixed observation time σ = *t*<sub>F</sub> (final time) with respect to the impulse application time *t* (Section 3.3).

Mathematically, for a linear time-varying system in state-space form:

$$\frac{d\mathbf{y}}{dt} = \mathbf{A}(t_F - t)\mathbf{y} + \mathbf{f}(t)$$

The adjoint system is defined as:

$$\frac{d\mathbf{x}}{dt} = -\mathbf{A}^T(t_F - t)\mathbf{x}$$

where the superscript *T* denotes matrix transposition. The key property is that the adjoint vector **x** satisfies:

$$\mathbf{x}^T(t)\mathbf{y}(t) = \text{constant}$$

To make the adjoint system physically realizable, a **modified adjoint system** is used with time transformation τ = *t*<sub>F</sub> – *t*, running backward from the final time (Section 4.2).

## Why is it Used in Missile Guidance System Analysis?

The method of adjoints is widely used in missile guidance design for several critical reasons:

**1. Linearized Engagement Models**  
Missile guidance problems are inherently nonlinear, but when linearized about a collision course, they become linear time-varying systems. The method of adjoints is particularly well-suited for analyzing these linearized models (Section 3.3).

**2. Miss Distance Computation**  
The primary application is computing the **miss distance** *y*(*t*<sub>F</sub>) due to target maneuvers (such as step acceleration). By setting **x**<sup>T</sup>(*t*<sub>F</sub>) = (1, 0, …, 0) and **f**(*t*) = δ(*t*) (impulse input), the miss distance can be obtained from:

$$y(t_F) = \int_0^{t_F} \mathbf{x}^T(t)\mathbf{f}(t)\,dt$$

**3. Efficiency: Single Simulation Run**  
Without the adjoint method, obtaining the miss step response would require simulating the system response for each impulse application time separately. The adjoint method enables obtaining the complete miss distance response in **one simulation run** by integrating the modified adjoint…
```

**Your score:** __1___    **Notes:** _____

---

## 6. `q017` — `multi_hop`

**Question:** Both PN's optimality result (N=3 giving zero miss) and the linearization used to analyze PN guidance depend on the same physical assumption. What is this shared assumption, and what does it imply for each result?

**Reference / expected behavior:**

> Both depend on the near-collision-course assumption — that the missile approaches the target with constant closing velocity, on a near-collision trajectory, and that missile dynamics can be ignored. For the optimality result, this assumption (plus a non-maneuvering target) is what makes the navigation ratio N=3 minimize the miss-distance cost functional, yielding zero miss. For the linearization, the same assumption is what makes the nonlinear PN guidance equations reduce to a linear time-varying system whose analysis is tractable.

**Agent answer:**

```
Based on the knowledge base, I can now provide a comprehensive answer to your question.

## The Shared Assumption

The shared physical assumption underlying both results is the **near-collision course assumption** (also called the "collision course assumption"). Specifically, this assumes that:
- The missile approaches the target at a **constant closing velocity** (denoted v_cl)
- The approach is **near a collision course**
- The range can be approximated by a **linear function of time**

## What This Assumption Implies for Each Result

### 1. For the Optimality Result (N = 3 giving zero miss)

According to **Section 2.7 ("When is the PN Law Optimal?")**, the near-collision course assumptions allow the equation of motion to be written in a simplified linear form:

$$\ddot{y} = a_T - a_M$$

where y represents the miss distance, a_T is target acceleration, and a_M is missile acceleration.

Under these assumptions, with a performance index (cost functional) that includes both miss distance and energy expenditure:

$$J = \frac{C}{2}y^2(t_F) + \frac{1}{2}\int_0^{t_F} a_M^2(t)dt$$

the optimal solution yields:

$$a_M(t) = \frac{3}{t_F}\dot{y}(t)$$

Taking the limit as C → ∞ (emphasizing zero miss distance), this becomes the PN guidance law with navigation ratio **N = 3**. The key implication is that **N = 3 is the theoretically optimal value that guarantees zero miss distance**—but only under the near-collision course assumptions and when ignoring missile dynamics.

### 2. For the Linearization Used to Analyze PN Guidance

According to **Section 3.2 ("Inertialess PN Guidance System")**, the linearization of the inherently nonlinear PN guidance equations is valid **only when it is assumed that the missile and target approach the so-called collision course**.

The implication here is that:
- The linear time-varying system model "faithfully represents the guidance system dynamics" only in the vicinity of interception
- The linearization remains valid where **the closing velocity can be considered constant**, so that the range can be approximated as r ≈ v_cl(t_F - t)

## Summary

The near-collision course assumption is the foundation for both theoretical results. It enabl…
```

**Your score:** __1___    **Notes:** _____

---

## 7. `q019` — `multi_hop`

**Question:** How does Chapter 7's treatment of sinusoidal target maneuvers differ from Chapter 4's, and why is the Chapter 7 treatment considered more realistic?

**Reference / expected behavior:**

> Chapter 4 treats sinusoidal (weave) target maneuvers as fully deterministic signals — both amplitude and starting time are known. Chapter 7 instead treats the same maneuver as a random process: the sinusoidal amplitude and shape are retained, but the starting time of the maneuver is taken as random (uniformly distributed over the flight time, i.e., random phase). The Chapter 7 framing is more realistic because in actual engagements the missile has no a-priori knowledge of when an evasive maneuver will begin; treating only the deterministic case yields a worst-case miss peak, while the random-phase model gives an rms miss distance that better characterizes expected performance over many engagements.

**Agent answer:**

```
Based on the knowledge base, I can now provide a comprehensive comparison of how Chapter 4 and Chapter 7 treat sinusoidal target maneuvers.

## Key Differences Between Chapter 4 and Chapter 7

### Chapter 4: Deterministic Sinusoidal Maneuvers
In **Section 4.5 (Weave Maneuver Analysis)**, Chapter 4 treats sinusoidal target maneuvers as **deterministic** with known phase. The analysis:
- Focuses on finding the **miss peak** for various flight times $t_F$
- Determines the optimal evasive weave frequency that maximizes steady-state miss distance amplitude
- Provides closed-form solutions for miss distance as a function of navigation ratio, guidance system time constant, natural frequency, and damping ratio
- Represents a "worst-case" deterministic scenario

### Chapter 7: Random-Phase Sinusoidal Maneuvers
In **Section 7.3 (Random Target Maneuvers)** and **Section 7.5**, Chapter 7 treats sinusoidal maneuvers as having **random phase**:
- Models the maneuver as $a_T(t) = a_T \sin(\omega_T t + \phi_T)$, where $\phi_T$ is a **uniformly distributed random variable**
- Uses **shaping filter representations** excited by white noise to model the random nature
- The random-phase sinusoidal maneuver is represented as white noise with power spectral density $\Phi_\phi = a_T^2/t_F$ passing through a shaping filter with transfer function:
$$W_{filter}(s) = \frac{s^2/\omega_T + \omega_T}{s^2 + \omega_T^2}$$
- Derives **RMS miss distance** expressions for statistical analysis

## Why Chapter 7's Treatment Is More Realistic

According to Section 7.3, the Chapter 4 deterministic approach, while "quite realistic" in shape (corresponding to a "barrel roll" strategy), has a critical limitation: **the maneuver starting time is known**. Chapter 7 explicitly states:

> *"A more realistic scenario corresponds to sinusoidal target maneuvers with random starting times of the maneuver, that is, with a random phase."*

The Chapter 7 approach is more realistic because:

1. **Unknown Starting Time**: In real engagements, the target does not announce when it will begin its evasive maneuver—the starting time is uniformly distributed over the flight time.

2. **Statistical Characterization**: Rathe…
```

**Your score:** ___1__    **Notes:** _____

---

## 8. `q022` — `multi_hop`

**Question:** A missile flight has three phases — which guidance law dominates the midcourse phase in endoatmospheric engagements, what does it optimize, and what is the operational significance?

**Reference / expected behavior:**

> A missile flight consists of three phases: boost, midcourse, and homing. Kappa guidance dominates midcourse guidance in the endoatmosphere. It is an optimal guidance law that maximizes the missile's speed at the beginning of the terminal phase of flight, which is essential when engaging targets at far distances or low altitudes — where missile velocity is the prime factor. Kappa is also applied to close-in targets where the time line is critical (the missile must destroy the target before it reaches the minimum range of intercept). The Kappa midcourse algorithm is successfully used in the U.S. Standard Missile 2 (SM2), and is typically deployed alongside proportional navigation, which is used in the homing/terminal phase.

**Agent answer:**

```
According to **Section 8.8 (Kappa Guidance)** of Chapter 8 in the knowledge base:

## Dominant Midcourse Guidance Law
**Kappa guidance** dominates midcourse guidance in the endoatmosphere.

## What It Optimizes
Kappa guidance is an **optimal guidance law that maximizes terminal missile velocity** — specifically, it maximizes missile speed at the beginning of the terminal phase of flight. Mathematically, it solves for optimal coefficients in a guidance law formulation that maximize the terminal value of **v_M** (missile velocity), where the solution takes the form:

- A **proportional term** based on range-to-go vector **r_tgo**
- A **shaping term** incorporating the desired terminal velocity vector **v_PIP**

The optimal values depend on missile parameters including drag, lift factor, thrust, mass, and speed.

## Operational Significance
The operational significance is two-fold:

1. **Long-range/low-altitude engagements**: Against targets at far distance or low altitude, **missile velocity is the prime factor** for mission success. Maximizing terminal velocity ensures the missile retains sufficient kinetic energy and maneuver capability for the terminal homing phase.

2. **Close-in engagements**: For close-in targets, maximizing velocity ensures the **timeline is met** — the missile must destroy the target before it reaches within the minimum range of intercept.

The Kappa algorithm is currently **fielded in the SM2 (U.S. Standard Missile 2)**. It requires knowledge of the predicted intercept point (PIP), and its accuracy depends on estimates of time-to-go and target behavior.
```

**Your score:** __1___    **Notes:** _____

---

## 9. `q024` — `no_answer`

**Question:** How is terminal-phase missile guidance performed in GPS-denied environments using vision-only / camera-based seekers, and what computer-vision techniques are typically used?

**Reference / expected behavior:**

> None

**Agent answer:**

```
Based on my searches, **the knowledge base does not specifically cover GPS-denied terminal-phase guidance using vision-only/camera-based seekers or computer vision techniques.**

The corpus contains extensive material on:
- Terminal-phase guidance using traditional seekers (Section 8.6)
- IR imaging sensors and radar seekers for target tracking
- Filtering and estimation techniques (α,β filters, Kalman filters, extended Kalman filters)
- Proportional navigation and its variants for homing guidance

However, the specific technologies you asked about—GPS-denied environments, vision-only guidance relying solely on camera-based seekers, and computer vision techniques (such as feature detection, optical flow, template matching, or deep learning-based target recognition)—are not addressed in this textbook.

**Related material found discusses:**
- General seeker models with gimballed IR imaging sensors that track targets within their field of view
- Target state estimation using Kalman filters and extended Kalman filters for noisy angle measurements
- The need for range information (from active sensors or off-board sources) to accurately estimate target acceleration when using imaging sensors

But this does not substantively answer your question about GPS-denied vision-only terminal guidance and computer vision methods.
```

**Your score:** __1___    **Notes:** _____

---

## 10. `q030` — `ambiguous`

**Question:** What is the miss distance for my missile guidance system?

**Reference / expected behavior:**

> The system should recognize that miss distance is not a single number — it depends on multiple unspecified factors that the question does not provide — and either ask for the missing context, or surface the parameter dependence. The relevant unspecified factors include: (a) model order — first-order, single-time-constant, or higher-order models give different miss expressions (Ch3, Ch4); (b) input type — step target maneuver, sinusoidal/weave maneuver, or random maneuver each yields a different miss-distance formula (Ch3 §3.2, Ch4 §4.5, Ch7 §7.3); (c) deterministic vs stochastic analysis — peak miss vs rms miss are conceptually different metrics (Ch3-4 vs Ch7); (d) inclusion or exclusion of noise sources such as glint or thermal noise (Ch7 §7.4); (e) which guidance law (PN, APN, Lyapunov-derived, Kappa) is in use. Without these, no single 'miss distance' answer is correct. Silently committing to one (e.g., quoting the §3.2 first-order expression as if it were definitive) without surfacing the parameter dependence is a failure.

**Agent answer:**

```
Your question contains an ambiguity that prevents me from providing a specific numerical answer. When you ask about the **miss distance for "my" missile guidance system**, the calculation depends critically on several system-specific parameters that you have not provided.

According to the knowledge base (Chapter 3 and 4), miss distance is defined as the lateral position error between missile and target at the final time \( t_F \), and its calculation requires:

**Key Parameters Needed:**

1. **Flight Control System Dynamics**
   - System order (first-order, third-order, fourth-order, etc.)
   - Time constant(s) \( \tau \), damping ratio \( \zeta \), natural frequency \( \omega_M \)

2. **Guidance Law Parameters**
   - Navigation ratio \( N \)
   - Effective navigation ratio \( N' \) (if augmented PN)
   - Guidance law type (PN, APN, etc.)

3. **Engagement Geometry**
   - Closing velocity \( V_c \)
   - Flight time \( t_F \) or range-to-go

4. **Disturbance Sources** (for RMS miss distance)
   - Target maneuver characteristics (amplitude, frequency, start time distribution)
   - Noise sources (glint, fading, receiver noise) and their power spectral densities

5. **Seeker Dynamics**
   - Transfer function \( G_2(s) \) representing seeker/autopilot characteristics

**Which interpretation applies to your system?**
- Do you need the **deterministic miss distance** due to a specific target maneuver (e.g., step acceleration)?
- Do you need the **RMS miss distance** due to random target maneuvers and/or noise?
- What is the order of your flight control system model?

Please provide your system parameters so I can guide you through the appropriate calculation using the adjoint method or frequency-domain analysis described in Chapters 3–7.
```

**Your score:** ___1__    **Notes:** _____

---
