"""Input loading classes with validation and a shared interface."""
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class DataLoader(ABC):
    """Abstract loader interface.

    Subclasses implement load(path) and return a pandas DataFrame.
    """

    def __init__(self):
        self._last_loaded_path = None

    @property
    def last_loaded_path(self):
        """Return the path used by the most recent successful load."""
        return self._last_loaded_path

    @abstractmethod
    def load(self, path):
        """Load a dataset from path."""
        raise NotImplementedError


class CSVBookingLoader(DataLoader):
    """Load hotel-booking records from a CSV file."""

    def load(self, path):
        """Validate and load a CSV file without modifying the source."""
        source = Path(path)

        if source.suffix.lower() != ".csv":
            raise ValueError("Expected a .csv input file.")

        if not source.is_file():
            raise ValueError(f"Input file does not exist: {source}")

        handle = None

        try:
            handle = source.open("r", encoding="utf-8")
            frame = pd.read_csv(handle)

        except (pd.errors.ParserError, UnicodeDecodeError, OSError) as exc:
            raise ValueError(f"Could not read CSV input: {exc}") from exc

        else:
            self._last_loaded_path = str(source.resolve())
            return frame

        finally:
            if handle is not None:
                handle.close()
