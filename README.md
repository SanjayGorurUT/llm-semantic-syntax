# LLM Semantic Syntax Evaluation

This project evaluates the correctness of large language models in creating programs that contain both arithmetic and graphical properties. We assess LLM performance by prompting them to reconstruct simple board games in Python using pygame.

## Project Overview

The project tests LLM-generated code across three categories:
1. **Syntax errors** - Detected prior to execution
2. **Runtime errors** - Division by zero, out of bounds, overflow
3. **Game logic errors** - Semantic correctness in following game rules

## Games Included

- Tic-Tac-Toe
- Connect Four
- Snakes and Ladders
- Snake Game
- Ball Bouncing (off walls)

## Project Structure

```
llm-semantic-syntax/
├── games/              # Reference game implementations
├── testing/            # Testing framework
├── prompts/            # LLM prompt templates
├── tests/              # Pytest test suite
├── main.py            # Main experiment runner
└── requirements.txt   # Python dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running Tests

Run all tests:
```bash
pytest tests/
```

Run specific game tests:
```bash
pytest tests/test_tic_tac_toe.py
```

### Running Experiments

```bash
python main.py
```

### Playing Games

Games can be played interactively through pytest:
```bash
pytest tests/ -k play
```

## Testing Framework

The automated testing framework includes:
- Syntax error detection using Python's compiler
- Runtime error detection (50 iterations per program)
- Semantic accuracy testing with predefined test cases

## Results Format

Results are reported in a (3 × N × M) matrix where:
- 3 = error categories (syntax, runtime, semantic)
- N = number of games
- M = number of LLM models

