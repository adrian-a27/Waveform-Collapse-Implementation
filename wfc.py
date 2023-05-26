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
        self.wavefunction: Wavefunction = wavefunction

    def iterate(self) -> bool:
        """Perform the next interation in the Wavefunction Collapse Algorithm."""
        selected_tile = self.wavefunction.get_min_entropy_tile()
        selected_tile.collapase()
        return self.wavefunction.propegate(selected_tile)

    def collapse_wavefunction(self) -> bool:
        """
        Collapses the wavefunction.

        Returns:
            True if the wavefunction successfully collapses. False otherwise.
        """
        was_successful: bool = True

        while not self.wavefunction.is_collapsed():
            was_successful = self.iterate()

            if not was_successful:
                break

        return was_successful