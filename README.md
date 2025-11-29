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

Test reference implementations:
```bash
python main.py
```

Gather results from LLMs:
```bash
python gather_results.py openai,anthropic
```

Analyze collected results:
```bash
python analyze_results.py experiment_results_<timestamp>.json
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

## Next Steps

Based on the project proposal:

1. **Week 1-2 (Completed)**: Game implementations and testing framework
2. **Week 3**: Run experiments with LLMs (OpenAI, Anthropic, local models)
   - Use `gather_results.py` to collect data
   - Run 20 repetitions per game per model at temperature 0.75
3. **Week 4**: Expand to more complex games if needed
4. **Week 5**: Error classification and analysis
   - Use `analyze_results.py` to generate statistics
   - Classify error types (syntax, runtime, semantic)
5. **Week 6-7**: Visualization and report generation

## Project Status

✅ Reference game implementations (5 games)
✅ Automated testing framework (syntax, runtime, semantic)
✅ LLM integration scripts
✅ Results analysis tools
✅ Test suite (37 tests passing)

🔄 Ready for data collection from LLMs

