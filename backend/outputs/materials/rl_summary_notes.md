# High-Yield Content Analysis

## I. High Yield (Exam Critical)

### A. RL Definition & Distinction
*   **Reinforcement Learning (RL):** Multidisciplinary learning where training information **evaluates** actions, not instructs the correct one.
*   **Evaluative Feedback:** Points out *how good* the action was, but not *what the best action* should have been.
*   **Key Requirement:** Active **exploration** (trial-and-error search for good behavior).
*   **Vs. Supervised Learning (SL):** SL uses *instructive* feedback (tells correct action). RL uses *evaluative* feedback.
*   **Vs. Unsupervised Learning (UL):** RL maximizes a **reward signal**; UL finds hidden structure.

### B. Core Elements (Agent-Environment Interaction)
*   **Agent:** Takes actions.
*   **Environment:** The world the agent operates in.
*   **Action ($a_t$):** Move made by the agent.
*   **Observation:** Information about the environment after an action.
*   **State ($s_t$):** The situation perceived by the agent (may differ from environment state $s^e_t$).
*   **Reward ($r_t$):** Feedback measuring success/failure; defines the problem goal.

### C. Fundamental Concepts & Goals
*   **Reward Hypothesis:** All goals can be described by the **maximization of expected total reward**.
*   **Policy ($pi$):** Agent’s behavior; a map from state to action.
    *   Deterministic: $a = pi(s)$
    *   Stochastic: $pi(a | s) = P [A_t = a | S_t = s]$
*   **Value Function ($v_pi(s)$):** Prediction of **future reward**; evaluates long-run goodness of a state.
    *   **Formula:** $v_pi(s) = E_pi[r_t + gamma r_{t+1} + gamma^2 r_{t+2} + dots | S_t = s]$
*   **Markov State:** Future is independent of the past given the present: $P [s_{t+1} | s_t ] = P [s_{t+1} | s_0, dots, s_t ]$.

## II. Medium Yield (Important Definitions/Formulas)

### A. Reward Accumulation
*   **Total Reward ($G_t$):** Sum of future rewards (may not converge).
    *   **Formula:** $G_t = sum_{i=t+1}^{infty} r_i$
*   **Discounted Total Reward ($G_t$):** Incorporates discount factor $gamma$.
    *   **Formula:** $G_t = sum_{i=t+1}^{infty} gamma^{i-t-1}r_i$, where $gamma in [0, 1]$.

### B. Model & History
*   **Model:** Predicts what the environment will do next ($P$ predicts next state, $R$ predicts next reward).
*   **History ($H_t$):** Sequence of all observable variables: $s_0, a_0, r_0, s_1, a_1, r_1, dots, s_t$.

### C. Key Successes (Contextual Knowledge)
*   **Early Successes:** Checkers (Samuel), Backgammon (TD-Gammon, used TD($lambda$)).
*   **Modern Successes:** Go (AlphaGo/AlphaGo Zero), Atari Games (Deep Q-Networks), Financial Applications (Hedging, Optimal Execution), Data Center Cooling Optimization.