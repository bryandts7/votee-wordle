# Wordle Auto Solver CLI

A command-line application to solve Wordle puzzles. This tool can solve the daily Wordle, a random Wordle, or a specific Wordle word using a predefined algorithm.

---

## Features

- **Daily Mode**: Solve the daily Wordle puzzle.
- **Random Mode**: Solve a randomly generated Wordle puzzle.
- **Word Mode**: Solve a specific Wordle word provided by the user.
- **Customizable Word Size**: Supports Wordle puzzles of any size (e.g., 5-letter, 6-letter, etc.).

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bryandts7/votee-wordle.git
   cd votee-wordle
   ```

2. **Install dependencies**:
   Ensure you have Python 3.x installed. Then, install the required dependencies:
   ```bash
   pip install requests
   ```

3. **Run the application**:
   Use the CLI to solve Wordle puzzles.

---

## Usage

### Solve Daily Wordle
To solve the daily Wordle puzzle:

```bash
python wordle_auto.py daily
```

```bash
python wordle_auto.py --size 8 daily
```

### Solve Random Wordle
To solve a random Wordle puzzle:
```bash
python wordle_auto.py --size 5 random
```

### Solve a Specific Word
To solve a specific Wordle word (e.g., "apple"):
```bash
python wordle_auto.py --size 5 word apple
```

### Arguments
- `--size`: The size of the Wordle puzzle (e.g., `5` for a 5-letter Wordle). The default value is 5
- `daily`: Solve the daily Wordle.
- `random`: Solve a random Wordle.
- `word`: Solve a specific Wordle word (requires an additional argument for the word). If the number of alphabets in the specified word is not 5, you must specify the size accordingly.

---

## How It Works

The solver uses a combination of feedback from the Wordle API and a heuristic algorithm to generate guesses. It keeps track of:
- **Correct letters**: Letters that are in the correct position.
- **Present letters**: Letters that are in the word but in the wrong position.
- **Absent letters**: Letters that are not in the word.

Based on this information, the solver generates the next guess until the word is solved or the maximum number of attempts is reached.

---

## Example Output

### Daily Mode
```bash
Attempt 1: crane
Attempt 2: slope
Attempt 3: glory
Attempt 4: flour

Solved in 4 attempts!
Final Answer: flour
```

### Random Mode
```bash
Attempt 1: tiger
Attempt 2: sloan
Attempt 3: brand

Solved in 3 attempts!
Final Answer: brand
```

### Word Mode
```bash
Attempt 1: apple
Attempt 2: paper
Attempt 3: grape

Solved in 3 attempts!
Final Answer: grape
```

---

## Limitations
- The solver relies on the Wordle API (`https://wordle.votee.dev:8000/`) for feedback. If the API is unavailable, the solver will not work.
- The solver may not always find the correct word within the maximum number of attempts (100 by default).

---

## Acknowledgments

- Thanks to the [Wordle API](https://wordle.votee.dev:8000/) for providing the backend.

---

Enjoy solving Wordle puzzles with this CLI tool! 🎉
```
