# Configuration Guide

## LLM API Setup

To gather results from LLMs, you need to configure API keys:

### OpenAI
```bash
export OPENAI_API_KEY="your-key-here"
```

### Anthropic
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Local Models
For local models, create a `local_llm.py` file with a `generate()` function:
```python
def generate(prompt, model_path, temperature):
    # Your local model integration here
    return generated_code
```

## Running Experiments

1. **Test reference implementations:**
   ```bash
   python main.py
   ```

2. **Gather results from LLMs:**
   ```bash
   python gather_results.py openai
   python gather_results.py anthropic
   python gather_results.py openai,anthropic
   ```

3. **Analyze results:**
   ```bash
   python analyze_results.py experiment_results_<timestamp>.json
   ```

## Experiment Parameters

Edit `gather_results.py` to adjust:
- `REPETITIONS = 20` - Number of times to run each game per model
- `TEMPERATURE = 0.75` - LLM temperature setting
- `RUNTIME_ITERATIONS = 50` - Number of runtime test iterations

## Results Format

Results are saved as:
- `experiment_results_<timestamp>.json` - Full detailed results
- `results_matrix.json` - Summary matrix (3 × N × M)
- `*_stats.json` - Statistical analysis
- `*_matrix.json` - Matrix format

