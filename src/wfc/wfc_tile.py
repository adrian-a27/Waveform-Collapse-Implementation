"""This module contains the immutable WFCTile interface."""

from __future__ import annotations
from typing import TypeVar, Generic, Set
from abc import ABC, abstractmethod

T = TypeVar("T")


class WFCTile(ABC, Generic[T]):
    """
    An immutable tile in the WFC algorithm.

    Args:
        value (T | None): The given value for this tile. Default is None.

    Attributes:
        value (T | None): The value represented by this tile.
        x (int): x-coordinate of the tile.
        y (int): y-coordinate of the tile.
        possible_values (Set[T]): All possible values for this tile.
        neighbors (Set[T]): A set of all possible neighbors, initialized to contain every
        option.
    """

    def __init__(self, x: int, y: int, value: (T | None) = None) -> None:
        """
        Initialize a WFCTile.

        Args:
            value (T | None): The given value for this tile. Default is None.
        """
        self.value: (T | None) = value
        self.x = x
        self.y = y
        self.possible_values: Set[T] = set()
        self.neighbors: Set[T] = set()

    @abstractmethod
    def collapase(self) -> WFCTile[T] | None:
        """
        Collapses the space to a single randomly-selected valid value.

        Returns:
            A new WFCTile if there are still valid options. None otherwise.
        """
