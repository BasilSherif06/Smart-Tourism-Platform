import numpy as np
from stable_baselines3 import PPO
from tourism_env import TourismDisruptionEnv

# 1. Initialize your custom simulator
env = TourismDisruptionEnv()

# 2. Create the PPO agent with TensorBoard logging enabled
# verbose=1 prints live training stats in your terminal every 2,048 steps
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log="./ppo_tensorboard/",
    seed=42,
)

# 3. Train for 50,000 steps (~10,000 simulated vacations, takes ~20-30s on RTX 3060)
print("Starting PPO training...")
model.learn(total_timesteps=50_000, tb_log_name="ppo_v1_baseline")

# 4. Save the trained Actor weights
model.save("ppo_tourism_v1")
print("\nSaved model to ppo_tourism_v1.zip")

# 5. Post-Training Diagnosis: Test on 500 fresh trips to check for reward hacking
action_counts = {0: 0, 1: 0, 2: 0, 3: 0}
total_rewards = []

for _ in range(500):
    obs, _ = env.reset()
    done = False
    ep_reward = 0.0
    while not done:
        # deterministic=True picks the agent's #1 highest-probability button
        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        action_counts[action] += 1
        obs, reward, terminated, truncated, _ = env.step(action)
        ep_reward += reward
        done = terminated or truncated
    total_rewards.append(ep_reward)

total_steps = sum(action_counts.values())
print(f"\n--- 500-Trip Evaluation Summary ---")
print(f"Mean Episode Reward: {np.mean(total_rewards):.2f}")
for act, count in action_counts.items():
    pct = (count / total_steps) * 100
    print(f"Action {act}: {count} times ({pct:.1f}%)")