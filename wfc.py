"""This module contains the Wavefunction Collapse (WFC) algorithm class."""

from wfc_types import Wavefunction


class WFC:
    """A class containg all operations for the WFC algorithm.

    Args:
        wavefunction (Wavefunction): The wavefunction to run the WFC algorithm on

    Attributes:
        wavefunction (Wavefunction): The active wavefunction.
    """

    def __init__(self, wavefunction: Wavefunction):
        """Initialize the WFC class with its wavefunction."""
        self.wavefunction = wavefunction

    def iterate(self) -> None:
        """Perform the next interation in the Wavefunction Collapse Algorithm."""
        pass
