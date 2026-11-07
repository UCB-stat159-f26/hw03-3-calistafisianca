"""Get a tennis player's career matches from Tennis Abstract and plot them."""
from .data import get_career_matches
from .plot import plot_career_matches

__all__ = ["get_career_matches", "plot_career_matches"]
__version__ = "0.1.0"
