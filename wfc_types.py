"""This module contains the immutable WFCTile class and Wavefunction Interface."""

from typing import TypeVar, Generic, Set, List, Any
from abc import ABC, abstractmethod

T = TypeVar("T")


class WFCTile(ABC, Generic[T]):
    """
    An immutable tile in the WFC algorithm.

    Args:
        value (T): The given value for this tile. Default is None.

    Attributes:
        value (T): The value represented by this tile
        neighbors (Set[T]): A set of all possible neighbors, initialized to contain every
        option.
    """

    @property
    @abstractmethod
    def value(self) -> T:
        """The value represented by this tile."""

    @property
    @abstractmethod
    def neighbors(self) -> Set[T]:
        """A set of all possible neighbors, initialized to contain every option."""

    @abstractmethod
    def collapase(self) -> ("WFCTile[T]" | None):
        """
        Collapses the tile to an option.

        Returns:
            A new WFCTile if there are still valid options. None otherwise.
        """


class Wavefunction(ABC):
    """
    An interface defining an immutable wavefunction structure in the WFC algorthim.

    Args:
        options (Set[T]): A set of all possible options for each tile of the wavefunction
        size (int, int): a tuple containing width and height information

    Attributes:
        wavefunction (List[List[WFCTile]]): The state of the wavefunction
    """

    @property
    @abstractmethod
    def wavefunction(self) -> List[List[WFCTile[Any]]]:
        """The current state of the wavefunction."""

    @abstractmethod
    def propegate(self, selected_tile: WFCTile[Any]) -> ("Wavefunction" | None):
        """
        Propegates a given change throughout the entire board.

        Arg:
            selected_tile (WFCTile): The selected tile to collapse the waveform under.

        Returns:
            The updated wavefunction if all tiles still have valid options. None otherwise.
        """

    @abstractmethod
    def get_min_entropy_tile(self) -> WFCTile[Any]:
        """
        Determine the next tile to collapse.

        Returns:
            The tile in the wavefunction with the lowest number of options.
        """

    @abstractmethod
    def visualize(self) -> str:
        """
        Visualizes the final result of the wavefunction.

        Raises:
            Exception: Waveform is not fully collapsed

        Returns:
            A string representation of the final waveform
        """

    @abstractmethod
    def is_collapsed(self) -> bool:
        """
        Check if the wavefunction is collapsed.
        
        Returns:
            True if the wavefunction is completely collapsed. False otherwise.
        """
