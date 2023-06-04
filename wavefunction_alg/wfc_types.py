"""This module contains the immutable WFCTile class and Wavefunction Interface."""

from typing import Self, TypeVar, Generic, Set, List
from abc import ABC, abstractmethod

T = TypeVar("T")
E = TypeVar("E")


class WFCTile(ABC, Generic[T]):
    """
    An immutable tile in the WFC algorithm.

    Args:
        value (T | None): The given value for this tile. Default is None.

    Attributes:
        value (T | None): The value represented by this tile.
        possible_values (Set[T]): All possible values for this tile.
        neighbors (Set[T]): A set of all possible neighbors, initialized to contain every
        option.
    """

    def __init__(self, value: (T | None) = None) -> None:
        """
        Initialize a WFCTile.

        Args:
            value (T | None): The given value for this tile. Default is None.
        """
        self.value: (T | None) = value
        self.possible_values: Set[T] = set()
        self.neighbors: Set[T] = set()

    @abstractmethod
    def collapase(self) -> Self | None:
        """
        Collapses the space to a single randomly-selected valid value.

        Returns:
            A new WFCTile if there are still valid options. None otherwise.
        """


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
