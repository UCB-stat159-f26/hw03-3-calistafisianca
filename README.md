# tennisplot

A Python package that retrieves the career matches of a tennis player from
[Tennis Abstract](https://www.tennisabstract.com) and draws a scatter plot like
the New York Times' Serena Williams visualization: the player's age on the
x-axis, the age difference with each opponent on the y-axis, and points
colored by win or loss.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-calistafisianca.git
```

## Usage

```python
import matplotlib.pyplot as plt
from tennisplot import get_career_matches, plot_career_matches

# Serena Williams data and plot
serena = get_career_matches("serena williams")
plot_career_matches(serena)
plt.show()

# Rafael Nadal data and plot
rafa = get_career_matches("Rafael Nadal")
plot_career_matches(rafa)
plt.show()

# An unknown player raises a meaningful error
get_career_matches("GastonSanchez")
# ValueError: No Tennis Abstract data found for 'GastonSanchez'. Check the
# spelling of the player's first and last name.
```

Player names can be written as `"serena williams"`, `"Serena Williams"`, or
`"SerenaWilliams"`.

## Functions

### `get_career_matches(player_name)`

Downloads the player's career file and player page from Tennis Abstract and
returns a data frame with one row per match:

| Column | Description |
|---|---|
| `player` | Player's full name |
| `date` | Date of the match |
| `tournament`, `surface` | Tournament name and court surface |
| `result` | `"W"` (win) or `"L"` (loss) for the player |
| `score` | Match score |
| `opponent` | Opponent's name |
| `player_age` | Player's age (years) on the match date |
| `opponent_age` | Opponent's age (years) on the match date |
| `age_diff` | `player_age - opponent_age` |

Career files of female players give each opponent's date of birth, from which
the age is computed; files of male players already give the opponent's age.
The player's own date of birth comes from their Tennis Abstract player page.
Matches without a win/loss result or without the opponent's age are dropped.

### `plot_career_matches(matches, ax=None)`

Takes the data frame from `get_career_matches()` and returns a matplotlib
`Axes` with the scatter plot. Pass `ax` to draw on existing axes.

## Package structure

```
├── pyproject.toml          # package metadata and dependencies
├── README.md
├── src/tennisplot/
│   ├── __init__.py         # exposes the two public functions
│   ├── data.py             # get_career_matches() and helpers
│   └── plot.py             # plot_career_matches() and helpers
└── tests/
    ├── conftest.py
    ├── mock_data.py        # mock career files and player pages
    ├── test_data.py
    └── test_plot.py
```

## Tests

The tests use mock Tennis Abstract content (`tests/mock_data.py`) and never
contact the live website.

```bash
pip install ".[test]"
pytest
```

## Personal reflections

### Calista Kurniawan

[Your reflection here]
