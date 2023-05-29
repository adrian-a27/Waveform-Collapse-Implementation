"""This module contains the Wavefunction Collapse (WFC) algorithm class."""
from typing import List
from wavefunction_alg.wfc_types import Wavefunction


class WFC:
    """A class containg all operations for the WFC algorithm.

    Args:
        wavefunction (Wavefunction): The wavefunction to run the WFC algorithm on

    Attributes:
        wavefunction (Wavefunction): The active wavefunction.
    """

    def __init__(self, wavefunction: Wavefunction) -> None:
        """Initialize the WFC class with its wavefunction."""
        self.wavefunction: Wavefunction = wavefunction
        self.previous_wavefunctions: List[Wavefunction] = []

    def __iterate(self) -> Wavefunction | None:
        """Perform the next interation in the Wavefunction Collapse algorithm."""
        selected_tile = self.wavefunction.get_min_entropy_tile()
        new_tile = selected_tile.collapase()
        return self.wavefunction.propegate(new_tile) if new_tile else None

    def collapse_wavefunction(self) -> Wavefunction | None:
        """
        Collapses the wavefunction.

        Returns:
            True if the wavefunction successfully collapses. False otherwise.
        """
        was_successful: (Wavefunction | None) = None

        while not self.wavefunction.is_collapsed():
            original_wavefunction = self.wavefunction
            new_wavefunction = self.__iterate()

            if new_wavefunction:
                self.previous_wavefunctions.append(original_wavefunction)
                self.wavefunction = new_wavefunction
            else:
                self.wavefunction = self.previous_wavefunctions.pop()

        return was_successful
