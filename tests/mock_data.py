"""Mock Tennis Abstract content, so tests never hit the live website."""

# A few entries from a female player's career file (opponent date of birth at position 16)
FEMALE_CAREER_JS = """var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],
          ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"],
          ["19970804", "Manhattan Beach", "Hard", "W", "L", "", "", "WC", "Q3", "7-6 4-6 6-3", "3", "Magui Serna", "54", "6", "", "L", "19790301", "167", "ESP", "0", "", "", "", "", "", "", "1997-W-WT-USA-07A-1997-026"]];
"""

# A few entries from a male player's career file (opponent age at position 16).
# The third row is a made-up win, added to test win/loss handling.
MALE_CAREER_JS = """var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0"],
          ["20010917", "Seville CH", "Clay", "C", "L", "", "", "WC", "R16", "3-6 6-1 6-3", "3", "Stefano Galvani", "161", "2", "", "R", "24.2902121834", "178", "ITA", "0"],
          ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Mock Opponent", "300", "", "", "R", "20.5", "", "ESP", "0"]];
"""

FEMALE_PLAYER_PAGE = "var nameparam = 'SerenaWilliams';\nvar fullname = 'Serena Williams';\nvar dob = 19810926;\nvar hand = 'R';"
MALE_PLAYER_PAGE = "var nameparam = 'RafaelNadal';\nvar fullname = 'Rafael Nadal';\nvar dob = 19860603;\nvar hand = 'L';"
