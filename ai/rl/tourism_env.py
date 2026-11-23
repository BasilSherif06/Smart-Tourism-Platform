import gymnasium as gym
from gymnasium import spaces
import numpy as np


class TourismDisruptionEnv(gym.Env):
    """Multi-day tourism disruption simulator for RL magnitude selection."""

    def __init__(self, max_days: int = 5):
        super().__init__()
        self.max_days = max_days

        # 4 discrete choices: 0=No Change, 1=Minor, 2=Moderate, 3=Full Re-plan
        self.action_space = spaces.Discrete(4)

        # 7 normalized state metrics, all strictly bounded in [0.0, 1.0]
        # [severity, category, days_left, affected_stops, budget_left, pacing, time_overlap]
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(7,),
            dtype=np.float32,
        )

        # Internal trip trackers (populated in reset)
        self.state = None
        self.current_day = 1
        self.total_days = max_days
        self.budget_left = 1.0
        self.pacing = 0.5

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # 1. Spawn a brand-new random vacation (3 to 7 days)
        self.total_days = int(self.np_random.integers(3, 8))
        self.current_day = 1
        self.budget_left = float(self.np_random.uniform(0.5, 1.0))
        self.pacing = float(self.np_random.uniform(0.1, 1.0))

        # 2. Inject the first disruption of the trip
        self.state = self._generate_disruption()

        return self.state, {}

    def _generate_disruption(self) -> np.ndarray:
        # 1. Pick a random disruption severity & category
        severity = float(self.np_random.uniform(0.1, 1.0))
        category = float(self.np_random.choice([0.0, 0.33, 0.66, 1.0]))

        # 2. Calculate remaining days percentage from our trip clock
        days_left = (self.total_days - self.current_day) / self.total_days

        # 3. Time window overlap (30% chance it happens at 3 AM while sleeping -> 0 overlap)
        if self.np_random.random() < 0.30:
            time_overlap = 0.0
            affected_stops = 0.0
        else:
            time_overlap = float(np.clip(severity * self.np_random.uniform(0.6, 1.2), 0.1, 1.0))
            # Scale affected stops (0.25 per stop, out of 4 stops/day)
            raw_stops = int(np.ceil(severity * 4 * self.np_random.uniform(0.5, 1.0)))
            affected_stops = float(np.clip(raw_stops * 0.25, 0.25, 1.0))

        return np.array(
            [
                severity,
                category,
                days_left,
                affected_stops,
                self.budget_left,
                self.pacing,
                time_overlap,
            ],
            dtype=np.float32,
        )

    def step(self, action: int):
        severity, category, days_left, affected_stops, budget_left, pacing, time_overlap = self.state
        broken_stops = round(affected_stops * 4)

        # 1. Apply the chosen action (0=None, 1=Minor, 2=Moderate, 3=Full)
        if action == 0:
            stops_fixed = 0
            budget_cost = 0.0
            change_penalty = 0.0
        elif action == 1:
            stops_fixed = min(broken_stops, 1)
            budget_cost = 0.03
            change_penalty = 1.5
        elif action == 2:
            stops_fixed = min(broken_stops, 3)
            budget_cost = 0.08
            change_penalty = 4.0
        else:  # action == 3
            stops_fixed = broken_stops
            budget_cost = 0.18
            change_penalty = 8.0

        # 2. Calculate the 3-part reward score
        unresolved_stops = broken_stops - stops_fixed
        fix_score = stops_fixed * (4.0 + 4.0 * severity)
        unresolved_pain = unresolved_stops * (4.0 + 3.0 * pacing)
        low_budget_penalty = 6.0 if (budget_cost > 0 and self.budget_left < 0.20) else 0.0

        reward = float(fix_score - change_penalty - unresolved_pain - low_budget_penalty)

        # 3. Update the trip's backpack & advance the calendar
        self.budget_left = float(np.clip(self.budget_left - budget_cost, 0.0, 1.0))
        self.current_day += 1

        # 4. Check if the vacation is over
        terminated = bool(self.current_day > self.total_days)
        truncated = False

        if not terminated:
            self.state = self._generate_disruption()

        return self.state, reward, terminated, truncated, {}


if __name__ == "__main__":
    from stable_baselines3.common.env_checker import check_env

    env = TourismDisruptionEnv()
    check_env(env, warn=True)
    print("Environment passed all Gymnasium & SB3 checks!")