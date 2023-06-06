"""This module contains the Wavefunction Collapse (WFC) algorithm class."""

from typing import List, Any
from .wavefunction import Wavefunction
from .wfc_tile import WFCTile


class WFC:
    """A class containg all operations for the WFC algorithm.

    Args:
        wavefunction (Wavefunction[WFCTile[Any]]): The wavefunction to run the WFC algorithm on

    Attributes:
        wavefunction (Wavefunction[WFCTile[Any]]): The active wavefunction.
    """

    def __init__(self, wavefunction: Wavefunction[WFCTile[Any]]) -> None:
        """Initialize the WFC class with its wavefunction."""
        self.wavefunction: Wavefunction[WFCTile[Any]] = wavefunction
        self.previous_wavefunctions: List[Wavefunction[WFCTile[Any]]] = []

    def __iterate(self) -> Wavefunction[WFCTile[Any]] | None:
        """Perform the next interation in the Wavefunction[WFCTile[Any]] Collapse algorithm."""
        selected_tile = self.wavefunction.get_min_entropy_tile()
        if not selected_tile:
            return None
        new_tile = selected_tile.collapase()
        return self.wavefunction.propegate(new_tile) if new_tile else None

    def collapse_wavefunction(self) -> Wavefunction[WFCTile[Any]] | None:
        """
        Collapses the wavefunction.

        Returns:
            True if the wavefunction successfully collapses. False otherwise.
        """
        was_successful: (Wavefunction[WFCTile[Any]] | None) = None
        count = 0
        while not self.wavefunction.is_collapsed():
            count += 1
            print(f"Count: {count}", end="\r")
            original_wavefunction = self.wavefunction
            new_wavefunction = self.__iterate()
            if new_wavefunction:
                self.previous_wavefunctions.append(original_wavefunction)
                self.wavefunction = new_wavefunction
            else:
                self.wavefunction = self.previous_wavefunctions.pop()
        print("\n")
        return was_successful
