"""This module implements a space in a sodoku board used in the WFC algorithm."""

from __future__ import annotations
import random
from ..wfc_tile import WFCTile


class SudokuSpace(WFCTile[int]):
    """
    An immutable type that represents a space on a sudoku space.

    Args:
        x (int): the x-coordinate of the space
        y (int): the y-coordinate of the space
        max_value (int): the maximum value of this space
        value (int | None): a starting value between 1 and 9 inclusive. Defaults to None.

    Attributes:
        x (int): the x-coordinate of the space
        y (int): the y-coordinate of the space
        max_value (int): the maximum value of this space
        value (T | None): The value represented by this tile.
        possible_values (Set[T]): All possible values for this tile.
        neighbors (Set[T]): A set of all possible neighbors, initialized to contain every
        option.
    """

    def __init__(
        self,
        x: int,
        y: int,
        max_value: int,
        value: int | None = None,
    ) -> None:
        """
        Initilizes new sudoku space.

        Args:
            x (int): the x-coordinate of the space
            y (int): the y-coordinate of the space
            max_value (int): the maximum value of this space
            value (int | None): a starting value between 1 and 9 inclusive. Defaults to None.

        Raises:
            ValueError: value is not between 1 and the max_value.
        """
        if value and (value < 1 or value > max_value):
            raise ValueError(
                f"Value is {value}, but must be between 1 and {max_value} inclusive."
            )

        super().__init__(x, y, value)
        self.max_value = max_value
        self.neighbors = set(range(1, max_value + 1))
        self.possible_values = set(range(1, max_value + 1)) if not value else {value}
        if value:
            self.neighbors.remove(value)

    def validate_value(self, new_value: int) -> None:
        """
        Check that a new_value is valid.

        Raises:
            ValueError: New value is outside of the allowed range.
        """
        if new_value and (new_value < 1 or new_value > self.max_value):
            raise ValueError(
                f"Value is {new_value}, but must be between 1 and {self.max_value} inclusive."
            )

    def collapase(self) -> SudokuSpace | None:
        """
        Collapses the space to a single randomly-selected valid value.

        Returns:
            A new WFCTile if there are still valid options. None otherwise.
        """
        if self.possible_values is set():
            return None

        updated_space = SudokuSpace(self.x, self.y, self.max_value)
        updated_space.value = random.choice(tuple(self.possible_values))
        updated_space.possible_values = (
            set(value for value in self.possible_values if value != updated_space.value)
            if len(self.possible_values) > 1
            else {updated_space.value}
        )
        updated_space.neighbors = set(
            value for value in self.neighbors if value != updated_space.value
        )
        return updated_space

    def copy(self) -> SudokuSpace:
        """
        Create a copy of the space.

        Returns:
            A copy of the space.
        """
        new_copy = SudokuSpace(self.x, self.y, self.max_value, self.value)
        new_copy.possible_values = self.possible_values.copy()
        new_copy.neighbors = self.neighbors.copy()

        return new_copy
