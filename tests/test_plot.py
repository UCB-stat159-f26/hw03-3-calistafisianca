"""Tests for the scatter plot. No test uses the internet."""
import matplotlib

matplotlib.use("Agg")  # draw without opening a window

import pandas as pd
import pytest

from tennisplot import plot_career_matches
from tennisplot import data
from mock_data import MALE_CAREER_JS


@pytest.fixture
def matches():
    rows = data._parse_career_js(MALE_CAREER_JS)
    return data._clean_matches(rows, pd.Timestamp("1986-06-03"), "Rafael Nadal")


def test_plot_draws_wins_and_losses(matches):
    ax = plot_career_matches(matches)
    assert len(ax.collections) == 2  # one scatter for wins, one for losses
    labels = [text.get_text() for text in ax.get_legend().get_texts()]
    assert labels == ["Win (1)", "Loss (2)"]


def test_plot_labels_use_player_name(matches):
    ax = plot_career_matches(matches)
    assert ax.get_xlabel() == "Rafael Nadal's age (years)"


def test_plot_rejects_wrong_data_frame():
    with pytest.raises(ValueError, match="Missing columns"):
        plot_career_matches(pd.DataFrame({"a": [1, 2]}))
