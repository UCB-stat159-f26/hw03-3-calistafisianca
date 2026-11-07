"""Download and clean a player's career matches from Tennis Abstract."""
import json
import re
import urllib.error
import urllib.request

import pandas as pd

BASE_URL = "https://www.tennisabstract.com"
DAYS_PER_YEAR = 365.25

# Positions used in each match array of a Tennis Abstract career file.
# Position 16 is the opponent's date of birth (YYYYMMDD) for female players
# and the opponent's age (in years) for male players.
COLUMNS = {
    0: "date",
    1: "tournament",
    2: "surface",
    4: "result",
    9: "score",
    11: "opponent",
    16: "opponent_info",
}


def get_career_matches(player_name):
    """Return a clean data frame with the career matches of a tennis player.

    Parameters
    ----------
    player_name : str
        Name of the player, e.g. "serena williams", "Serena Williams",
        or "SerenaWilliams".

    Returns
    -------
    pandas.DataFrame
        One row per match with the columns player, date, tournament,
        surface, result ("W" or "L"), score, opponent, player_age,
        opponent_age and age_diff (player_age - opponent_age).

    Raises
    ------
    ValueError
        If no Tennis Abstract data exists for `player_name`.
    """
    slug = _name_to_slug(player_name)
    career_js = _fetch_text(f"{BASE_URL}/jsmatches/{slug}Career.js", player_name)
    player_page = _fetch_text(f"{BASE_URL}/cgi-bin/player.cgi?p={slug}", player_name)
    rows = _parse_career_js(career_js)
    player_dob = _parse_player_dob(player_page)
    full_name = _parse_full_name(player_page, default=player_name)
    return _clean_matches(rows, player_dob, full_name)


def _name_to_slug(player_name):
    """Turn "serena williams" or "SerenaWilliams" into "SerenaWilliams"."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("player_name must be a non-empty string, e.g. 'Serena Williams'.")
    words = player_name.split()
    return "".join(word[0].upper() + word[1:] for word in words)


def _fetch_text(url, player_name):
    """Download a page as text; a missing page means an unknown player."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError:
        raise ValueError(
            f"No Tennis Abstract data found for '{player_name}'. "
            "Check the spelling of the player's first and last name."
        ) from None


def _parse_career_js(career_js):
    """Extract the list of match arrays from the text of a career JS file."""
    pattern = r"var\s+\w+\s*=\s*(\[\s*\[.*?\]\s*\])\s*;?"
    blocks = re.findall(pattern, career_js, flags=re.S)
    if not blocks:
        raise ValueError("No match data found in the career file.")
    rows = []
    for block in blocks:
        block = re.sub(r",\s*\]", "]", block.replace("\\'", "'"))
        rows.extend(json.loads(block))
    return rows


def _parse_player_dob(player_page):
    """Read the player's date of birth (var dob = YYYYMMDD) from their page."""
    found = re.search(r"var\s+dob\s*=\s*'?(\d{8})'?", player_page)
    if not found:
        raise ValueError("Could not find the player's date of birth.")
    return pd.to_datetime(found.group(1), format="%Y%m%d")


def _parse_full_name(player_page, default):
    """Read the player's full name (var fullname = '...') from their page."""
    found = re.search(r"var\s+fullname\s*=\s*'([^']+)'", player_page)
    return found.group(1) if found else default


def _rows_to_frame(rows):
    """Keep the useful positions of each match array as named columns."""
    records = [{name: row[i] if i < len(row) else "" for i, name in COLUMNS.items()}
               for row in rows]
    frame = pd.DataFrame(records, columns=list(COLUMNS.values()))
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d", errors="coerce")
    return frame.drop_duplicates()


def _opponent_ages(opponent_info, match_dates):
    """Opponent age in years from a birth date (female) or an age (male)."""
    info = opponent_info.astype(str).str.strip()
    is_dob = info.str.fullmatch(r"\d{8}")
    dob = pd.to_datetime(info.where(is_dob), format="%Y%m%d", errors="coerce")
    age_from_dob = (match_dates - dob).dt.days / DAYS_PER_YEAR
    return age_from_dob.where(is_dob, pd.to_numeric(info, errors="coerce"))


def _add_ages(frame, player_dob):
    """Add player_age, opponent_age and age_diff columns."""
    frame = frame.copy()
    frame["player_age"] = (frame["date"] - player_dob).dt.days / DAYS_PER_YEAR
    frame["opponent_age"] = _opponent_ages(frame["opponent_info"], frame["date"])
    frame["age_diff"] = frame["player_age"] - frame["opponent_age"]
    return frame.drop(columns="opponent_info")


def _clean_matches(rows, player_dob, player_name):
    """Build the final data frame: ages added, invalid matches dropped."""
    frame = _add_ages(_rows_to_frame(rows), player_dob)
    frame = frame[frame["result"].isin(["W", "L"])]
    frame = frame.dropna(subset=["date", "player_age", "opponent_age"]).copy()
    age_columns = ["player_age", "opponent_age", "age_diff"]
    frame[age_columns] = frame[age_columns].round(3)
    frame.insert(0, "player", player_name)
    return frame.sort_values("date").reset_index(drop=True)
