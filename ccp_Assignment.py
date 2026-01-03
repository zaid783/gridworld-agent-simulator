import random
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from datetime import datetime
from PIL import Image
import io

# Create output directory for saving GUI results
OUTPUT_DIR = "gui_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# Environment Settings
# -------------------------------
GRID_SIZE = 4
START_STATE = (0, 0)
GOAL_STATE = (3, 3)
ACTIONS = ["up", "down", "left", "right"]

# -------------------------------
# Rewards
# -------------------------------
def get_reward(state):
    if state == GOAL_STATE:
        return 1
    else:
        return -1  # All non-goal states (including START) give -1


# -------------------------------
# Movement Logic
# -------------------------------
def move(state, action):
    x, y = state

    if action == "up":
        x = max(0, x - 1)
    elif action == "down":
        x = min(GRID_SIZE - 1, x + 1)
    elif action == "left":
        y = max(0, y - 1)
    elif action == "right":
        y = min(GRID_SIZE - 1, y + 1)

    return (x, y)


# -------------------------------
# Matplotlib Grid Visualization
# -------------------------------
def draw_grid(agent_state, step, episode, total_reward):
    plt.clf()

    grid = np.ones((GRID_SIZE, GRID_SIZE, 3)) * 0.95

    grid[START_STATE] = [0.2, 0.8, 0.2]     # Start
    grid[GOAL_STATE] = [0.9, 0.2, 0.2]      # Goal
    grid[agent_state] = [0.2, 0.3, 0.9]     # Agent

    plt.imshow(grid)

    plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
    plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
    plt.grid(color="black", linewidth=1.5)
    plt.xticks([])
    plt.yticks([])

    # Cell text
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) == START_STATE:
                text, color = "S\n0", "black"
            elif (i, j) == GOAL_STATE:
                text, color = "G\n+1", "white"
            else:
                text, color = "-1", "black"

            if (i, j) == agent_state:
                text, color = "A", "white"

            plt.text(j, i, text,
                     ha="center", va="center",
                     fontsize=12, fontweight="bold",
                     color=color)

    # Top info bar
    plt.title(
        f"Episode: {episode}   |   Step: {step}   |   Total Reward: {total_reward}",
        fontsize=14, fontweight="bold"
    )

    plt.pause(0.3)


# -------------------------------
# Capture Frame Function
# -------------------------------
def capture_frame(agent_state, step, episode, total_reward, mode_name):
    """Capture the current grid state as a PIL Image for GIF creation"""
    fig = plt.figure(figsize=(6, 6))
    
    grid = np.ones((GRID_SIZE, GRID_SIZE, 3)) * 0.95

    grid[START_STATE] = [0.2, 0.8, 0.2]     # Start
    grid[GOAL_STATE] = [0.9, 0.2, 0.2]      # Goal
    grid[agent_state] = [0.2, 0.3, 0.9]     # Agent

    plt.imshow(grid)

    plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
    plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
    plt.grid(color="black", linewidth=1.5)
    plt.xticks([])
    plt.yticks([])

    # Cell text
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) == START_STATE:
                text, color = "S\n0", "black"
            elif (i, j) == GOAL_STATE:
                text, color = "G\n+1", "white"
            else:
                text, color = "-1", "black"

            if (i, j) == agent_state:
                text, color = "A", "white"

            plt.text(j, i, text,
                     ha="center", va="center",
                     fontsize=12, fontweight="bold",
                     color=color)

    # Top info bar
    plt.title(
        f"{mode_name} | Episode: {episode} | Step: {step} | Total Reward: {total_reward}",
        fontsize=14, fontweight="bold"
    )

    # Convert figure to PIL Image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    plt.close(fig)
    
    return img


# -------------------------------
# Save Frames as GIF
# -------------------------------
def save_gif(frames, episode, mode_name, duration=500):
    
    if not frames:
        print("⚠️ No frames to save!")
        return
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/{mode_name}_episode_{episode}_{timestamp}.gif"
    
    # Save frames as GIF
    # Add the last frame multiple times to pause at the end
    extended_frames = frames + [frames[-1]] * 3  # Pause on last frame
    
    extended_frames[0].save(
        filename,
        save_all=True,
        append_images=extended_frames[1:],
        duration=duration,
        loop=0  # 0 means infinite loop
    )
    
    print(f"🎬 GIF saved to: {filename}")
    print(f"   - Total frames: {len(frames)}")
    print(f"   - Frame duration: {duration}ms")


# -------------------------------
# Input Helpers
# -------------------------------
def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if min_value is not None and value < min_value:
            print(f"Please enter a value >= {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a value <= {max_value}.")
            continue

        return value


# -------------------------------
# Stochastic Mode
# -------------------------------
def stochastic_mode(episodes, iterations_per_episode):
    plt.figure("Stochastic GridWorld")

    for ep in range(1, episodes + 1):
        state = START_STATE
        total_reward = 0
        frames = []  # List to store frames for this episode

        print(f"\nEpisode {ep} started")
        
        # Capture initial state
        frames.append(capture_frame(state, 0, ep, total_reward, "Stochastic"))

        for step in range(1, iterations_per_episode + 1):
            draw_grid(state, step, ep, total_reward)

            action = random.choice(ACTIONS)
            next_state = move(state, action)
            reward = get_reward(next_state)

            total_reward += reward
            state = next_state

            # Capture frame after each step
            frames.append(capture_frame(state, step, ep, total_reward, "Stochastic"))

            print(f"Step {step}: {state}, Reward: {reward}, Total: {total_reward}")

            if state == GOAL_STATE:
                draw_grid(state, step, ep, total_reward)
                print(f"🎯 Goal Reached! Episode {ep} Total Reward: {total_reward}")
                break

        # Save all frames as GIF after episode finishes
        save_gif(frames, ep, "Stochastic")
        print(f"📊 Episode {ep} Final Total Reward: {total_reward}")

    plt.close()




# -------------------------------
# Episodic (Deterministic) Mode
# -------------------------------
HARDCODED_EPISODES = {
    1: ["right", "right", "right", "down", "down", "down"],
    2: ["down", "down", "down", "right", "right", "right"],
    3: ["right", "down", "right", "down", "right", "down"]
}


def episodic_mode(choice):
    plt.figure("Episodic GridWorld")

    state = START_STATE
    total_reward = 0
    path = HARDCODED_EPISODES[choice]
    frames = []  # List to store frames for this episode

    print(f"\nRunning Episodic Path {choice}")
    
    # Capture initial state
    frames.append(capture_frame(state, 0, choice, total_reward, "Episodic"))

    for step, action in enumerate(path, start=1):
        draw_grid(state, step, 1, total_reward)

        next_state = move(state, action)
        reward = get_reward(next_state)

        total_reward += reward
        state = next_state

        # Capture frame after each step
        frames.append(capture_frame(state, step, choice, total_reward, "Episodic"))

        print(f"Step {step}: {state}, Reward: {reward}, Total: {total_reward}")

        if state == GOAL_STATE:
            draw_grid(state, step, 1, total_reward)
            print(f"🎯 Goal Reached! Total Reward: {total_reward}")
            break

    # Save all frames as GIF after episode finishes
    save_gif(frames, choice, "Episodic")
    print(f"📊 Final Total Reward: {total_reward}")
    plt.close()




# -------------------------------
# Main Menu
# -------------------------------
def main():
    print("Choose Mode:")
    print("1. Stochastic")
    print("2. Episodic")

    mode = get_int_input("Enter choice (1 or 2): ", min_value=1, max_value=2)

    if mode == 1:
        episodes = get_int_input("Enter number of episodes (1–3): ", min_value=1, max_value=3)
        iterations = get_int_input(
            "Enter number of iterations (steps) per episode: ",
            min_value=1
        )
        stochastic_mode(episodes, iterations)

    elif mode == 2:
        print("\nHard-Coded Episodes:")
        print("1. Right → Right → Right → Down → Down → Down")
        print("2. Down → Down → Down → Right → Right → Right")
        print("3. Zig-Zag Path")

        choice = get_int_input("Choose episode (1–3): ", min_value=1, max_value=3)
        episodic_mode(choice)

    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
