# High-Yield Content Analysis

## High Yield (Core Concepts & Definitions)

**Reinforcement Learning (RL) Distinctions:**
*   **vs. Supervised Learning:** RL uses **Evaluative Feedback** (how good the action was), not **Instructive Feedback** (the correct action). Requires **Active Exploration** (trial-and-error).
*   **vs. Unsupervised Learning:** RL maximizes a **Reward Signal**; Unsupervised Learning finds hidden structure.

**Fundamental Components & Hypothesis:**
*   **Reward Hypothesis:** All goals can be described by the **maximization of expected total reward**.
*   **Core Elements:** Agent, Environment, Action ($a_t$), Observation, Reward ($r_t$).
*   **Markov State:** A state $s_t$ is Markov if the future is independent of the past given the present:
    $$\text{P} [s_{t+1} | s_t] = \text{P} [s_{t+1} | s_0, \dots, s_t]$$

**Policy ($pi$):** Agent's behavior; map from state to action.
*   **Deterministic:** $a = \pi(s)$
*   **Stochastic:** $\pi(a | s) = \text{P} [A_t = a | S_t = s]$

**Value Function ($v_pi(s)$):** Predicts long-run future reward (goodness of a state).
*   $$v_\pi(s) = E_\pi[r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \dots | S_t = s]$$

## Medium Yield (Formulas & Supporting Concepts)

**Reward Signals:**
*   **Total Future Reward ($G_t$):** $$G_t = \sum_{i=t+1}^{\infty} r_i$$ (May not converge).
*   **Discounted Total Reward ($G_t$):** $$G_t = \sum_{i=t+1}^{\infty} \gamma^{i-t-1}r_i$$ where $\gamma \in [0, 1]$ is the discount rate.

**Model:** Predicts what the environment will do next:
*   Predicts next state ($P$).
*   Predicts next immediate reward ($R$).

**History ($H_t$):** Sequence of all observable variables up to time $t$: $s_0, a_0, r_0, s_1, a_1, r_1, \dots, s_t$.

## Low Yield (Context & Examples)

*   **Multidisciplinary:** RL draws from control theory, psychology, and computer science.
*   **Agent vs. Environment State:** Agent state ($s_t$) may not match environment state ($s^e_t$) (e.g., Poker vs. Chess).
*   **Key Success Areas (For context/application knowledge):**
    *   Games: Checkers (Samuel), Backgammon (TD($\lambda$)), Go (AlphaGo).
    *   Robotics/Control: Autonomous Helicopter Flight, Mobile Robots.
    *   Deep RL Milestones: Atari Games (Deep Q-Networks).
    *   Finance: Option Pricing/Hedging, Optimal Execution.