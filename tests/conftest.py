"""Let tests import mock_data.py from this folder."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
