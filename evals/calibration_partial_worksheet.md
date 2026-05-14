# Partial-credit judge calibration — worksheet

Blind hand-grade. Rubric buckets:
- single_hop / multi_hop: 0.0 / 0.4 / 0.7 / 1.0
- no_answer / ambiguous: 0.0 / 0.5 / 1.0

Fill **Your score:** for each row. Do not consult the judge key.

## 1. `q003` — `single_hop` — run:v4 — [CLEAN]

**Question:** What are the three phases of missile flight?

**Reference answer:** Boost, midcourse, and homing.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS']

**Agent answer:**

According to **Section 8.1 (Introduction)** of Chapter 8 (Testing Guidance Laws), the three phases of missile flight for engagement and interception are:

## 1. Launch Phase
The first phase is usually **uncontrolled**. During this stage, the rocket motor is initiated and the missile is boosted up to its operating velocity in the direction of a target.

## 2. Midcourse Phase
This phase follows the launch phase **if the missile is not locked onto the target**. During midcourse, the missile is typically guided by radar into an area that allows it to lock onto the target with its own onboard sensor.

## 3. Terminal (Homing) Guidance Phase
During this phase, the missile is guided onto the target using its **local sensor measurements**. Depending on the interceptor and mission, the terminal phase can begin anywhere from tens of seconds down to a few seconds before intercept. The purpose of this phase is to remove residual errors accumulated during prior phases and ultimately reduce the final miss distance below a specified level. Near the end of the terminal phase (often called the "endgame"), the interceptor may need to maneuver at maximum capability to hit fast-moving, evasive targets.

---

This three-phase structure applies broadly across missile types, including both aerodynamic missiles and ballistic missiles. The terminal phase is particularly critical as it demands high accuracy and quick reaction capability from the guidance system.

**Your score:** 1.0

---

## 2. `q003` — `single_hop` — run:v5 — [CLEAN]

**Question:** What are the three phases of missile flight?

**Reference answer:** Boost, midcourse, and homing.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS']

**Agent answer:**

According to **Section 8.1 (Introduction)** of Chapter 8 (Testing Guidance Laws), the three phases of missile flight are:

## 1. Launch Phase
The first phase is usually **uncontrolled**. During this stage, the rocket motor is initiated and the missile is boosted up to its operating velocity in the direction of a target.

## 2. Midcourse Phase
This phase follows the launch phase **if the missile is not locked onto the target**. Usually, during this phase the missile is guided by radar into an area that allows it to lock onto the target with its own sensor.

## 3. Terminal (Homing) Guidance Phase
During this phase, the missile is guided onto the target using its **local sensor measurements**. Key characteristics include:
- The terminal phase can begin anywhere from **tens of seconds down to a few seconds before intercept**
- Its purpose is to remove the residual errors accumulated during the prior phases and ultimately reduce the final distance between the interceptor and threat below some specified level
- For systems with a fuze and fragmentation warhead, the final miss distance must be less than the warhead lethal radius; direct-hit missiles can tolerate only very small misses
- Near the very end of the terminal phase (often called the **"endgame"**), the interceptor may be required to maneuver to maximum capability to converge on and hit a fast-moving evasive target

**Your score:** 1.0

---

## 3. `q004` — `single_hop` — run:v5 — [CLEAN]

**Question:** What is the difference between rendezvous and intercept in guidance?

**Reference answer:** Rendezvous requires the object's velocity to equal the target's velocity at the meeting point; intercept requires only that the missile's position coincide with the target's position at some moment, with sufficient terminal velocity to destroy the target.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS']

**Agent answer:**

According to **Section 1.2** of the textbook (*Basics of Missile Guidance*), the difference between rendezvous and intercept is defined by the velocity matching requirement:

## Rendezvous
**Rendezvous** is guidance where an object's position coincides with the target's position **and** the object's velocity equals the target's velocity. This represents a "soft" matching condition where both position and velocity vectors must align at the point of encounter.

## Intercept (as applied to missiles)
**Intercept** guidance, used for missile applications, requires that at a certain moment in time:
1. The missile's position coincides with the target's position
2. The **target velocity should be sufficient to destroy the target**

The key distinction is that intercept does **not** require velocity matching between the missile and target. Instead, the encounter conditions only need to satisfy the lethality requirement—typically implying a high closing velocity that enables warhead effectiveness. This is in contrast to rendezvous scenarios (such as spacecraft docking or vessels meeting at sea) where relative velocity must be near-zero at contact.

**Your score:** 0.7

---

## 4. `q007` — `single_hop` — run:v5 — [CLEAN]

**Question:** What is the collision triangle in parallel-navigation geometry?

**Reference answer:** The triangle in the planar engagement geometry formed by the missile position, the target position, and the line-of-sight between them. Under the parallel-navigation rule the LOS direction remains constant, so the missile and target are on intercept trajectories.

**Expected chunks:** ['02-Chapter-2---Parallel-Navigation.md#2.1 INTRODUCTION']

**Agent answer:**

Based on Section 2.1 of Chapter 2 (Parallel Navigation), the **collision triangle** is the engagement triangle formed when the parallel navigation rule is satisfied.

As shown in Figure 2.1 of the text, the collision triangle consists of:
- The missile position (M) and target position (T)
- The velocity vectors of both the missile (**v**_M) and target (**v**_T)
- The line-of-sight (LOS) vector and range vector (**r**)

For the triangle to be a "collision triangle," two conditions must be satisfied:

1. **Collinearity condition**: The range rate vector **ṙ** must be collinear with the range vector **r**, meaning the vectors **r**(t), **v**_M(t), and **v**_T(t) are instantaneously coplanar. This is expressed by equation (2.3):
   - **ṙ** = −v_cl·**λ** (where v_cl > 0 is the closing velocity)

2. **Negative range rate**: The closing velocity must be positive (ṙ < 0), meaning the distance between missile and target is decreasing.

The geometry also involves:
- The **lead angle** (δ) — the angle between the missile velocity vector and the LOS
- The **aspect angle** (180° − θ) — related to the target velocity vector orientation
- The **LOS angle** (λ) — measured with respect to a horizontal reference

When these conditions are met and the target is non-maneuvering with constant speeds, the missile can intercept the target by moving in a straight line — this is the collision course depicted by the collision triangle.

**Your score:** 0.7

---

## 5. `q009` — `single_hop` — run:v5 — [CLEAN]

**Question:** Under what assumptions does the PN law become an optimal control solution, and what navigation ratio guarantees zero miss distance under those assumptions?

**Reference answer:** Under near-collision-course assumptions — constant closing velocity, planar engagement, missile dynamics ignored, and a non-maneuvering target. Under these conditions, an optimal navigation ratio of N = 3 guarantees zero miss distance.

**Expected chunks:** ['02-Chapter-2---Parallel-Navigation.md#2.7 WHEN IS THE PN LAW OPTIMAL?']

**Agent answer:**

Based on my reading of **Section 2.7 "WHEN IS THE PN LAW OPTIMAL?"** in Chapter 2 (Parallel Navigation), I can provide you with the complete answer:

## Assumptions Under Which PN Becomes Optimal

The PN law becomes an optimal control solution under the following **near-collision course assumptions**:

1. **Constant closing velocity** ($v_{cl}$): The missile approaches the target at a constant closing velocity
2. **Near-collision course**: The engagement geometry is close to a collision course
3. **Negligible missile dynamics**: Missile dynamics are ignored (instantaneous response to acceleration commands)

Under these assumptions, PN minimizes a quadratic performance index (cost functional) of the form:

$$J = \text{[miss distance]} + C \int_0^{t_F} a_M^2 \, dt$$

where $C$ is a weighting factor that trades off between minimizing miss distance and minimizing energy expenditure during the flight.

## Navigation Ratio for Zero Miss Distance

The **navigation ratio $N = 3$** guarantees zero miss distance under these assumptions.

As stated in the text: *"Zero miss corresponds to $C \to \infty$"* (meaning miss distance is the sole priority), *"so that the optimal guidance law becomes"* the PN law with $N = 3$.

**Important caveat:** The text notes that by ignoring missile dynamics and considering a nonmaneuvering target, the problem is excessively simplified, so this result has "pure" theoretical rather than practical importance. More realistic guidance problems with missile dynamics and maneuvering targets require more sophisticated approaches.

**Your score:** 0.7

---

## 6. `q016` — `multi_hop` — run:v4 — [CLEAN]

**Question:** How does proportional navigation implement the parallel-navigation principle, and when was it first used in a real missile system?

**Reference answer:** Parallel navigation requires that the line-of-sight (LOS) direction between missile and target remain constant — i.e., the LOS rate must be zero. Proportional navigation implements this principle by commanding a missile acceleration proportional to the measured LOS rate; when the LOS rate is non-zero, the acceleration command drives it toward zero. PN was first used in a missile system on the Lark missile in 1950, and has since been used in almost all of the world's tactical guided missiles.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS', '02-Chapter-2---Parallel-Navigation.md#2.2 PROPORTIONAL NAVIGATION. PLANAR ENGAGEMENT']

**Agent answer:**

Based on my searches, I can provide a complete answer to the first part of your question, but the knowledge base does not contain specific information about when proportional navigation was first used in a real missile system.

## How Proportional Navigation Implements Parallel Navigation

According to **Section 2.2** and **Section 2.5** of Chapter 2 (Parallel Navigation), proportional navigation (PN) implements the parallel-navigation principle as follows:

**The Core Philosophy:**
The parallel-navigation rule (also called "constant bearing") requires that the line-of-sight (LOS) direction relative to the inertial coordinate system remains constant—that is, the LOS stays parallel to its initial direction throughout the engagement. Mathematically, this means the LOS rate λ̇ must equal zero.

**PN Implementation:**
Since in reality the LOS rate differs from zero, PN creates a guidance command that is proportional to the LOS rate deviation from zero, with the goal of driving the LOS rate toward zero. The commanded acceleration is given by:

$$a_c(t) = N \cdot v_{cl} \cdot \dot{\lambda}$$

Where:
- **N** is the effective navigation ratio (dimensionless constant)
- **v_cl** is the closing velocity (negative range rate)
- **λ̇** is the LOS rate

**From a Control Theory Perspective (Section 2.5):**
PN can be formally derived as a control law that guarantees asymptotic stability of the missile-target engagement system with respect to the LOS rate. Using Lyapunov stability theory with the Lyapunov function chosen as the square of the LOS derivative:

$$Q = c \cdot \dot{\lambda}^2$$

The control law that ensures asymptotic stability (lim λ̇ → 0 as t → ∞) takes the form:

$$u = k \cdot \dot{\lambda}$$

where k > 2v_cl, which when expressed in terms of the navigation ratio N gives the standard PN law.

**First Use in Operational Missile Systems:**
The knowledge base does not specifically cover when proportional navigation was first used in a real missile system. The material discusses that PN "is the most widely used law in practice" and describes its implementation in tactical radar homing missiles and infrared missiles, but does not provide historical dates or identify the first operational system to employ this guidance law.

**Your score:** 0.4

---

## 7. `q016` — `multi_hop` — run:v5 — [CLEAN]

**Question:** How does proportional navigation implement the parallel-navigation principle, and when was it first used in a real missile system?

**Reference answer:** Parallel navigation requires that the line-of-sight (LOS) direction between missile and target remain constant — i.e., the LOS rate must be zero. Proportional navigation implements this principle by commanding a missile acceleration proportional to the measured LOS rate; when the LOS rate is non-zero, the acceleration command drives it toward zero. PN was first used in a missile system on the Lark missile in 1950, and has since been used in almost all of the world's tactical guided missiles.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS', '02-Chapter-2---Parallel-Navigation.md#2.2 PROPORTIONAL NAVIGATION. PLANAR ENGAGEMENT']

**Agent answer:**

Based on my reading of the full sections, I can answer the first part of your question. The knowledge base does not contain specific information about when proportional navigation was first used in a real missile system.

---

## How Proportional Navigation Implements Parallel Navigation

According to **Section 2.2** and **Section 2.5** of the Parallel Navigation chapter, proportional navigation (PN) implements the parallel-navigation principle as follows:

### The Parallel Navigation Rule
The parallel navigation rule (also called "constant bearing") requires that the **line-of-sight (LOS) direction relative to the inertial coordinate system be kept constant**, meaning the LOS rate must equal zero (λ̇(t) = 0) with the additional requirement that the range rate is negative (ṙ(t) < 0) to ensure the missile is closing on the target (**Section 2.1**).

### Implementation Through PN
Proportional navigation implements this rule through a control philosophy based on physical intuition: **missile acceleration should nullify the LOS rate** (**Section 2.5**). Specifically:

> "The basic philosophy behind PN guidance, which implements parallel navigation, is that missile acceleration should nullify the LOS rate."

The PN law states that **commanded acceleration is proportional to the measured LOS rate**:

a_c(t) = N·v_cl·λ̇(t)

Where:
- **a_c(t)** is the commanded acceleration acting perpendicular to the instantaneous LOS
- **N** is the effective navigation ratio
- **v_cl** is the closing velocity (relative missile-to-target velocity)
- **λ̇(t)** is the LOS rate

When the LOS rate differs from zero in reality, the guidance command proportional to this deviation creates acceleration to eliminate the deviation, driving the LOS rate toward zero (**Section 2.5**).

### Control-Theoretic Formulation
As formulated in **Section 2.5**, PN can be viewed as a control problem that realizes the parallel navigation rule λ̇(t) → 0. Using Lyapunov stability analysis with Q = c·λ̇² as the Lyapunov function, the control law:

**u = k·v_cl·λ̇(t)**

stabilizes the system when k > 2v_cl, which corresponds to the effective navigation ratio N > 2. This ensures asymptotic stability with respect to the LOS derivative—meaning the LOS rate converges to zero, satisfying the parallel navigation condition.

---

## Historical Deployment Information

**The knowledge base does not specifically cover when proportional navigation was first used in a real missile system.** 

I read:
- **Section 1.1 (Introduction)** – which discusses early missile development through World War I and World War II, including the V-1 and V-2 missiles, but does not mention when proportional navigation was first fielded
- **Sections 2.1, 2.2, and 2.5** – which thoroughly cover the technical implementation but do not provide historical deployment dates

These sections discuss the technical theory and implementation of PN guidance but do not specify which missile system first employed it operationally or when that occurred.

**Your score:** 0.4

---

## 8. `q018` — `multi_hop` — run:v4 — [PRIMED]

**Question:** Why was frequency-domain analysis of missile guidance systems developed, given that time-domain analysis already exists?

**Reference answer:** Time-domain analysis of PN guidance systems cannot yield closed-form analytical expressions for miss distance when high-order models — those realistically reflecting autopilot and airframe dynamics, with time-varying coefficients — are used; designers are forced to rely on simulation tools like the method of adjoints. Frequency-domain analysis was developed because the method of transfer functions, the foundation of frequency methods, enables analytical expressions for miss distance to be obtained for these higher-order models, and because the frequency approach gives designers direct control over system bandwidth.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.1 INTRODUCTION', '04-Chapter-4---Analysis-of-Proportional.md#4.1 INTRODUCTION']

**Agent answer:**

Based on the knowledge base, I can now provide a direct answer to your question.

According to **Section 4.2 (Adjoint Method. Generalized Model)** of Chapter 4, frequency-domain analysis was developed because **time-domain analysis was bounded by the consideration of a step target acceleration signal**.

The key limitations that motivated frequency-domain development were:

1. **Restricted test signal capability**: The time-domain adjoint method could only analyze the system's response to a step target maneuver, which severely limited the range of target behaviors that could be evaluated.

2. **Need for more general analysis**: As stated in the text, "Because the frequency-domain analysis uses a different test signal, it is convenient to consider a more general model of the adjoint system commonly used in modern control theory." Frequency-domain methods employ transfer functions that enable analysis using various input signals through Laplace transforms.

3. **Broader maneuver analysis capability**: The frequency-domain approach enables determination of miss distance "for a wide class of target maneuvers," not just step maneuvers. This is particularly important because actual target evasion strategies involve complex, time-varying accelerations (e.g., sinusoidal weaves, random maneuvers) that cannot be adequately characterized by simple step inputs.

In practical terms, frequency-domain analysis allows engineers to:
- Characterize system dynamics using transfer functions (e.g., the missile's airframe, autopilot, guidance filters, and seeker as a combined transfer function *W(s)*)
- Evaluate system performance against realistic target maneuvers by transforming complex input signals
- Obtain analytical expressions for impulse responses that would be difficult to derive in the time domain for higher-order system models

**Your score:** 0.4

---

## 9. `q018` — `multi_hop` — run:v5 — [PRIMED]

**Question:** Why was frequency-domain analysis of missile guidance systems developed, given that time-domain analysis already exists?

**Reference answer:** Time-domain analysis of PN guidance systems cannot yield closed-form analytical expressions for miss distance when high-order models — those realistically reflecting autopilot and airframe dynamics, with time-varying coefficients — are used; designers are forced to rely on simulation tools like the method of adjoints. Frequency-domain analysis was developed because the method of transfer functions, the foundation of frequency methods, enables analytical expressions for miss distance to be obtained for these higher-order models, and because the frequency approach gives designers direct control over system bandwidth.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.1 INTRODUCTION', '04-Chapter-4---Analysis-of-Proportional.md#4.1 INTRODUCTION']

**Agent answer:**

Based on my reading of the full text from Sections 4.1 and 3.3, I can now provide a comprehensive answer.

## Why Frequency-Domain Analysis Was Developed

According to **Section 4.1**, frequency-domain analysis of missile guidance systems was developed to overcome fundamental limitations of time-domain analysis. While time-domain methods (specifically the method of adjoints) provided useful simulation capabilities, they suffered from several critical shortcomings:

### 1. Inability to Obtain Practical Analytical Expressions

As stated in **Section 4.1**: *"The difficulty of the analysis of differential equations with time-varying coefficients describing linearized models of guidance systems is that it does not allow researchers to obtain analytical expressions for miss distance that can be effectively utilized in practice."*

**Section 3.3** further elaborates: *"the necessity to simulate the system response for each impulse application time by using the model of the original system or using the adjoint system to simplify this procedure was stipulated by the inability to obtain an analytical expression for the miss step that can be used for analysis and design of missile guidance systems."*

### 2. Limitations of Simplified Models

The time-domain approach relied on simplified models (zero-lag or single time-constant representations) that did not accurately reflect real missile dynamics. As noted in **Section 4.1**: *"the disadvantage of the single time constant representation of a missile guidance system is that the miss distance can be seriously underestimated."* **Section 3.3** adds: *"The zero and single lag guidance systems are convenient analytical models, but they do not quite match reality."*

### 3. Inability to Handle High-Order Models and Target Dynamics

**Section 3.3** explicitly states: *"Because of the inability to obtain analytical expressions for the miss step for the high-order planar models, the simulation process using the method of adjoints still remains a very useful tool for time-domain analysis. The analytical difficulties do not allow researchers to build and analyze more complicated models that also include the dynamics of a maneuvering target."*

The key advantage of frequency-domain analysis, as noted in **Section 4.1**, is that it *"enables us to overcome the difficulties mentioned above"* by:
- Providing analytical expressions for miss distance (frequency response) for realistic guidance system models
- Allowing analysis of both step maneuvers and weaving targets (sinusoidal acceleration) through the same framework
- Enabling control of system bandwidth—a physical and intuitive design parameter
- Supporting the building of realistic models with justifiable simplifications

The frequency approach uses sinusoidal inputs as standard test signals (analogous to step signals in time-domain), allowing engineers to assess system response across a range of frequencies, which is particularly valuable for analyzing miss distance due to weaving targets.

**Your score:** 1.0

---

## 10. `q020` — `multi_hop` — run:v4 — [PRIMED]

**Question:** The book derives the proportional-navigation law as the solution to a control problem in Chapter 2 and revisits it via a Lyapunov approach in Chapter 5 — what does the Lyapunov treatment add beyond the Chapter 2 derivation?

**Reference answer:** Chapter 2's control-problem formulation derives PN by treating commanded acceleration as the control input and the LOS angle and its derivative as state variables, primarily under the non-maneuvering-target assumption. Chapter 5's Lyapunov approach reframes the same derivation as a partial-stability problem with respect to the LOS derivative, with the Lyapunov function chosen as the square of the LOS derivative (planar case) or as the sum of LOS-derivative components (3D case). The Lyapunov treatment adds two things: (1) it provides a unified framework whose negative-definiteness condition determines the applicability of any candidate guidance law, with the module of the Lyapunov-function derivative serving as a performance index for comparing existing PN variants and creating new ones; and (2) it extends naturally to maneuvering targets, where the augmented PN law and other PN modifications can be obtained as solutions of a stability problem rather than as ad-hoc extensions of the nonmaneuvering derivation.

**Expected chunks:** ['02-Chapter-2---Parallel-Navigation.md#2.5 PROPORTIONAL NAVIGATION AS A CONTROL PROBLEM', '05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN']

**Agent answer:**

Based on my review of the relevant sections, I can now synthesize the answer. The knowledge base reveals that **both chapters use Lyapunov methods**, but Chapter 5 significantly extends the Chapter 2 framework through what the book calls the "time-domain approach."

## What Chapter 2 Establishes (Section 2.5)

Chapter 2 derives PN as a solution to a **control problem for a linearized planar engagement model**. Using the state variables x₁ = λ(t) and x₂ = λ̇(t), it:
- Chooses a Lyapunov function Q = cx₂² (proportional to the square of LOS rate)
- Establishes **partial stability** with respect to x₂ (i.e., λ̇ → 0)
- Derives the classic PN law: a_M(t) = N·v_cl·λ̇(t) with N > 2

The derivation relies on the near-collision course assumption (r̈(t) ≈ 0) and small-angle approximations.

---

## What Chapter 5 Adds via the Lyapunov "Time-Domain Approach"

Chapter 5 does **not** abandon the Lyapunov framework—it generalizes and extends it in four key ways:

### 1. **Performance Criterion for Law Comparison** (Section 5.2)
Chapter 5 introduces |Q̇| (the magnitude of the Lyapunov function derivative) as a **performance index** to compare PN-class guidance laws. The law that drives λ̇(t) → 0 *faster* at each instant (more negative Q̇) is preferable. This transforms the finite-time engagement problem into an infinite-time partial stability problem with an explicit optimization criterion not present in Chapter 2.

### 2. **Nonlinear Corrections and Extended Applicability** (Section 5.5)
Chapter 5 treats the **general nonlinear planar case** (without small-angle approximation), deriving the guidance law as a sum of the basic PN term plus "correction controls":

u = u_PN + u₀ + u₁ + u₂ + u₃

Where:
- **u₀** = –N₀r(t)λ̇²(t)sin(λ(t)) — compensates for large LOS angles
- **u₁** = N₁λ̇³(t) — provides variable effective navigation ratio (larger gain when LOS rate is high for faster response, smaller when low to reduce noise)
- **u₂** = N₂r̈(t)λ(t) — the "shaping term" acting along the LOS
- **u₃** = N₃(t)·sign(a_T(t)λ̇(t))·|a_T(t)| — improved maneuver compensation with time-varying gain

These corrections extend PN's validity beyond small angles and short ranges.

### 3. **Impact Angle Constraints** (Section 5.4)
Chapter 5 modifies the Lyapunov function to handle **specified terminal LOS angles** λ₀:

Q = c₁(x₁ – λ₀)² + cx₂²

This shifts from partial stability (only x₂ → 0) to **stability of the full system**, driving both x₁ → λ₀ and x₂ → 0. The resulting guidance law adds a shaping term N₂r̈(t)(λ(t) – λ₀) to achieve the desired impact geometry.

### 4. **Full Three-Dimensional Treatment** (Section 5.6)
The 3D guidance law is derived using:
- A Lyapunov function Q = Σ d_sλ̇_s² (sum over LOS rate components)
- **Radial and tangential acceleration components**, revealing that the u₂ term acts radially (along LOS) to influence closing velocity
- A structure showing the 3D law embeds the planar results as special cases

---

## Summary Table

| Aspect | Chapter 2 | Chapter 5 Addition |
|--------|-----------|-------------------|
| **Engagement model** | Linearized planar | General nonlinear + 3D |
| **Stability type** | Partial (x₂ only) | Partial and full system (with λ₀ constraint) |
| **Lyapunov function** | Q = cx₂² | Extended forms including angle error and cross-terms |
| **Performance metric** | None explicit | \|Q̇\| as instantaneous convergence criterion |
| **Corrections** | Basic APN: +a_T(t) | Cubic LOS term, geometric corrections, time-varying gains |
| **Impact angle** | Not addressed | Handled via modified Lyapunov function |

In essence, Chapter 5 treats the Lyapunov framework not just as a proof tool (as in Chapter 2) but as a **systematic design methodology** for creating, comparing, and improving guidance laws with guaranteed stability properties.

**Your score:** 1.0

---

## 11. `q020` — `multi_hop` — run:v5 — [PRIMED]

**Question:** The book derives the proportional-navigation law as the solution to a control problem in Chapter 2 and revisits it via a Lyapunov approach in Chapter 5 — what does the Lyapunov treatment add beyond the Chapter 2 derivation?

**Reference answer:** Chapter 2's control-problem formulation derives PN by treating commanded acceleration as the control input and the LOS angle and its derivative as state variables, primarily under the non-maneuvering-target assumption. Chapter 5's Lyapunov approach reframes the same derivation as a partial-stability problem with respect to the LOS derivative, with the Lyapunov function chosen as the square of the LOS derivative (planar case) or as the sum of LOS-derivative components (3D case). The Lyapunov treatment adds two things: (1) it provides a unified framework whose negative-definiteness condition determines the applicability of any candidate guidance law, with the module of the Lyapunov-function derivative serving as a performance index for comparing existing PN variants and creating new ones; and (2) it extends naturally to maneuvering targets, where the augmented PN law and other PN modifications can be obtained as solutions of a stability problem rather than as ad-hoc extensions of the nonmaneuvering derivation.

**Expected chunks:** ['02-Chapter-2---Parallel-Navigation.md#2.5 PROPORTIONAL NAVIGATION AS A CONTROL PROBLEM', '05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN']

**Agent answer:**

Based on my reading of the full sections, I can now synthesize the answer.

## What the Lyapunov Treatment Adds (Chapter 5 vs. Chapter 2)

**Chapter 2's Optimal Control Approach (Section 2.7)** treats the PN law as the solution to an **inverse optimal control problem**. Under near-collision course assumptions (constant closing velocity, ignoring missile dynamics), it minimizes the quadratic performance index:

$$J = \frac{C}{2}y^2(t_F) + \frac{1}{2}\int_0^{t_F} a_M^2(t)\,dt$$

where the first term penalizes miss distance and the second penalizes control energy. The analysis shows that PN with navigation ratio **N = 3** is optimal for this specific functional as C → ∞ (zero miss). This is primarily a **theoretical result** demonstrating optimality under restrictive assumptions.

**Chapter 5's Lyapunov Approach (Section 5.2)** adds several practical dimensions that Chapter 2 lacks:

1. **A Comparison Criterion for Guidance Laws**: The Lyapunov treatment introduces the **module of the Lyapunov function derivative |Q(t)|** as a performance index to compare different PN-class guidance laws. This measures "closeness to parallel navigation" — how fast the line-of-sight rate λ̇(t) tends to zero.

2. **A Design Methodology**: Rather than just proving optimality of a single law, Chapter 5 uses Lyapunov analysis to **create new guidance laws** within the PN class. The approach transforms the finite-time engagement problem into an infinite-interval partial stability problem, enabling systematic control design.

3. **Practical Guidance Law Selection**: The Chapter 2 derivation assumes specific idealized conditions to derive N = 3 as "optimal." Chapter 5's Lyapunov framework provides a **physical justification for choosing among different navigation ratios** or PN variants based on transient performance (how quickly λ̇ → 0), without requiring full trajectory simulation.

In summary, Chapter 2 answers "When is PN theoretically optimal?" while Chapter 5 answers "How do we compare and design PN-type laws in practice?" The Lyapunov approach shifts from proving optimality under restrictive assumptions to providing an engineering tool for guidance law selection and synthesis.

**Your score:** 0.4

---

## 12. `q022` — `multi_hop` — run:v4 — [CLEAN]

**Question:** A missile flight has three phases — which guidance law dominates the midcourse phase in endoatmospheric engagements, what does it optimize, and what is the operational significance?

**Reference answer:** A missile flight consists of three phases: boost, midcourse, and homing. Kappa guidance dominates midcourse guidance in the endoatmosphere. It is an optimal guidance law that maximizes the missile's speed at the beginning of the terminal phase of flight, which is essential when engaging targets at far distances or low altitudes — where missile velocity is the prime factor. Kappa is also applied to close-in targets where the time line is critical (the missile must destroy the target before it reaches the minimum range of intercept). The Kappa midcourse algorithm is successfully used in the U.S. Standard Missile 2 (SM2), and is typically deployed alongside proportional navigation, which is used in the homing/terminal phase.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS', '08-Chapter-8---Testing-Guidance-Laws.md#8.8 KAPPA GUIDANCE']

**Agent answer:**

According to **Section 8.8 (Kappa Guidance)** of Chapter 8, the guidance law that dominates midcourse guidance in endoatmospheric engagements is the **Kappa algorithm**.

**What it optimizes:**
Kappa guidance is an optimal guidance law that **maximizes terminal missile velocity** — specifically, it maximizes missile speed at the beginning of the terminal phase of flight. The optimal problem is formulated as finding coefficients K₁ and K₂ that maximize the terminal value of the missile velocity vector **v**_M, yielding a guidance law consisting of a proportional term (based on range-to-go) and a shaping term (based on desired terminal velocity vector).

**Operational significance:**
- **Against far-distant or low-altitude targets:** Missile velocity is the prime factor for engagement success, making velocity maximization essential.
- **Against close-in targets:** The timeline becomes critical — the missile must destroy the target before it reaches within the minimum range of intercept.
- **Real-world implementation:** Despite the complexity of optimal guidance (requiring predicted intercept point estimation and complete information about missile/target states), the Kappa midcourse guidance algorithm is successfully deployed in the **SM2 (U.S. Standard Missile 2)** missiles. The guidance law accounts for drag and lift effects through coefficients incorporating drag components (D₀), lift factor (L_α), thrust (T), mass (m), and speed (v).

**Your score:** 1.0

---

## 13. `q022` — `multi_hop` — run:v5 — [CLEAN]

**Question:** A missile flight has three phases — which guidance law dominates the midcourse phase in endoatmospheric engagements, what does it optimize, and what is the operational significance?

**Reference answer:** A missile flight consists of three phases: boost, midcourse, and homing. Kappa guidance dominates midcourse guidance in the endoatmosphere. It is an optimal guidance law that maximizes the missile's speed at the beginning of the terminal phase of flight, which is essential when engaging targets at far distances or low altitudes — where missile velocity is the prime factor. Kappa is also applied to close-in targets where the time line is critical (the missile must destroy the target before it reaches the minimum range of intercept). The Kappa midcourse algorithm is successfully used in the U.S. Standard Missile 2 (SM2), and is typically deployed alongside proportional navigation, which is used in the homing/terminal phase.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.2 GUIDANCE PROCESS', '08-Chapter-8---Testing-Guidance-Laws.md#8.8 KAPPA GUIDANCE']

**Agent answer:**

I now have the complete information to answer your question. Based on the full text of Section 8.8 and Section 8.1 of Chapter 8 (Testing Guidance Laws), here is the answer:

## The Three Phases of Missile Flight

According to Section 8.1, the three phases are:
1. **Launch phase** — uncontrolled boost stage where the rocket motor accelerates the missile to operating velocity
2. **Midcourse phase** — missile is guided by radar into an area allowing it to acquire and lock onto the target with its own sensor
3. **Terminal (homing) phase** — missile uses its local sensor measurements to guide onto the target; this phase removes residual errors accumulated during prior phases

## Midcourse Guidance in Endoatmospheric Engagements

**Kappa guidance** dominates midcourse guidance in the endoatmosphere.

### What It Optimizes

Kappa guidance is an **optimal guidance law that maximizes the terminal missile velocity** — specifically, the missile speed at the beginning of the terminal phase of flight. This is achieved by finding optimal coefficients for the proportional and shaping terms that maximize the terminal value of missile velocity.

### Operational Significance

According to Section 8.8, this requirement is operationally essential for two distinct scenarios:

1. **Long-range or low-altitude targets**: "When engaging a target at long range or at low altitude, missile velocity is the prime factor."

2. **Close-in targets**: "When engaging a close-in target, the time line is most important because the missile must destroy the target before it reaches within the minimum range of intercept."

Kappa guidance achieves this by calculating a proportional term based on range-to-go and a shaping term based on the desired terminal velocity vector, which is defined by vertical and horizontal trajectory shaping angles (e.g., approximately 45° for tactical ballistic missiles, approximately –75° for cruise missiles).

The algorithm's practical value is confirmed by its successful implementation in the **SM2 (U.S. Standard Missile 2)** system.

**Your score:** 1.0

---

## 14. `q029` — `ambiguous` — run:v4 — [PRIMED]

**Question:** What is the optimal guidance law?

**Reference answer:** The system should recognize that 'optimal' is used in several distinct, non-equivalent senses across the book — and either ask which sense the user means, or surface the multiplicity. The relevant senses include: (1) PN with N=3 is optimal in the inverse-optimal-control sense under idealized assumptions — constant closing velocity, planar engagement, no missile dynamics, non-maneuvering target — minimizing a quadratic cost functional (Ch2 §2.7); (2) Lyapunov-based guidance laws are 'optimal' in the sense of guaranteeing partial stability with respect to the LOS derivative (Ch5 §5.3); (3) neoclassical guidance is 'optimal' in the sense of achieving zero miss distance for the linearized engagement model — but this can worsen real performance when missile dynamics are ignored (Ch6 §6.2); (4) Kappa guidance is optimal in the sense of maximizing terminal missile velocity at the start of homing (Ch8 §8.8); (5) integrated guidance-and-control design (Ch9 §9.3) is optimal in the sense of jointly minimizing a performance index across both subsystems. Each of these is a defensible answer to 'what is optimal'; silently picking one — typically PN with N=3 because §2.7 is highly BM25-retrievable — without surfacing the other senses is a failure.

**Expected chunks:** (none — no_answer/ambiguous)

**Agent answer:**

Based on my search of the knowledge base, I can now provide a comprehensive answer. There is **no single "optimal guidance law"**—optimality depends entirely on the specific performance criterion (performance index) being optimized.

## Key Findings

### 1. PN Law Optimality (Section 2.7)
Under specific conditions, **Proportional Navigation with navigation ratio N = 3** is optimal. According to the text, linear controls are optimal for systems with linear differential equations and a quadratic performance index. For the near-collision course case (constant closing velocity, ignoring missile dynamics), the performance index is:

$$J = \text{(miss distance)}^2 + C \int_0^{t_F} a_M^2(t) dt$$

where:
- The first term represents miss distance (terminal accuracy)
- The second term represents energy expenditure during flight
- *C* is a weighting factor (high *C* emphasizes small miss; low *C* emphasizes energy conservation)

**Zero miss corresponds to C → ∞**, yielding the optimal guidance law:

$$a_M(t) = \frac{3}{t_{go}^2}(y(t) + \dot{y}(t)t_{go}) = 3v_{cl}\dot{\lambda}(t)$$

This is **PN with N = 3**, which guarantees zero miss distance under the stated assumptions.

### 2. Kappa Guidance Optimality (Section 8.8)
**Kappa guidance** is another optimal guidance law, but for a different objective: it **maximizes terminal missile velocity** at the beginning of the terminal phase. This is essential for:
- Long-range targets
- Low-altitude targets
- Close-in targets where timeline is critical

The Kappa law is formulated as finding optimal coefficients *K₁* and *K₂* that maximize the terminal velocity **v**_M, resulting in:

$$\mathbf{a}_M = K_1(\mathbf{r}_{PIP} - \mathbf{r}_M) + K_2(\mathbf{v}_{PIP} - \mathbf{v}_M)$$

where the optimal values incorporate drag (*D₀*), lift factor (*L_α*), thrust (*T*), mass (*m*), and velocity (*v*).

## Summary
The "optimal guidance law" depends on your mission objective:
- **For minimizing miss + energy**: PN with N = 3
- **For maximizing terminal velocity**: Kappa guidance

The text also notes that "it is difficult to reflect all factors when formulating the optimal guidance problem, so that many optimal problems discussed in the literature have not been implemented in practice."

**Your score:** 0.5

---

## 15. `q029` — `ambiguous` — run:v5 — [PRIMED]

**Question:** What is the optimal guidance law?

**Reference answer:** The system should recognize that 'optimal' is used in several distinct, non-equivalent senses across the book — and either ask which sense the user means, or surface the multiplicity. The relevant senses include: (1) PN with N=3 is optimal in the inverse-optimal-control sense under idealized assumptions — constant closing velocity, planar engagement, no missile dynamics, non-maneuvering target — minimizing a quadratic cost functional (Ch2 §2.7); (2) Lyapunov-based guidance laws are 'optimal' in the sense of guaranteeing partial stability with respect to the LOS derivative (Ch5 §5.3); (3) neoclassical guidance is 'optimal' in the sense of achieving zero miss distance for the linearized engagement model — but this can worsen real performance when missile dynamics are ignored (Ch6 §6.2); (4) Kappa guidance is optimal in the sense of maximizing terminal missile velocity at the start of homing (Ch8 §8.8); (5) integrated guidance-and-control design (Ch9 §9.3) is optimal in the sense of jointly minimizing a performance index across both subsystems. Each of these is a defensible answer to 'what is optimal'; silently picking one — typically PN with N=3 because §2.7 is highly BM25-retrievable — without surfacing the other senses is a failure.

**Expected chunks:** (none — no_answer/ambiguous)

**Agent answer:**

Based on the textbook's full coverage of optimal guidance theory, I can now synthesize an answer. There is **no single universal "optimal guidance law"** — optimality depends entirely on the performance index chosen for the specific engagement requirements.

## 1. PN as Optimal Under Quadratic Performance Index

According to **Section 2.7**, Proportional Navigation (PN) is optimal when:

- The system has **linear differential equations**
- The performance index is **quadratic** (LQ optimal control theory)
- Under near-collision course assumptions (constant closing velocity, ignoring missile dynamics)

For the equation of motion with state variables y (relative displacement) and ẏ, the performance index is:

$$J = y^2(t_F) + C \int_0^{t_F} a_M^2(t)\,dt$$

where:
- First term: **miss distance** at terminal time
- Second term: **energy expenditure** during flight
- C = weighting factor (high C → emphasize accuracy; low C → emphasize energy)

**The optimal solution is:**

$$a_M(t) = \frac{3}{(1 + \frac{3}{C})t_{go}^2} \left[y(t) + \dot{y}(t)t_{go}\right]$$

As **C → ∞** (zero miss required), the optimal guidance law becomes:

$$a_M(t) = \frac{3}{t_{go}^2}\left[y(t) + \dot{y}(t)t_{go}\right] = 3v_{cl}\dot{\lambda}$$

**This is PN with navigation ratio N = 3** — the optimal value guaranteeing zero miss under these simplified assumptions.

## 2. Kappa Guidance: Optimal for Terminal Velocity

As described in **Section 8.8**, **Kappa guidance** is optimal for a different objective: **maximizing terminal missile velocity** at the predicted intercept point. This is essential for:
- Long-range engagements
- Low-altitude targets  
- Close-in targets requiring minimum time-to-intercept

The Kappa algorithm solves for optimal coefficients K₁ and K₂ in:

$$\mathbf{a}_c = K_1(\mathbf{v}_{PIP} - \mathbf{v}_M) + K_2(\mathbf{r}_{PIP} - \mathbf{r}_M - \mathbf{v}_{PIP}t_{go})$$

The optimal values are:

$$K_1 = \frac{(D_0 - \frac{T}{m})}{\frac{L_\alpha}{v}|\mathbf{r}_{tgo}|}, \quad K_2 = \frac{3}{|\mathbf{r}_{tgo}|}$$

This law is implemented in operational systems (SM2 Standard Missile) and consists of:
- **Proportional term**: Velocity matching toward terminal velocity
- **Shaping term**: Trajectory shaping using position error

## 3. General Optimal Control Formulation

Per **Section 9.3.1**, the optimal guidance problem is formulated as minimizing a generalized performance index:

$$J = V_0(\mathbf{x}(t_F)) + \int_0^{t_F} L(\mathbf{x}(t), \mathbf{u}(t), t)\,dt$$

This leads to the **Bellman functional equation**:

$$\frac{\partial V}{\partial t} + \min_{\mathbf{u}}\left\{\mathbf{c}^T(\mathbf{x},t)\frac{\partial V}{\partial \mathbf{x}} + L(\mathbf{x},\mathbf{u},t)\right\} = 0$$

**Key insight from the text:** "The analytical solution exists only for the linear-quadratic problems." For nonlinear, realistic missile dynamics with drag, lift, and maneuvering targets, closed-form optimal solutions are generally intractable.

## Summary: What is "Optimal"?

| Scenario | Optimal Law | Performance Index |
|----------|-------------|-------------------|
| Simplified linear engagement | PN with N=3 | Miss distance + control energy |
| Maximize terminal velocity | Kappa guidance | Terminal speed |
| General nonlinear problem | Numerical solution | Problem-dependent |

**Practical limitation noted in the text:** "It is difficult to reflect all factors when formulating the optimal guidance problem, so that many optimal problems discussed in the literature have not been implemented in practice."

**Your score:** 0.5

---

## 16. `q030` — `ambiguous` — run:v4 — [PRIMED]

**Question:** What is the miss distance for my missile guidance system?

**Reference answer:** The system should recognize that miss distance is not a single number — it depends on multiple unspecified factors that the question does not provide — and either ask for the missing context, or surface the parameter dependence. The relevant unspecified factors include: (a) model order — first-order, single-time-constant, or higher-order models give different miss expressions (Ch3, Ch4); (b) input type — step target maneuver, sinusoidal/weave maneuver, or random maneuver each yields a different miss-distance formula (Ch3 §3.2, Ch4 §4.5, Ch7 §7.3); (c) deterministic vs stochastic analysis — peak miss vs rms miss are conceptually different metrics (Ch3-4 vs Ch7); (d) inclusion or exclusion of noise sources such as glint or thermal noise (Ch7 §7.4); (e) which guidance law (PN, APN, Lyapunov-derived, Kappa) is in use. Without these, no single 'miss distance' answer is correct. Silently committing to one (e.g., quoting the §3.2 first-order expression as if it were definitive) without surfacing the parameter dependence is a failure.

**Expected chunks:** (none — no_answer/ambiguous)

**Agent answer:**

Based on the knowledge base, I can provide you with a comprehensive explanation of **miss distance** in missile guidance systems.

## Definition

**Miss distance** is the terminal guidance accuracy metric representing the distance between the missile and target at their closest approach point. According to Section 4.1 (Analysis of Proportional Navigation Guidance Systems), it is the key performance indicator for assessing guided missile systems.

## Analytical Determination

The miss distance can be obtained through several approaches:

1. **Method of Adjoints**: For linearized guidance system models, the method of adjoints enables analytical expressions for miss distance. The adjoint system's impulse response relates to the original system's miss distance (Section 3.3).

2. **Frequency Response Approach**: The miss distance due to a weaving target (sinusoidal acceleration) can be obtained from the frequency response of the linearized guidance system. Miss due to step target maneuvers can also be derived from these frequency characteristics (Section 4.1).

## Main Factors Influencing Miss Distance

According to Section 4.1, the primary factors affecting miss distance in homing missiles are:

| Factor | Description |
|--------|-------------|
| **Seeker errors** | Tracking inaccuracies and noise (τ₂, τ₃ parameters) |
| **Airframe characteristics** | Dynamics including damping, natural frequency, and airframe zero frequency (ωz) |
| **Autopilot lag** | Time constant τ₁ of the flight control system |
| **Target maneuvers** | Step and weaving (sinusoidal) target accelerations |

## RMS Miss Distance Due to Noises

For stochastic analysis, the **rms miss distance** is calculated as follows (Section 7.4):

- **Total rms miss distance**: Square root of the sum of variances from independent noise sources:
  - Glint noise (ηg) — mainly affects radar-guided missiles
  - Range-independent noise (ηr) — proportional to closing velocity vcl
  - Range-dependent noise — proportional to vcl² (semiactive) or vcl³ (active)

The general expression for rms response at final time tF due to white noise input with spectral density Φn is:

$$y_{rms}(t_F) = \sqrt{\Phi_n \int_0^{t_F} P_0^2(t_F, \sigma) d\sigma}$$

where P₀(tF, σ) is the system impulse response obtained via the adjoint method.

## Practical Considerations

- Single time constant representations can **seriously underestimate** miss distance (Section 4.1)
- Neoclassical guidance can suppress range-independent and range-dependent noises (eliminating their influence on miss distance), though glint noise reduction remains limited (Section 7.4)

Would you like me to elaborate on calculating miss distance for a specific guidance system configuration or noise scenario?

**Your score:** 0.5

---

## 17. `q034` — `single_hop` — run:v5 — [PRIMED]

**Question:** What causes the radome effect and why is it worse at high altitudes?

**Reference answer:** A nonhemispheric radome refracts incoming electromagnetic waves, causing aberration of the measured LOS angles. The aberration has a destabilizing effect on the guidance loop, and the effect is more severe at high altitudes.

**Expected chunks:** ['08-Chapter-8---Testing-Guidance-Laws.md#8.6 SEEKER MODEL']

**Agent answer:**

Based on my reading of the relevant section, I can now provide you with an answer about the radome effect. The key information is found in **Section 8.6 (SEEKER MODEL)** of Chapter 8.

## What Causes the Radome Effect

According to the text, the radome effect arises because:

1. **Electromagnetic Wave Refraction**: A nonhemispheric radome (the protective dome covering the seeker antenna designed to protect the missile from airflow and reduce drag) causes **refraction of incoming electromagnetic waves**. This refraction gives a wrong indication of the target's location.

2. **Coupling to Body Dynamics**: The radome effect **couples the missile's line-of-sight (LOS) angles to the body dynamics through the gimbal angles**, causing **aberration of the measured LOS angles**. The measured LOS angles depend nonlinearly on the horizontal and vertical gimbal angles (ψₛ and θₛ).

3. **Approximate Error Terms**: In first-order approximation, the radome introduces additional error terms **ρψψₛ** and **ρθθₛ** in the azimuth and elevation channels respectively, where ρψ and ρθ are radome slope coefficients.

## Why It Is Worse at High Altitudes

The text explicitly states: *"The radome reflection has a destabilizing effect on the missile guidance system, **especially at high altitudes**"* [18,19]. 

While the text does not explicitly detail the physical mechanism for this altitude dependence, it appears in the context where tail-controlled aerodynamic missiles exhibit performance deterioration at high altitudes—specifically, the existence of **low-frequency right-half plane zeros** in the flight control dynamics (ωz = 5 rad/s in the example) that correspond to high-altitude flight conditions. These non-minimum phase characteristics, combined with the radome-induced LOS aberrations, create a more destabilizing feedback situation at high altitudes than at lower altitudes.

The radome slope coefficients (ρψ and ρθ) in simulation models are typically described as random processes to account for manufacturing variations and operational conditions.

**Source**: Modern Missile Guidance, Chapter 8, Section 8.6 (SEEKER MODEL), pp. 126-128.

**Your score:** 1.0

---

## 18. `q035` — `multi_hop` — run:v4 — [PRIMED]

**Question:** How does adding a cubic term to the Lyapunov guidance law compare to using it in the pseudoclassical method? Do they achieve the same thing?

**Reference answer:** Both approaches add a nonlinear cubic term in LOS rate to improve on standard PN, but their derivation is different: the Lyapunov approach derives the cubic term from stability conditions in the time domain (Section 5.3), while the pseudoclassical approach uses it as part of frequency-domain feedforward/feedback compensation (Section 6.4). The mechanism is the same modification, the framing is different.

**Expected chunks:** ['05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN', '06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS']

**Agent answer:**

[Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Your score:** 0.0

---

## 19. `q035` — `multi_hop` — run:v5 — [PRIMED]

**Question:** How does adding a cubic term to the Lyapunov guidance law compare to using it in the pseudoclassical method? Do they achieve the same thing?

**Reference answer:** Both approaches add a nonlinear cubic term in LOS rate to improve on standard PN, but their derivation is different: the Lyapunov approach derives the cubic term from stability conditions in the time domain (Section 5.3), while the pseudoclassical approach uses it as part of frequency-domain feedforward/feedback compensation (Section 6.4). The mechanism is the same modification, the framing is different.

**Expected chunks:** ['05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN', '06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS']

**Agent answer:**

[Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Your score:** 0.0

---

## 20. `q036` — `multi_hop` — run:v4 — [CLEAN]

**Question:** What's the difference between miss distance for a deterministic weaving target versus a random-phase sinusoidal maneuver?

**Reference answer:** Deterministic weaving uses the frequency response magnitude to find peak miss distance (Ch6 Section 6.4), while a random-phase sinusoidal maneuver is treated as white noise through a shaping filter, yielding RMS miss distance (Ch7 Section 7.5). One is a peak metric, the other is a statistical one.

**Expected chunks:** ['06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS', '07-Chapter-7---Guidance-Law-Performance.md#7.5 EFFECT OF RANDOM TARGET MANEUVERS ON MISS DISTANCE']

**Agent answer:**

Based on the retrieved content, I can now provide a comprehensive answer about the difference between these two types of maneuvers.

---

## Summary

The key difference lies in **how the miss distance is characterized**—the deterministic weaving target yields a specific **miss peak** (worst-case amplitude), while the random-phase sinusoidal maneuver yields an **RMS miss distance** computed via stochastic methods.

---

## 1. Deterministic Weaving/Sinusoidal Maneuver

As described in **Section 4.5 (Weave Maneuver Analysis)**, the deterministic sinusoidal maneuver has a fixed, known form:

- The maneuver is represented as **a_T sin(ω_T t)** with specific frequency and phase
- This is a "barrel roll" strategy that is deterministic and "quite realistic" (Section 7.3)
- The analysis yields a **steady-state miss distance** that varies with weaving frequency ω

**Key characteristics:**
- The miss distance depends on the relationship between target weaving frequency and guidance system dynamics
- There exists an **optimal weaving frequency** ω_opt that maximizes the miss distance (worst-case scenario)
- For a simple first-order guidance system with time constant τ₁, the amplitude characteristic is:

|P(t_F, iω)| = [B₁²ω² / ((N-2)²ω² + (1/τ₁² + ω²)(1 + τ₁²ω²))]^(1/2)

where B₁ = –τ₁

- The steady-state miss due to a weaving target is:

Miss(t) = a_T|P(t_F, iω)|sin(ωt + φ)

**Example (Section 4.5):** For N = 3 and τ₁ = 0.5 s, the peak miss of 0.93 m occurs at a target frequency of 1.5 rad/s.

---

## 2. Random-Phase Sinusoidal Maneuver

As described in **Sections 7.3 and 7.5**, the random-phase sinusoidal maneuver has the form:

**a_T(t) = a_T sin(ω_T t + φ_T)**

where φ_T is a **uniformly distributed random variable** (representing random starting time over flight time t_F).

**Key characteristics:**
- The random starting time is uniformly distributed over flight time t_F (probability density p_T(t) = 1/t_F for 0 ≤ t ≤ t_F)
- This maneuver is considered more realistic than the deterministic case because the defender doesn't know when the target will begin weaving
- Can be represented as **white noise** with power spectral density **Φ_φ = a_T²/t_F** passing through a shaping filter with transfer function:

W_filter(s) = (s²/ω_T + ω_T)^(-1)

- The **RMS miss distance** is computed using adjoint methods for stochastic analysis (Figure 7.6)
- For the first-order guidance system model, the RMS miss distance is given by equation (7.51)

---

## Key Differences

| Aspect | Deterministic Weaving | Random-Phase Sinusoidal |
|--------|----------------------|-------------------------|
| **Characterization** | Fixed phase and frequency | Random phase φ_T uniformly distributed |
| **Miss Metric** | Peak miss distance (worst-case amplitude) | RMS miss distance (statistical average) |
| **Analysis Method** | Frequency-domain, steady-state analysis | Stochastic methods, adjoint system with white noise representation |
| **Representation** | Deterministic input signal | White noise with PSD = a_T²/t_F through shaping filter |
| **Practical Use** | Evaluates worst-case barrel roll scenario | Models realistic unknown starting time |

---

## Practical Implication

As noted in Section 7.3, the deterministic sinusoidal maneuver enables evaluation of the **"miss peak"** and **worst-case scenario** (existence of optimal evasive frequency), while the random-phase maneuver provides a **statistical approach** for designing defensive missiles when the target's exact maneuver timing is unknown.

**Your score:** 1.0

---

## 21. `q036` — `multi_hop` — run:v5 — [CLEAN]

**Question:** What's the difference between miss distance for a deterministic weaving target versus a random-phase sinusoidal maneuver?

**Reference answer:** Deterministic weaving uses the frequency response magnitude to find peak miss distance (Ch6 Section 6.4), while a random-phase sinusoidal maneuver is treated as white noise through a shaping filter, yielding RMS miss distance (Ch7 Section 7.5). One is a peak metric, the other is a statistical one.

**Expected chunks:** ['06-Chapter-6---Design-of-Guidance-Laws.md#6.4 EXAMPLE SYSTEMS', '07-Chapter-7---Guidance-Law-Performance.md#7.5 EFFECT OF RANDOM TARGET MANEUVERS ON MISS DISTANCE']

**Agent answer:**

Based on my reading of the textbook, I can now provide a comprehensive answer comparing the miss distance characteristics for these two types of target maneuvers.

## Key Differences

### Deterministic Weaving (Sinusoidal Maneuver)
According to **Section 4.5 (Weave Maneuver Analysis)**, a deterministic weaving target executes a sinusoidal maneuver with a specific, known form:

- The analysis yields a **"miss peak"** — the maximum steady-state miss distance amplitude as a function of weaving frequency.
- This miss peak represents the **worst-case scenario** for a given weaving frequency. For example, with a first-order guidance system model (time constant τ₁ = 0.5 s, N = 3), the peak miss of **0.93 m** occurs at a target weaving frequency of **1.5 rad/s** (period ≈ 4.2 s) for a 1-g maneuver amplitude.
- The deterministic analysis provides a frequency response characterization — targets with very low weaving frequencies appear as "near-constant" maneuvers, while very high frequencies cause minimal displacement. The "miss peak" occurs at an optimal intermediate frequency.

### Random-Phase Sinusoidal Maneuver
According to **Section 7.3 (Random Target Maneuvers)** and **Section 7.5**, a random-phase sinusoidal maneuver has the form:
$$a_T(t) = a_T \sin(\omega_T t + \phi_T)$$

where φ_T is a uniformly distributed random variable (or equivalently, the starting time is uniformly distributed over the flight time t_F).

- This is modeled as **white noise** with power spectral density **Φ_ϕ = a_T²/t_F** passing through a shaping filter with transfer function $W_{filter}(s) = (s^2/\omega_T + \omega_T)^{-1}$.
- The result is an **RMS miss distance** — a statistical measure rather than a deterministic peak value. The textbook provides the expression (Equation 7.51):

$$y_{rms} = \sqrt{\frac{a_T^2}{t_F} \cdot \frac{1}{2\pi} \int_{-\infty}^{\infty} |P_T(t_F, i\omega)|^2 \left| \frac{\omega_T}{\omega_T^2 - \omega^2} \right|^2 d\omega}$$

- **Section 7.7** shows example results for a 3-g random-phase sinusoidal maneuver with ω_T = 1.4 rad/s (Figure 7.12), illustrating how the RMS miss varies with flight time.

## Summary Comparison

| Aspect | Deterministic Weaving | Random-Phase Sinusoidal |
|--------|----------------------|------------------------|
| **Form** | Fixed sinusoid: sin(ωt) | Random phase: sin(ωt + φ) |
| **Output metric** | Miss peak (maximum amplitude) | RMS miss distance |
| **Interpretation** | Worst-case for specific frequency | Statistical average over random starting times |
| **Physical model** | Deterministic frequency response | Shaping filter driven by white noise |
| **Realism** | Represents a "barrel roll" with known timing | More realistic — maneuver start time unknown |

The deterministic miss peak enables evaluation of worst-case engagement scenarios for system design, while the random-phase RMS miss distance provides a statistical assessment of performance when the target's maneuver initiation timing is unknown.

**Your score:** 1.0

---

## 22. `q046` — `single_hop` — run:v4 — [CLEAN]

**Question:** For a cruciform missile configuration, what simplification applies to the moment equations, and why?

**Reference answer:** A cruciform configuration is symmetrical about both the xy and xz planes, so the product of inertia Ixz = 0. This removes the cross-axis inertia symmetry term that otherwise couples the roll-yaw moment equations, simplifying the moment equations (and further simplifying if Iyy = Izz, as for a circular body cross section).

**Expected chunks:** ['08-Chapter-8---Testing-Guidance-Laws.md#8.3 MISSILE DYNAMICS']

**Agent answer:**

According to **Section 8.3 (Missile Dynamics)** of Chapter 8, for a **cruciform missile configuration**, the moment equations are simplified by the elimination of the **product-of-inertia terms** (Ixy, Ixz, Iyz).

## The Simplification

In the general case, the moment equations include all three mass products of inertia:
- Ixy (about the x and y axes)
- Ixz (about the x and z axes)  
- Iyz (about the y and z axes)

For a cruciform configuration, which is **symmetrical about both the xy and xz planes**, all three product-of-inertia terms vanish:

**Ixy = 0, Iyz = 0, and Ixz = 0**

This reduces the general moment equations to the simpler form where each moment component depends only on its corresponding principal moment of inertia and the angular rates, eliminating the cross-coupling terms involving products of inertia.

## The Reason

The simplification occurs because of **geometric and mass symmetry**:

1. **Symmetry about the xz plane** → Iyz = 0 and Ixy = 0
2. **Symmetry about the xy plane** (additional symmetry in cruciform configuration) → **Ixz = 0**

The text states: *"In the case of a cruciform configuration, which is symmetrical about both the xy and xz planes, Ixz = 0 as well, so that equation (8.7) is reduced"* to the simplified form (equation 8.8 in the text). This allows the moment equations to decouple into simpler expressions for roll (L), pitch (M), and yaw (N) moments without the cross-axis inertia coupling terms that appear in the general case.

**Your score:** 1.0

---

## 23. `q050` — `single_hop` — run:v4 — [CLEAN]

**Question:** What's the condition for BIBO stability of a PN guidance system?

**Reference answer:** The PN guidance system is BIBO stable if, for any bounded target acceleration, its miss y(tF) stays bounded for all flight times. The condition: the inverse Laplace transform of the transfer function P(tF,s) must be absolutely integrable on [0, infinity). Equivalently, P(tF,s) must be analytic in the right half-plane (including the imaginary axis) and lim as s goes to infinity of P(tF,s) = 0.

**Expected chunks:** ['04-Chapter-4---Analysis-of-Proportional.md#4.8 BOUNDED INPUT-BOUNDED OUTPUT STABILITY']

**Agent answer:**

Based on Section 4.8 of the knowledge base, here is the condition for BIBO stability of a PN guidance system:

## Definition
The PN guidance system is **BIBO stable** if for any bounded target acceleration, the miss distance *y(tF)* is bounded for all times of flight *tF* ∈ [0, ∞).

## Stability Condition (Theorem)
According to equation (4.64) in the text, the proportional navigation guidance system with transfer function *W(s)* is **BIBO stable if and only if**:

$$\sum_{k=1}^{l} B_k \tau_k + \sum_{j=1}^{m} \frac{C_j}{\omega_j} < \frac{1}{N}$$

Where:
- *τₖ* and *ωⱼ* are parameters of the missile guidance system
- *N* is the effective navigation ratio
- *Bₖ* and *Cⱼ* are coefficients of the partial fraction expansion of *W(s)/s*

## Key Result (Corollary)
Proportional navigation missile guidance systems with the standard transfer function structure are **BIBO stable for all** *rᵢ* (i = 1,…, n–1). This is because *H(s)* is a proper rational function where the degree of its numerator equals *n* – 1, which ensures the inequality above is always satisfied.

## Physical Interpretation
The stability condition requires that the inverse Laplace transform of *P(tF, s)* be absolutely integrable on [0,∞), which is equivalent to requiring that the transfer function *P(tF, s)* be analytic in the right half-plane (including the imaginary axis) with lim_{s→∞} *P(tF, s)* = 0.

**Your score:** 0.7

---

## 24. `q050` — `single_hop` — run:v5 — [CLEAN]

**Question:** What's the condition for BIBO stability of a PN guidance system?

**Reference answer:** The PN guidance system is BIBO stable if, for any bounded target acceleration, its miss y(tF) stays bounded for all flight times. The condition: the inverse Laplace transform of the transfer function P(tF,s) must be absolutely integrable on [0, infinity). Equivalently, P(tF,s) must be analytic in the right half-plane (including the imaginary axis) and lim as s goes to infinity of P(tF,s) = 0.

**Expected chunks:** ['04-Chapter-4---Analysis-of-Proportional.md#4.8 BOUNDED INPUT-BOUNDED OUTPUT STABILITY']

**Agent answer:**

According to **Section 4.8** of the textbook on analysis of proportional navigation guidance systems, here are the BIBO stability conditions:

## Definition
The PN guidance system is **BIBO stable** if for any bounded target acceleration, the miss distance *y(t_F)* is bounded for all times of flight *t_F* ∈ [0, ∞).

## Main Theorem
The proportional navigation guidance system with the transfer function *W(s)* is **BIBO stable if and only if** the following condition is satisfied:

$$\sum_{k=1}^{l} \frac{B_k}{\tau_k} - 2\sum_{j=1}^{m} \frac{C_j \zeta_j}{\omega_j} = N - 1$$

where:
- *τ_k* and *ω_j* are parameters of the missile guidance system
- *N* is the effective navigation ratio
- *B_k* and *C_j* are coefficients of the partial fraction expansion of *W(s)/s*
- *ζ_j* are damping coefficients

## Proof Outline
- **Necessity**: If the above equation does not hold, then lim_{s→∞} *P(t_F, s)* ≠ 0, contradicting the condition for existence of an inverse Laplace transform.
- **Sufficiency**: When the condition holds, the function *P(t_F, s)* is analytic in the region where Re *s* > –σ (where σ = min(1/τ_k, ζ_j ω_j)), meaning it is analytic in the right-half plane. This ensures that the inverse Laplace transform is absolutely integrable on [0,∞).

## Corollary
Proportional navigation missile guidance systems with the transfer function (4.29) are **BIBO stable for all r_i** (*i* = 1,…, *n* – 1). 

This is because *H(s)* is a proper rational function with numerator degree equal to *n* – 1. When presenting equation (4.30) in the form of (4.29), equating to zero the *n*-th power term of the numerator automatically satisfies the inequality of equation (4.64), making BIBO stability guaranteed for this class of PN guidance structures.

**Your score:** 0.7

---

## 25. `q051` — `single_hop` — run:v4 — [CLEAN]

**Question:** What is the 'miss step response' and why does it matter for evaluating a PN guidance system?

**Reference answer:** The miss step response is the miss distance due to a step target maneuver. It is analogous to the well-known step response in classical control theory and lets designers characterize and minimize miss distance in the time domain. Closed-form time-domain solutions exist only for simple models, not high-order ones with realistic autopilot and airframe dynamics.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.1 INTRODUCTION']

**Agent answer:**

Based on Section 4.7 of Chapter 4, I can provide you with a comprehensive explanation of the miss step response and its significance.

## What is the Miss Step Response?

The **miss step response** is the miss distance that results when the target performs a **step maneuver** (a sudden, sustained acceleration). Mathematically, it equals the integral of the system's impulse response:

$$\text{Miss Step Response} = \int_0^{t_F} P(t_F, t) \, dt$$

where:
- $P(t_F, t)$ is the impulse response of the guidance system
- $t_F$ is the flight time (time of interception)

The section shows that this step response can be computed directly from the **frequency response** of the guidance system using the key equation:

$$\text{Miss Step} = \frac{1}{\pi} \int_0^\infty \frac{\text{Re}[P(t_F, i\omega)]}{\omega} \, d\omega$$

## Why It Matters for Evaluating PN Guidance

The miss step response is crucial for evaluation because:

1. **Predicts Worst-Case Performance**: A step maneuver represents a target executing a sudden, constant acceleration. The resulting miss distance indicates how well the guidance system can handle rapid target maneuvers.

2. **Enables Frequency-Domain Analysis**: As demonstrated in Section 4.7, the miss step can be calculated directly from the system's frequency response without time-domain simulation. This provides a powerful analytical tool.

3. **Determines Flight Time Requirements**: The frequency response bandwidth $\omega_s$ characterizes how quickly miss distance decreases with flight time. The key design inequality is:

   $$t_F \geq \frac{4\pi}{\omega_s}$$

   This means if you know the system bandwidth from frequency analysis, you can estimate the minimum engagement time needed to achieve small miss distances against step maneuvers.

4. **Practical Validation**: Figure 4.11 in the text shows that miss values calculated via frequency analysis match simulation results closely, validating this as a reliable analysis method.

In summary, the miss step response provides an essential metric for assessing how PN guidance systems perform against target evasive maneuvers, and frequency-domain techniques allow designers to predict this behavior without exhaustive simulations.

**Your score:** 0.7

---

## 26. `q051` — `single_hop` — run:v5 — [CLEAN]

**Question:** What is the 'miss step response' and why does it matter for evaluating a PN guidance system?

**Reference answer:** The miss step response is the miss distance due to a step target maneuver. It is analogous to the well-known step response in classical control theory and lets designers characterize and minimize miss distance in the time domain. Closed-form time-domain solutions exist only for simple models, not high-order ones with realistic autopilot and airframe dynamics.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.1 INTRODUCTION']

**Agent answer:**

Based on my reading of Section 4.7 (Frequency Analysis and Miss Step Response) and Section 3.3 (Method of Adjuncts) in Chapter 3, I can provide a comprehensive answer.

---

## Definition of Miss Step Response

The **miss step response** is the miss distance at intercept that results from a **step target maneuver** — specifically, a constant target acceleration that begins at a specific time during the engagement. Mathematically, it is defined as the integral of the impulse response *P*(*t*<sub>F</sub>, *t*) of the guidance system:

$$m(t_F) = \int_0^{t_F} P(t_F, t)\, dt$$

where *t*<sub>F</sub> is the total flight time (intercept time).

---

## Why It Matters for Evaluating PN Guidance Systems

According to the text, the miss step response is **"one of the most used estimates of missile system performance"** and serves as an **important time-domain characteristic** for guidance system design for several reasons:

### 1. **Quantifies Effect of System Dynamics**
The miss step response reveals how the missile's flight control system dynamics — particularly time lags and time constants — affect terminal accuracy. Unlike the idealized inertialess PN model where miss distance is zero, real systems with dynamics (represented by time constants τ₁) exhibit non-zero miss distances that depend significantly on flight time.

### 2. **Enables Design Trade-offs Without Simulation**
The miss step response allows designers to **choose appropriate guidance parameters** (such as effective navigation ratio *N*, time constants, and autopilot gains) to minimize miss distance. As noted in Section 3.3: *"It is an important time-domain characteristic of missile guidance systems that allows designers to choose appropriate parameters of the missile guidance system to minimize the miss step."*

### 3. **Connection to Frequency Domain Analysis**
The frequency approach provides a powerful analytical relationship between the frequency response and miss step response:

$$m(t_F) = \frac{2}{\pi} \int_0^{\infty} \frac{\text{Re}[P(t_F, i\omega)]}{\omega} \sin(\omega t_F)\, d\omega$$

This enables engineers to **calculate the miss step response directly from the frequency response** without running time-domain simulations of the full nonlinear engagement model.

### 4. **Bandwidth-Based Flight Time Estimation**
The miss step response provides a practical design rule: if ω<sub>s</sub> is the system bandwidth frequency (determined from the real part of the frequency response), then for flight times satisfying:

$$t_F \geq \frac{4\pi}{\omega_s}$$

the miss distance becomes acceptably small. This gives system designers a direct way to estimate required engagement duration for a given guidance system bandwidth to achieve acceptable accuracy.

### 5. **Practical Performance Prediction**
As demonstrated in Figure 4.11 of the text, the miss step response calculated via frequency-domain methods matches simulation results closely, validating its use as a **predictive tool for evaluating PN guidance system performance** against maneuvering targets without extensive Monte Carlo simulation campaigns.

**Your score:** 0.7

---

## 27. `q052` — `multi_hop` — run:v4 — [CLEAN]

**Question:** How does the inertialess PN miss result from Chapter 3 connect to the rms miss distance for a realistic first-order system in Chapter 7?

**Reference answer:** The inertialess case (Ch3) is the idealized baseline: miss is zero for N > 2. Chapter 7 extends the analysis to realistic systems with a flight-control time constant, where miss is no longer zero — the rms miss becomes finite and depends on the system time constant and flight time.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.2 INERTIALESS PN GUIDANCE SYSTEM', '07-Chapter-7---Guidance-Law-Performance.md#7.7 EXAMPLES']

**Agent answer:**

Based on the knowledge base content, I can now synthesize the connection between these two concepts.

## Connection Between Inertialess PN Miss and RMS Miss Distance

The **inertialess PN miss** from Chapter 3 and the **rms miss distance for a first-order system** in Chapter 7 are connected through a progression from idealized theory to practical stochastic analysis:

### 1. The Inertialess Baseline (Chapter 3, Section 3.2)
The inertialess model represents the ideal case where missile acceleration equals commanded acceleration with no dynamic lag. For this idealized linearized model, **the miss distance is zero** for step target maneuvers when the effective navigation ratio N > 2. This serves as the theoretical lower bound—the best performance physically possible. As noted in Section 3.2, "the model of the missile guidance system considered above is too simple to immediately make too optimistic estimates of the PN law performance."

### 2. The First-Order Extension (Chapter 4 & 7)
When autopilot inertia is introduced via a **first-order lag** with time constant τ₁, the transfer function becomes:

**W(s) = 1/(τ₁s + 1)**

This is the foundation for the rms miss calculations in Chapter 7. According to Section 7.7, the analytical expressions for rms miss distance due to glint noise, independent-range noise, passive/active receiver noise, and random target maneuvers (equations 7.43, 7.46, and 7.48–7.51) are derived using the first-order model transfer function **P(t_F, s)** referenced in equations **(3.19)** and **(4.21)**.

### 3. The Key Connection: From Deterministic to Stochastic
The inertialess result informs the first-order rms analysis in two critical ways:

- **As τ → 0, the system approaches the inertialess case**: Section 7.7 explicitly states that "the decrease of the time constant makes it closer to the ideal inertialess case."

- **The adjoint method bridges both analyses**: The impulse response **P(t_F, τ)** derived via the adjoint method (Chapter 3, Section 3.3 and Chapter 4, Section 4.2) enables the frequency-domain rms calculations in Chapter 7. The adjoint system provides the transfer function **P(t_F, s)** that appears in the rms miss integrals.

### 4. Important Insight: Surprising Behavior vs. Ideal
Section 7.7 reveals a counter-intuitive result: while reducing τ brings the system closer to the inertialess ideal in deterministic analysis, for **glint noise** the rms miss distance actually **increases** as τ decreases. As stated: "the described effect can be predicted by analyzing equation (7.55) and the expression given above of the first-order system P(t_F, s)." This demonstrates that stochastic effects can produce behavior opposite to the deterministic ideal.

### Summary
The inertialess PN miss (zero miss for N > 2) represents the theoretical ideal. The rms miss distance formulas for the first-order system in Chapter 7 quantify how system lag (τ) degrades this ideal performance under realistic stochastic conditions—target maneuvers modeled as random processes and sensor noise. The first-order model provides analytical tractability while capturing the essential effect of finite bandwidth, with results showing that "in all considered cases the first-order system analysis gives a significantly lower miss estimate than a more realistic model."

**Your score:** 1.0

---

## 28. `q052` — `multi_hop` — run:v5 — [CLEAN]

**Question:** How does the inertialess PN miss result from Chapter 3 connect to the rms miss distance for a realistic first-order system in Chapter 7?

**Reference answer:** The inertialess case (Ch3) is the idealized baseline: miss is zero for N > 2. Chapter 7 extends the analysis to realistic systems with a flight-control time constant, where miss is no longer zero — the rms miss becomes finite and depends on the system time constant and flight time.

**Expected chunks:** ['03-Chapter-3---Analysis-of-Proportional.md#3.2 INERTIALESS PN GUIDANCE SYSTEM', '07-Chapter-7---Guidance-Law-Performance.md#7.7 EXAMPLES']

**Agent answer:**

Based on my reading of the relevant sections, I can now synthesize the connection between the inertialess PN miss result from Chapter 3 and the rms miss distance for a first-order system in Chapter 7.

## Connection Between Inertialess PN and First-Order System RMS Miss

### 1. The Inertialess PN Result (Chapter 3, Section 3.2)

The inertialess PN guidance system represents the idealized case where the missile acceleration instantaneously follows the commanded acceleration (no dynamics). For this model, the miss distance **y(t_F)** due to a step target maneuver is shown to be **zero** when the effective navigation ratio **N > 2**.

As stated in Section 3.2: *"the miss distance y(t_F) is zero (i.e., PN with the effective navigation ratio N > 2 is an effective way to hit a target)."*

This is the **baseline theoretical result**—with perfect (instantaneous) response, PN achieves perfect interception against step maneuvers.

### 2. The First-Order System (Chapter 7, Section 7.7)

When the guidance system includes a first-order lag with time constant **τ** (representing autopilot and airframe dynamics), the transfer function becomes **W(s) = 1/(τs + 1)**. The key connection is established through the **impulse response transfer function P(t_F, s)** from equation (3.19) and (4.10):

**P(t_F, s) = (τ²s²X(s))/(v_cl·t_go)**

where **X(s)** depends on the closed-loop dynamics involving **W(s)**.

### 3. The RMS Miss Distance Formulas (Chapter 7, Sections 7.4 and 7.7)

For the first-order system, the rms miss distance expressions (equations 7.43, 7.46, 7.48–7.51) are derived analytically. For example, the rms miss due to **glint noise** is:

**RMS miss = √(Φ_gn · ∫₀^∞ L⁻¹[P(t_F,s)]² dτ)**

The text explicitly notes the relationship to the inertialess case: *"the decrease of the time constant makes it closer to the ideal inertialess case"* (Section 7.7).

### 4. Key Insights from the Comparison

| Aspect | Inertialess (Chapter 3) | First-Order System (Chapter 7) |
|--------|------------------------|--------------------------------|
| **Transfer function** | W(s) = 1 (instantaneous) | W(s) = 1/(τs + 1) |
| **Step maneuver miss** | Zero for N > 2 | Non-zero (depends on τ and t_F) |
| **RMS noise miss** | Zero (perfect rejection) | Non-zero, given by equations (7.43), (7.46), etc. |

### 5. Important Non-Intuitive Result

Section 7.7 highlights a surprising finding: *"the described effect can look 'strange,' especially for the first-order model, because the decrease of the time constant makes it closer to the ideal inertialess case. However, the rms miss distance due to glint noise **increases** with the decrease of the flight control system time constant."*

This reveals that while the **deterministic** miss distance approaches zero as τ → 0 (approaching the inertialess case), the **stochastic** rms miss due to certain noise sources (like glint) can actually behave counter-intuitively.

### Summary

The inertialess PN result from Chapter 3 establishes the **theoretical limit** (zero miss against step maneuvers for N > 2). The rms miss distance analysis in Chapter 7 for the first-order system shows how **system dynamics (τ)** introduce non-zero miss in both deterministic and stochastic scenarios. The first-order model serves as a bridge between the ideal inertialess case and more realistic higher-order models containing complex-conjugated poles from the flight-control system damping and natural frequency.

**Your score:** 1.0

---

## 29. `q053` — `multi_hop` — run:v5 — [CLEAN]

**Question:** How does the Lyapunov approach to guidance design differ from the Bellman-functional approach to integrated guidance, in how each treats the problem?

**Reference answer:** The Lyapunov approach (Ch5) uses a Lyapunov function of the LOS rate and enforces negative-definiteness of its derivative to guarantee partial stability (asymptotic stability of the LOS rate). The Bellman-functional approach (Ch9) formulates the problem as minimizing a performance index over the full state vector, leading to a Bellman functional equation (or a state-dependent Riccati equation) that couples guidance and control.

**Expected chunks:** ['05-Chapter-5---Design-of-Guidance-Laws.md#5.3 LYAPUNOV APPROACH TO CONTROL LAW DESIGN', '09-Chapter-9---Integrated-Missile-Design.md#9.3.1 MINIMIZATION OF STANDARD FUNCTIONALS']

**Agent answer:**

Based on my reading of the relevant sections, here is how the **Lyapunov approach** to guidance design differs from the **Bellman-functional approach** to integrated guidance in how each treats the problem:

---

## Lyapunov Approach (Chapter 5, Section 5.3)

The Lyapunov approach treats guidance as a **stabilization problem** using a sufficient condition based on instantaneous rate of change:

**Core Principle:** If there exist positive definite functions \( Q(\mathbf{x}, t) \) and \( R(\mathbf{x}, t) \) such that the derivative \( \dot{Q} \) along any system trajectory satisfies:
$$\dot{Q} \leq -R(\mathbf{x}, t)$$

then the system is stabilized by control \( \mathbf{u} \) determined from this inequality.

**How it treats the problem:**
- **Instantaneous criterion:** It serves as an "instantaneous criterion" that ensures the system state moves toward the desired equilibrium (zero LOS rate) at each moment.
- **No explicit time integration:** The quality estimate does not include the time of control directly—it focuses only on ensuring \( \dot{Q} \) is negative definite at each instant.
- **Sufficient condition:** This is a sufficient (not necessary) condition for stability. The guidance law is derived by choosing \( Q \) and \( R \) forms that make the inequality satisfied.
- **Practical focus:** For parallel navigation, the only requirement is to get the LOS rate to zero "as soon as possible"—the \( \dot{Q} \) criterion reflects this requirement directly.

---

## Bellman-Functional Approach (Chapter 9, Sections 9.3.1–9.3.2; Appendix A.2)

The Bellman-functional approach treats guidance as an **optimization problem over a time horizon** using dynamic programming:

**Core Principle:** Based on the optimality principle that "every tail of the optimal trajectory is the optimal trajectory," it minimizes a cost functional:
$$J = \int_{t_0}^{t_F} L(\mathbf{x}(t), \mathbf{u}(t), t) \, dt + V_0(\mathbf{x}(t_F))$$

**How it treats the problem:**
- **Time-integrated performance:** The objective involves integrating a cost over the entire engagement interval, with both running costs \( L(\mathbf{x}, \mathbf{u}, t) \) and terminal costs \( V_0(\mathbf{x}(t_F)) \).
- **Bellman functional equation:** The optimal control satisfies a partial differential equation (the Bellman equation):
$$\min_{\mathbf{u}} \left\{ L(\mathbf{x}, \mathbf{u}, t) + \frac{\partial V}{\partial \mathbf{x}} \mathbf{f}(\mathbf{x}, \mathbf{u}, t) \right\} = -\frac{\partial V}{\partial t}$$
- **Globally optimal over horizon:** The solution guarantees optimality over the complete time interval, not just local stability at each instant.

---

## Key Differences in Problem Treatment

| Aspect | Lyapunov Approach | Bellman-Functional Approach |
|--------|-------------------|----------------------------|
| **Primary objective** | Ensure stability (negative definiteness of \( \dot{Q} \)) | Minimize integral cost functional over time |
| **Time consideration** | Instantaneous rate of change | Integrated performance over \( [t_0, t_F] \) |
| **Mathematical foundation** | Lyapunov stability theory | Dynamic programming / Bellman optimality principle |
| **Equation type** | Algebraic inequality ( \( \dot{Q} \leq -R \) ) | Nonlinear PDE (Bellman functional equation) |
| **Solution difficulty** | Finding appropriate \( Q \) and \( R \) forms | Solving complex partial differential equations |
| **Optimality** | Stabilizing (sufficient condition) | Optimal over the time horizon |
| **Terminal conditions** | Not explicitly enforced | Explicitly included via \( V_0(\mathbf{x}(t_F)) \) |

---

## The "Special Functionals" Variant (Section 9.3.2)

Interestingly, the text presents a hybrid approach for integrated guidance that bridges the two: by using **special functionals** that include an unknown optimal control \( \mathbf{u}_0 \), the problem reduces to solving a **Lyapunov equation for the uncontrolled system** rather than the full Bellman equation:

$$-\frac{\partial V}{\partial t} = \frac{\partial V}{\partial \mathbf{x}} \mathbf{f}(\mathbf{x}, t) + R(\mathbf{x}, t)$$

This yields optimal control laws requiring significantly fewer computations than standard Bellman functionals, while still achieving optimality over the interval—offering a computationally tractable middle ground for integrated guidance and control design.

**Your score:** 1.0

---

## 30. `q054` — `multi_hop` — run:v4 — [PRIMED]

**Question:** When you take the PN law from Chapter 2 and drop it into the 3-DOF simulation model in Chapter 8, what extra step is needed to use the commanded acceleration?

**Reference answer:** The PN law outputs a commanded acceleration in an inertial/NED frame, but in the 3-DOF model the thrust acts along the body axis. The model must determine the angle of attack (the corpus uses regression models from the aerodynamic coefficients) to resolve the commanded acceleration onto the body axes — an iterative step not present in the idealized PN derivation.

**Expected chunks:** ['02-Chapter-2---Parallel-Navigation.md#2.2 PROPORTIONAL NAVIGATION. PLANAR ENGAGEMENT', '08-Chapter-8---Testing-Guidance-Laws.md#8.9.2 3-DOF SIMULATION MODEL']

**Agent answer:**

Based on my reading of **Section 8.9.2 (3-DOF Simulation Model)** in Chapter 8, the extra step needed is:

**The commanded acceleration must be resolved into components along and orthogonal (normal) to the missile velocity vector** (and subsequently normal to the missile body axis).

Here's the specific process described in the text:

1. **Projection onto velocity vector**: The commanded acceleration **a**_c_ = (_a__c1_, _a__c2_, _a__c3_) from the guidance law is projected onto the unit velocity vector **e**_M_ to obtain _a__L_ (the component along the velocity vector):
   - Equation (8.74) computes this scalar projection: _a__L_ = **a**_c_ · **e**_M_
   - Equation (8.75) gives the vector projection **a**_L_

2. **Component normal to velocity**: The acceleration normal to the velocity vector **a**_cN_ is computed by subtracting the parallel component:
   - Equation (8.76): **a**_cN_ = **a**_c_ − **a**_L_

3. **Component normal to body axis**: The unit vector orthogonal to the velocity vector **e**_LN_ is calculated (equation 8.77), and then the commanded acceleration normal to the missile body **a**_cBN_ is obtained (equations 8.78–8.80).

This resolution is necessary because in the 3-DOF model, different acceleration components act in different directions—thrust acts along the body axis, the controlled part of commanded acceleration acts orthogonal to the body, and drag acts along the velocity vector. Without decomposing the PN law's commanded acceleration into these directional components, it cannot be properly combined with thrust and drag in the equations of motion (equation 8.82).

**Your score:** 0.4

---

## 31. `q055` — `multi_hop` — run:v4 — [CLEAN]

**Question:** Why does neoclassical guidance suppress receiver noise but not glint noise?

**Reference answer:** Neoclassical guidance achieves zero miss distance (ZMD), which eliminates the contribution of range-independent and range-dependent receiver noises to the miss. Glint noise behaves differently: as flight time increases its transfer to the miss does not vanish, so the rms miss ends up dominated by the glint noise contribution.

**Expected chunks:** ['06-Chapter-6---Design-of-Guidance-Laws.md#6.2 NEOCLASSICAL MISSILE GUIDANCE', '07-Chapter-7---Guidance-Law-Performance.md#7.4 ANALYSIS OF INFLUENCE OF NOISES ON MISS DISTANCE']

**Agent answer:**

I now have the answer from Section 7.4. Let me synthesize this for you.

According to **Section 7.4 "Analysis of Influence of Noises on Miss Distance"** in Chapter 7, neoclassical guidance suppresses receiver noise but not glint noise due to fundamental differences in how these noise sources propagate through the guidance system:

## Why Receiver Noise is Suppressed

Neoclassical guidance is designed such that the impulse response to target maneuvers becomes zero: **P_T(t_F, s) = 0** (see equations 4.10, 6.1, 6.4, and 6.5). 

The rms miss distance expressions for receiver noise contain this P_T term directly:

- **Range-independent noise** (eq. 7.46): The rms miss is proportional to the derivative of P_T(t_F, s)
- **Passive-receiver noise** (eq. 7.47): Proportional to P_T(t_F, s)  
- **Active-receiver noise** (eq. 7.48): Also proportional to P_T(t_F, s)

Since neoclassical guidance forces **P_T(t_F, s) = 0**, the influence of all receiver noise types on miss distance is **eliminated entirely**.

## Why Glint Noise is NOT Suppressed

Glint noise enters the system differently. The impulse response for glint noise P_g(t_F, s) is derived from a different transfer function relationship (eq. 7.43):

$$P_g(t_F, s) = \frac{1}{s^2 v_{cl}\tau} \cdot \frac{1}{1 + N v_{cl} W(s)/s}$$

For **long flight times** (t_F → ∞), the right-hand side of equation (7.43) approaches **1**. This means:

$$\lim_{t_F \to \infty} P_g(t_F, s) \approx 1$$

Since the glint noise transfer function does not contain the P_T term that neoclassical guidance nullifies, glint continues to contribute to miss distance. The rms miss due to glint (eq. 7.42) remains significant regardless of the guidance law's zero-P_T design.

## Key Takeaway

The structural difference lies in the signal paths: receiver noises propagate through the target maneuver response channel (which neoclassical guidance cancels), while glint enters through the line-of-sight measurement directly and bypasses the mechanism that makes P_T = 0.

**Your score:** 1.0

---

## 32. `q056` — `multi_hop` — run:v4 — [PRIMED]

**Question:** How do the line-of-sight angles defined in Chapter 1 relate to the seeker gimbal angles in the Chapter 8 seeker model?

**Reference answer:** The LOS direction in Chapter 1 is specified geometrically in an inertial/NED frame. To point the seeker, that LOS direction is transformed into the missile body frame using the body Euler angles, then into the seeker frame via the seeker gimbal rotations, so the seeker boresight aligns with the target. The Chapter 8 seeker model adds real-effects like radome refraction on top of this geometry.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.5 LINE-OF-SIGHT', '08-Chapter-8---Testing-Guidance-Laws.md#8.6 SEEKER MODEL']

**Agent answer:**

Based on my search of the knowledge base, I can now synthesize the relationship between the line-of-sight angles from Chapter 1 and the seeker gimbal angles in Chapter 8.

## Relationship Between LOS Angles (Chapter 1) and Seeker Gimbal Angles (Chapter 8)

### Chapter 1: LOS Angle Definitions

According to **Section 1.5 (LINE-OF-SIGHT)** in Chapter 1, the three-dimensional LOS is characterized by two angles with respect to the Earth-based coordinate system:
- **Azimuth angle α**: The LOS position in the horizontal (northeast) plane
- **Elevation angle β**: The LOS position in the vertical plane

These angles define the LOS vector components (λ₁, λ₂, λ₃) through the following equations (1.9):
- λ₁ = cos α cos β
- λ₂ = sin α cos β  
- λ₃ = sin β

### Chapter 8: Seeker Gimbal Angles

According to **Section 8.6 (SEEKER MODEL)**, the seeker is mounted on gimbals with:
- **Yaw gimbal angle ψₛ**: Rotation about the seeker's yaw axis
- **Pitch gimbal angle θₛ**: Rotation about the seeker's pitch axis

When the seeker boresight axis **xₛ** coincides with the missile body **x** axis (gimbal angles at zero), the seeker axes align with the missile body axes. The transformation from missile body axes to seeker axes follows the Euler angle sequence: **yaw, pitch, and zero roll (ψₛ, θₛ, 0)**.

### The Direct Relationship

The critical connection is stated explicitly in Chapter 8: *"This corresponds to such a seeker's platform that it tracks the target in **azimuth and elevation**."*

**The seeker gimbal angles (ψₛ, θₛ) directly correspond to the LOS angles (α, β) defined in Chapter 1:**

| Chapter 1 LOS Angle | Chapter 8 Gimbal Angle | Function |
|---------------------|------------------------|----------|
| Azimuth angle α | Yaw gimbal angle ψₛ | Tracks target in the horizontal plane |
| Elevation angle β | Pitch gimbal angle θₛ | Tracks target in the vertical plane |

### Seeker Tracking Operation

The seeker senses the **LOS error** in two orthogonal components:
- **Azimuth error αₑₛ** = tan⁻¹(Rᵧₛ/Rₓₛ): Measured along the **yₛ** axis (yaw seeker axis)
- **Elevation error θₑₛ** = tan⁻¹(−Rᵤₛ/Rₓₛ): Measured along the **zₛ** axis (pitch seeker axis)

These error signals drive the gimbal control system to align the seeker boresight with the LOS. When the gimbal angles (ψₛ, θₛ) match the LOS angles (α, β), the LOS errors tend to zero and the seeker successfully tracks the target.

### Summary

The line-of-sight angles (azimuth α and elevation β) defined in Chapter 1 represent the **geometric orientation** of the LOS in inertial space. The seeker gimbal angles (yaw ψₛ and pitch θₛ) in Chapter 8 are the **physical control variables** that the seeker uses to align its boresight with that LOS. The seeker's function is to drive ψₛ → α and θₛ → β, thereby keeping the target centered in its field of view.

**Your score:** 0.4

---

## 33. `q056` — `multi_hop` — run:v5 — [PRIMED]

**Question:** How do the line-of-sight angles defined in Chapter 1 relate to the seeker gimbal angles in the Chapter 8 seeker model?

**Reference answer:** The LOS direction in Chapter 1 is specified geometrically in an inertial/NED frame. To point the seeker, that LOS direction is transformed into the missile body frame using the body Euler angles, then into the seeker frame via the seeker gimbal rotations, so the seeker boresight aligns with the target. The Chapter 8 seeker model adds real-effects like radome refraction on top of this geometry.

**Expected chunks:** ['01-Chapter-1---Basics-of-Missile-Guidance.md#1.5 LINE-OF-SIGHT', '08-Chapter-8---Testing-Guidance-Laws.md#8.6 SEEKER MODEL']

**Agent answer:**

[Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Your score:** 0.0

---

## 34. `q060` — `ambiguous` — run:v4 — [PRIMED]

**Question:** What time constant should I use in my guidance model?

**Reference answer:** The system should recognize that 'time constant' is overloaded across the corpus and either ask which one the user means or surface the alternatives. Distinct senses include: the single guidance-system / flight-control time constant in the first-order PN model (Ch3-4), the autopilot lag time constant (Ch8 autopilot models), the seeker time constant (Ch8 seeker model), and the actuator time constant (Ch8 actuator models). Each enters the miss-distance analysis differently. Silently committing to one — typically the first-order guidance time constant, the most BM25-retrievable — without surfacing the ambiguity is a failure.

**Expected chunks:** (none — no_answer/ambiguous)

**Agent answer:**

Your question contains some ambiguity that affects the answer. The appropriate time constant depends on **what aspect of the guidance system** you're modeling:

## Clarification Needed

**Are you asking about:**
1. **Flight control system time constant** (τ₁ = τ) — representing actuator/autopilot dynamics?
2. **A first-order guidance system approximation** — a simplified overall model?
3. **Seeker/filter dynamics** — sensor-related time constants?
4. **A specific missile type and flight condition** — aerodynamic missile at high altitude, tail-controlled, etc.?

---

## Guidance from the Knowledge Base

Based on the corpus, here are representative values:

### For Third-Order Flight Control Models (Realistic)
According to **Section 4.6** (Chapter 4), a realistic example for a **tail-controlled aerodynamic missile at high altitude** uses:
- **Flight control system time constant: τ = 0.5 s**
- Damping: ζ = 0.7
- Natural frequency: ω_M = 20 rad/s
- Right-half plane zero: ω_z = 5 rad/s (at high altitude)

**Table 4.1** (Chapter 4) shows a parametric study with **τ ranging from 0.2 s to 0.7 s**, demonstrating that:
- τ = 0.2 s produces severely degraded performance (peak miss distance = 22,100 m)
- τ = 0.5–0.7 s yields significantly better results (peak miss distances of 115–234 m depending on other parameters)

### Important Caveat on Model Fidelity
As noted in **Section 4.1** (Chapter 4): *"The disadvantage of the single time constant representation of a missile guidance system is that the miss distance can be seriously underestimated."* 

If you're using a first-order model for preliminary analysis, be aware that results can be misleading compared to more realistic third-order representations.

---

**Which guidance system component are you modeling, and what is your application context?** This will help determine whether τ ≈ 0.5 s is appropriate or if you need a different value.

**Your score:** 1.0

---

## 35. `q060` — `ambiguous` — run:v5 — [PRIMED]

**Question:** What time constant should I use in my guidance model?

**Reference answer:** The system should recognize that 'time constant' is overloaded across the corpus and either ask which one the user means or surface the alternatives. Distinct senses include: the single guidance-system / flight-control time constant in the first-order PN model (Ch3-4), the autopilot lag time constant (Ch8 autopilot models), the seeker time constant (Ch8 seeker model), and the actuator time constant (Ch8 actuator models). Each enters the miss-distance analysis differently. Silently committing to one — typically the first-order guidance time constant, the most BM25-retrievable — without surfacing the ambiguity is a failure.

**Expected chunks:** (none — no_answer/ambiguous)

**Agent answer:**

Based on my reading of the relevant sections, your question requires clarification because the appropriate time constant depends on several system parameters.

## Clarification Needed

The knowledge base shows that the flight control system time constant **τ** is highly dependent on:

1. **Airframe zero frequency (ω_z)**: At high altitudes where ω_z is low (e.g., 5 rad/s), decreasing τ can actually *increase* miss distance. At lower altitudes with higher ω_z, decreasing τ reduces miss distance.

2. **System dynamics**: The natural frequency ω_M and damping ζ interact with τ.

3. **Engagement scenario**: Different scenarios in the text use different values:
   - High-altitude tail-controlled missile: **τ = 0.5 s** (with ω_M = 20 rad/s, ζ = 0.7, ω_z = 5 rad/s)
   - Weaving target engagement: **τ = 0.1 s** (with ω_M = 5 rad/s, ζ = 0.65, ω_z = 30 rad/s)
   - Generic engagement model: **τ = 0.5 s** (with ω_M = 20 rad/s, ζ = 0.7, ω_z = 30 rad/s)

## What the Analysis Shows (Section 4.4 / Table 4.1)

| τ (s) | ω_z (rad/s) | Peak Miss (m) | Notes |
|-------|-------------|---------------|-------|
| 0.2 | 5 | 22,100 | Very large miss due to low ω_z |
| 0.5 | 5 | 234 | Reduced miss |
| 0.5 | 20 | 3.4 | Much smaller miss at higher ω_z |
| 0.5 | 100 | 2.8 | Further improvement |

**Key insight from Section 4.4**: "The decrease of the flight control system time constant τ increases the miss" when ω_z is low (high altitude). "For lower altitudes (i.e., for higher values of ω_z), the maximum miss decreases with the decrease of τ."

---

**Could you specify:**
- Your missile type (tail-controlled, aerodynamic, etc.)?
- Operating altitude (affects ω_z)?
- Natural frequency ω_M and damping ζ of your flight control system?
- Expected target maneuver characteristics?

With these details, I can point you to the relevant example parameters or analysis results in the text.

**Your score:** 0.5

---
