"""Tests for cleaning and processing career data. No test uses the internet."""
import urllib.error

import pandas as pd
import pytest

from tennisplot import data
from mock_data import (FEMALE_CAREER_JS, FEMALE_PLAYER_PAGE,
                       MALE_CAREER_JS, MALE_PLAYER_PAGE)


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams",
                                  "SerenaWilliams", "  serena   williams "])
def test_name_to_slug_accepts_different_formats(name):
    assert data._name_to_slug(name) == "SerenaWilliams"


@pytest.mark.parametrize("name", ["", "   ", None, 42])
def test_name_to_slug_rejects_invalid_input(name):
    with pytest.raises(ValueError):
        data._name_to_slug(name)


def test_parse_career_js_reads_all_rows():
    assert len(data._parse_career_js(FEMALE_CAREER_JS)) == 3
    assert len(data._parse_career_js(MALE_CAREER_JS)) == 3


def test_parse_career_js_without_matches_raises():
    with pytest.raises(ValueError, match="No match data"):
        data._parse_career_js("var something = 1;")


def test_parse_player_page():
    assert data._parse_player_dob(FEMALE_PLAYER_PAGE) == pd.Timestamp("1981-09-26")
    assert data._parse_full_name(MALE_PLAYER_PAGE, default="x") == "Rafael Nadal"
    assert data._parse_full_name("no name here", default="x") == "x"


def test_female_opponent_age_comes_from_birth_date():
    rows = data._parse_career_js(FEMALE_CAREER_JS)
    df = data._clean_matches(rows, pd.Timestamp("1981-09-26"), "Serena Williams")
    first = df.iloc[0]
    expected = (pd.Timestamp("1995-10-30") - pd.Timestamp("1977-01-19")).days / 365.25
    assert first["opponent"] == "Anne Miller"
    assert first["opponent_age"] == pytest.approx(expected, abs=0.001)


def test_male_opponent_age_is_read_directly():
    rows = data._parse_career_js(MALE_CAREER_JS)
    df = data._clean_matches(rows, pd.Timestamp("1986-06-03"), "Rafael Nadal")
    platel = df[df["opponent"] == "Guillermo Platel"].iloc[0]
    assert platel["opponent_age"] == pytest.approx(22.264, abs=0.001)


def test_age_diff_is_player_minus_opponent():
    rows = data._parse_career_js(MALE_CAREER_JS)
    df = data._clean_matches(rows, pd.Timestamp("1986-06-03"), "Rafael Nadal")
    diff = df["player_age"] - df["opponent_age"]
    assert (df["age_diff"] - diff).abs().max() < 0.002


def test_clean_matches_has_expected_columns_and_order():
    rows = data._parse_career_js(MALE_CAREER_JS)
    df = data._clean_matches(rows, pd.Timestamp("1986-06-03"), "Rafael Nadal")
    assert list(df.columns) == ["player", "date", "tournament", "surface", "result",
                                "score", "opponent", "player_age", "opponent_age",
                                "age_diff"]
    assert df["date"].is_monotonic_increasing
    assert set(df["result"]) == {"W", "L"}


def test_clean_matches_drops_invalid_rows():
    rows = data._parse_career_js(FEMALE_CAREER_JS)
    rows.append(["19980101", "Mock", "Hard", "W", "", "", "", "", "", "", "", "X",
                 "", "", "", "R", "19800101"])           # no result
    rows.append(["19980102", "Mock", "Hard", "W", "W", "", "", "", "", "", "", "Y",
                 "", "", "", "R", ""])                   # no opponent birth date
    df = data._clean_matches(rows, pd.Timestamp("1981-09-26"), "Serena Williams")
    assert len(df) == 3


def test_unknown_player_gives_meaningful_error(monkeypatch):
    def fake_urlopen(*args, **kwargs):
        raise urllib.error.HTTPError("url", 404, "Not Found", None, None)
    monkeypatch.setattr(data.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(ValueError, match="No Tennis Abstract data found for 'Gaston Sanchez'"):
        data.get_career_matches("Gaston Sanchez")


def test_get_career_matches_with_mock_pages(monkeypatch):
    pages = {"jsmatches": MALE_CAREER_JS, "player.cgi": MALE_PLAYER_PAGE}
    def fake_fetch(url, player_name):
        return next(text for key, text in pages.items() if key in url)
    monkeypatch.setattr(data, "_fetch_text", fake_fetch)
    df = data.get_career_matches("rafael nadal")
    assert len(df) == 3
    assert (df["player"] == "Rafael Nadal").all()
