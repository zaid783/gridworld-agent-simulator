# GridWorld Agent Simulation (Stochastic + Episodic)

A simple **4×4 GridWorld** simulation with step-by-step visualization. The agent starts at the top-left cell and tries to reach the goal at the bottom-right cell.

This project includes:
- **Stochastic mode**: the agent selects random actions each step.
- **Episodic mode**: the agent follows one of several hard-coded action sequences.
- **GIF export**: each run is saved as an animated GIF in `gui_results/`.

## Environment
- Grid size: **4×4**
- Start state: **(0, 0)**
- Goal state: **(3, 3)**
- Actions: **up, down, left, right**
- Rewards:
  - Goal cell: **+1**
  - Any other cell: **-1** (including the start)

## Modes

### 1) Stochastic Mode
The agent chooses a random action at each step.
- You select **number of episodes (1–3)**
- You select **number of iterations (steps) per episode**
- An episode ends early if the agent reaches the goal

### 2) Episodic Mode (Deterministic)
The agent follows a predefined action sequence.
- Choose one of **3** hard-coded episodes/paths

## Output
- A live matplotlib grid visualization updates every step.
- GIFs are saved automatically to `gui_results/` with timestamps.

## How to Run

### Option A: Install dependencies with pip
```bash
pip install -r requirements.txt
```

### Run the program
```bash
python ccp_Assignment.py
```

## Project Structure
- `ccp_Assignment.py` — main script
- `gui_results/` — generated GIF outputs

## Notes
- If the goal is reached before the iteration limit, the episode stops early.
- GIF filenames include the mode name, episode number, and a timestamp.
