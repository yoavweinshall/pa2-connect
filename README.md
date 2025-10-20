# HW2 ConnectX — Starter Guide

This directory contains the starter code for the ConnectX (Connect Four) agent you will build in HW2. You will implement a minimax-based AI with optional alpha-beta pruning and custom evaluation so it can compete against a human or random opponent.

## Repository Layout
- `main.py` – Entry point that launches the Tkinter UI (`connectx.app.main`).
- `connectx/game.py` – ConnectX environment; provides the `ConnectX` class, legal move generation, and win detection.
- `connectx/ai.py` – Where you will implement `best_move`. The file currently raises `NotImplementedError`.
- `connectx/app.py` – Simple GUI and game loop; it calls your `best_move` implementation when the AI takes a turn.
- `common/profiling.py` – Placeholder for optional profiling helpers if you want to measure performance.
- `requirements.txt` – Python dependencies needed for the starter (Tkinter bindings and pytest).

## Getting Started
1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
2. Install dependencies from the starter directory:
   ```bash
   pip install -r requirements.txt
   ```
   Tkinter is included with most Python installations; the `tk` package entry ensures the autograder environment has it as well.

## Running the Game Locally
From `hw2_autograder/starter`, launch the GUI:
```bash
python main.py
```
- You play as Red (`R`) and the AI plays as Yellow (`Y`).
- Use the radio buttons to switch between a random opponent and your AI.
- If `best_move` is still unimplemented, the app falls back to a random move and displays a reminder dialog.

## Implementing `best_move`
Your task is to complete `connectx/ai.py::best_move` so it returns the column index (0–6) where the AI should drop its next piece.

Expected behavior:
- Support pure minimax search up to the provided `depth`. The root player is Red (`R`); minimize when it is Yellow’s turn.
- Respect the `use_alpha_beta` flag: when `True`, prune using alpha-beta; when `False`, run plain minimax.
- Use the supplied `evaluator` callable when the search depth reaches zero. If `evaluator` is `None`, you may define a reasonable default heuristic.
- Treat terminal positions correctly: immediate wins should return large positive/negative scores so the agent prefers winning and avoids losing.
- Do **not** mutate the original `game` instance. Clone it (`game.clone()`) before exploring moves.

Unit tests will call `best_move` with different depths, pruning settings, and evaluators, so make sure your implementation handles each combination.
