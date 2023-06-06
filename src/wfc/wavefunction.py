"""This module contains the immutable Wavefunction Interface."""

from typing import Self, TypeVar, Generic, Set, List
from abc import ABC, abstractmethod

E = TypeVar("E")


class Wavefunction(ABC, Generic[E]):
    """
    An interface defining an immutable wavefunction structure in the WFC algorthim.

    Attributes:
        wavefunction (List[List[WFCTile]]): The state of the wavefunction
    """

    @property
    @abstractmethod
    def wavefunction(self) -> List[List[E]]:
        """The current state of the wavefunction."""

    @abstractmethod
    def propegate(self, selected_tile: E) -> Self | None:
        """
        Propegates a given change throughout the entire board.

        Arg:
            selected_tile (WFCTile): The selected tile to collapse the wavefunction under.

        Returns:
            The updated wavefunction if all tiles still have valid options. None otherwise.
        """

    @abstractmethod
    def get_min_entropy_tile(self) -> E | None:
        """
        Determine the tile with the fewest options (> 1). Selects randomly if there are multiple.

        Returns:
            The tile in the wavefunction with the lowest number of options. None if there are none.
        """

    @abstractmethod
    def get_affected_spaces(self, board_copy: List[List[E]], x: int, y: int) -> Set[E]:
        """
        Determine all spaces that can be affected by a tile at this coordinate.

        Args:
            x (int): The x-coordinate of a tile.
            y (int): The y-coordinate of a tile.

        Returns:
            A set of tiles that can be affected by the given coordinates.
        """

    @abstractmethod
    def __str__(self) -> str:
        """
        Visualizes the current state of the wavefunction.

        Returns:
            A string representation of the wavefunction
        """

    @abstractmethod
    def is_collapsed(self) -> bool:
        """
        Check if the wavefunction is collapsed.

        Returns:
            True if the wavefunction is completely collapsed. False otherwise.
        """
