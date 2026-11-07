"""Scatter plot of a player's age vs. the age difference with each opponent."""
import matplotlib.pyplot as plt

COLORS = {"W": "#7FB8E6", "L": "#7B3FA0"}  # light blue = win, purple = loss
LABELS = {"W": "Win", "L": "Loss"}
REQUIRED_COLUMNS = ["player_age", "age_diff", "result"]


def plot_career_matches(matches, ax=None):
    """Plot a player's age against the age difference with each opponent.

    Parameters
    ----------
    matches : pandas.DataFrame
        Data frame returned by `get_career_matches()`.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. A new figure is created when omitted.

    Returns
    -------
    matplotlib.axes.Axes
        The axes with the scatter plot: x = player's age, y = player's age
        minus opponent's age, points colored by win or loss.
    """
    _check_columns(matches)
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    for result in ["W", "L"]:
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_diff"], s=14, alpha=0.75,
                   color=COLORS[result], edgecolors="none",
                   label=f"{LABELS[result]} ({len(subset)})")
    _style_axes(ax, _player_name(matches))
    return ax


def _check_columns(matches):
    """Raise a clear error if the data frame lacks the columns to plot."""
    missing = [col for col in REQUIRED_COLUMNS if col not in matches.columns]
    if missing:
        raise ValueError(
            f"Missing columns {missing}; use the output of get_career_matches()."
        )


def _player_name(matches):
    """Name used in the labels; falls back to 'Player'."""
    if "player" in matches.columns and len(matches) > 0:
        return matches["player"].iloc[0]
    return "Player"


def _style_axes(ax, name):
    """Add a zero line, labels, title, grid and legend in a NYT-like style."""
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel(f"{name}'s age (years)")
    ax.set_ylabel(f"Age difference: {name} − opponent (years)")
    ax.set_title(f"{name} vs. opponents' ages", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
