"""This module implements a sudoku board to be used with the WFC algorithm."""

from __future__ import annotations
import random
from typing import List, Dict, Tuple, Set
from ..wavefunction import Wavefunction
from .sudoku_space import SudokuSpace


class SudokuBoard(Wavefunction[SudokuSpace]):
    """
    An immutable Sudoku board to be used in the WFC algorthim.

    Attributes:
        wavefunction (List[List[SudokuSpace]]): The state of the wavefunction
    """

    def __init__(
        self,
        board_size: int,
        initial_values: Dict[int, List[Tuple[int, int]]] | None = None,
    ):
        """
        Initialize new Sudoku board.

        Args:
            board_size (int): The size of the board. Must be a perfect square.
            initial_values (Dict[int, List[Tuple[int, int]]] | None): A list of values to add to the board. Defaults to None.

        Raises:
            ValueError: board_size is not a perfect sqaure.
            ValueError: Provided board is unsolvable.
        """
        if board_size**0.5 != int(board_size**0.5):
            raise ValueError("board_size needs to be a perfect square")
        self.board_size = board_size
        self._wavefunction: List[List[SudokuSpace]] = [
            [SudokuSpace(x, y, max_value=board_size) for x in range(board_size)]
            for y in range(board_size)
        ]

        count = 0
        if initial_values:
            value: int
            coords: List[Tuple[int, int]]
            for value, coords in initial_values.items():
                for coord in coords:
                    count += 1
                    space = self._wavefunction[coord[1]][coord[0]]
                    if value not in space.possible_values:
                        raise ValueError("Provided board is unsolvable.")
                    space.validate_value(value)
                    space.value = value
                    space.possible_values = {value}
                    space.neighbors.remove(value)
                    propegation_result = self.propegate(space)

                    if propegation_result:
                        self._wavefunction = propegation_result._wavefunction
                    else:
                        raise ValueError("Provided board is unsolvable.")

    @property
    def wavefunction(self) -> List[List[SudokuSpace]]:
        """The current state of the sudoku wavefunction."""
        return self._wavefunction

    def get_min_entropy_tile(self) -> SudokuSpace | None:
        """
        Determine the space with the fewest options (> 1). Selects randomly if there are multiple.

        Returns:
            The space on the sudoku board with the lowest number of options.
        """
        min_value = float("inf")
        min_spaces: List[SudokuSpace] = []

        for row in self.wavefunction:
            for space in row:
                if space.value is not None:
                    continue

                if len(space.possible_values) < min_value:
                    min_spaces = [space]
                    min_value = len(space.possible_values)
                elif len(space.possible_values) == min_value:
                    min_spaces.append(space)

        return random.choice(min_spaces) if min_spaces else None

    def is_collapsed(self) -> bool:
        """
        Check if the sudoku board is fully solved.

        Returns:
            True if the sudoku board is fully solved. False otherwise.
        """
        return all(
            all(space.value is not None for space in row) for row in self.wavefunction
        )

    def get_affected_spaces(
        self, board_copy: List[List[SudokuSpace]], x: int, y: int
    ) -> Set[SudokuSpace]:
        """
        Return the spaces in the same row, column, and square of the given space.

        Args:
            board_copy (List[List[SudokuSpace]]): A copy of the current board.
            x (int): The x-coordinate of a space.
            y (int): The y-coordinate of a space.

        Raises:
            ValueError: Either coordinate is out of range

        Returns:
            A list of spaces that can be affected by the given coordinates.
        """
        if (x < 0 or x >= self.board_size) or (y < 0 or y >= self.board_size):
            raise IndexError("One or more of the given coordinates are out of range")

        affected_spaces = set(
            [board_copy[y][other_coord] for other_coord in range(self.board_size)]
            + [board_copy[other_coord][x] for other_coord in range(self.board_size)]
        )

        square_size: int = int(self.board_size**0.5)
        top_left_x = x - x % square_size
        top_left_y = y - y % square_size

        for y_offset in range(square_size):
            for x_offset in range(square_size):
                affected_spaces.add(
                    board_copy[top_left_y + y_offset][top_left_x + x_offset]
                )

        affected_spaces.remove(board_copy[y][x])
        return affected_spaces

    def propegate(self, selected_tile: SudokuSpace) -> SudokuBoard | None:
        """
        Propegate a given change throughout the entire board.

        Arg:
            selected_tile (SudokuSpace): The selected space to collapse the wavefunction under.

        Returns:
            The updated wavefunction if all spaces still have valid options. None otherwise.
        """
        current_board_copy: List[List[SudokuSpace]] = [
            [space.copy() for space in row] for row in self.wavefunction
        ]

        current_board_copy[selected_tile.y][selected_tile.x] = selected_tile.copy()
        stack: List[SudokuSpace] = [selected_tile]
        while len(stack) > 0:
            current_space = stack.pop()
            space: SudokuSpace
            for space in self.get_affected_spaces(
                current_board_copy, current_space.x, current_space.y
            ):
                if space.value is not None:
                    continue
                space_possible_values = space.possible_values
                current_space_neighbors = current_space.neighbors

                new_options = space_possible_values & current_space_neighbors
                if new_options and space.possible_values != new_options:
                    space.possible_values = new_options

                    if not space in stack:
                        stack.append(space)
                elif not new_options:
                    return None
        new_board = SudokuBoard(self.board_size)

        new_board._wavefunction = current_board_copy
        return new_board

    def __str__(self) -> str:
        """
        Visualizes the current state of the wavefunction.

        Returns:
            A string representation of the wavefunction
        """
        output: str = "--------" * self.board_size + "\n|"
        for row in self.wavefunction:
            for space in row:
                output = (
                    output
                    + (str(space.value) if space.value is not None else "None")
                    + "\t|"
                )
            output = output + "\n" + "|-------" * self.board_size + "|\n|"
        output = "\n".join(output.split("\n")[:-2])
        output = output + "\n" + "--------" * self.board_size
        return output[:-1]


def is_valid(board: List[List[SudokuSpace]]) -> bool:
    """
    Checks if a solved sudoku board is valid.

    Args:
        board (List[List[SudokuSpace]]): A solved sudoku board

    Returns:
        True if the solution is valid. False otherwise.
    """
    for row in board:
        if len(set(space.value for space in row)) != len(board):
            return False

    # Check columns
    for col in range(len(board)):
        column = [board[row][col] for row in range(len(board))]
        if len(set(space.value for space in column)) != len(board):
            return False

    square_size = int(len(board) ** 0.5)
    for i in range(0, len(board), square_size):
        for j in range(0, len(board), square_size):
            subgrid = [
                board[row][col]
                for row in range(i, i + square_size)
                for col in range(j, j + square_size)
            ]
            if len(set(space.value for space in subgrid)) != len(board):
                return False
    return True
