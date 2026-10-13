import importlib.resources
import random
from typing import List, Optional

_CACHED_QUOTES: Optional[List[str]] = None


def load_quotes() -> List[str]:
    """Read all .txt files from the package quotes directory and return non-empty lines."""
    global _CACHED_QUOTES
    if _CACHED_QUOTES is not None:
        return _CACHED_QUOTES

    all_quotes: List[str] = []

    # Access the bundled quotes/ folder inside the iitkquotes package
    quotes_dir = importlib.resources.files("iitkquotes") / "quotes"

    if quotes_dir.is_dir():
        # Sort files so index order remains consistent across runs
        for text_file in sorted(quotes_dir.glob("*.txt")):
            with text_file.open("r", encoding="utf-8") as f:
                for raw_line in f:
                    cleaned_line = raw_line.strip()
                    # Skip empty lines and lines with only spaces/newlines
                    if cleaned_line:
                        all_quotes.append(cleaned_line)

    _CACHED_QUOTES = all_quotes
    return _CACHED_QUOTES


def quote(index: Optional[int] = None) -> str:
    """Return a campus quote.

    If index is provided (1-based), return that specific quote.
    If no index is provided, return a random quote.
    """
    quotes = load_quotes()

    if not quotes:
        return "Arey bhai, quotes folder mein koi valid text file ya quote nahi mila!"

    if index is None:
        return random.choice(quotes)

    if not isinstance(index, int):
        raise TypeError(f"Bhai index integer hona chahiye, '{type(index).__name__}' nahi!")

    zero_based_index = index - 1
    if 0 <= zero_based_index < len(quotes):
        return quotes[zero_based_index]

    raise IndexError(
        f"Arey baap re! Index {index} out of syllabus hai bhai! "
        f"CPI ki tarah quote range bhi limited hai — 1 se {len(quotes)} ke beech choose karo."
    )


# Module-level variable so 'from iitkquotes import QUOTES' works directly
QUOTES = load_quotes()