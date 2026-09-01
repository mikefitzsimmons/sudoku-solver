from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Set, Tuple


class Board:
    """Represents a mutable 9x9 Sudoku board."""

    SIZE = 9
    BOX_SIZE = 3

    def __init__(self, grid: Sequence[Sequence[int]]):
        if len(grid) != self.SIZE or any(len(row) != self.SIZE for row in grid):
            raise ValueError("Board must be a 9x9 grid.")
        self.grid = [list(row) for row in grid]

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[int]]) -> "Board":
        return cls(rows)

    def get_cell(self, row: int, col: int) -> int:
        return self.grid[row][col]

    def set_cell(self, row: int, col: int, value: int) -> None:
        self.grid[row][col] = value

    def find_empty_cells(self) -> List[Tuple[int, int]]:
        return [(row, col) for row in range(self.SIZE) for col in range(self.SIZE) if self.grid[row][col] == 0]

    def is_complete(self) -> bool:
        return all(cell != 0 for row in self.grid for cell in row)

    def is_valid_move(self, row: int, col: int, value: int) -> bool:
        if not 1 <= value <= 9:
            return False
        if self.grid[row][col] != 0:
            return False

        for idx in range(self.SIZE):
            if idx != col and self.grid[row][idx] == value:
                return False
            if idx != row and self.grid[idx][col] == value:
                return False

        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(start_row, start_row + self.BOX_SIZE):
            for c in range(start_col, start_col + self.BOX_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True

    def has_conflicts(self) -> bool:
        for row in range(self.SIZE):
            seen = set()
            for col in range(self.SIZE):
                value = self.grid[row][col]
                if value == 0:
                    continue
                if value in seen:
                    return True
                seen.add(value)

        for col in range(self.SIZE):
            seen = set()
            for row in range(self.SIZE):
                value = self.grid[row][col]
                if value == 0:
                    continue
                if value in seen:
                    return True
                seen.add(value)

        for box_row in range(0, self.SIZE, self.BOX_SIZE):
            for box_col in range(0, self.SIZE, self.BOX_SIZE):
                seen = set()
                for row in range(box_row, box_row + self.BOX_SIZE):
                    for col in range(box_col, box_col + self.BOX_SIZE):
                        value = self.grid[row][col]
                        if value == 0:
                            continue
                        if value in seen:
                            return True
                        seen.add(value)
        return False

    def copy(self) -> "Board":
        return Board(self.grid)

    def __iter__(self):
        return iter(self.grid)

    def __repr__(self) -> str:
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)


def _to_board(grid: Sequence[Sequence[int]]) -> Board:
    if isinstance(grid, Board):
        return grid
    return Board(grid)


def generate_candidates(board: Board, row: int, col: int) -> Set[int]:
    """Return the legal values for a cell, assuming it is empty."""
    cell_value = board.get_cell(row, col)
    if cell_value != 0:
        return set()

    used: Set[int] = set()
    for idx in range(9):
        used.add(board.get_cell(row, idx))
        used.add(board.get_cell(idx, col))

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            used.add(board.get_cell(r, c))

    used.discard(0)
    return set(range(1, 10)) - used


class SudokuSolver:
    """Backtracking solver with a lightweight reasoning trace."""

    def __init__(self) -> None:
        self.trace: List[dict] = []

    def _record(self, action: str, row: int, col: int, value: Optional[int], reason: str) -> None:
        self.trace.append({
            "step": len(self.trace) + 1,
            "row": row,
            "col": col,
            "value": value,
            "action": action,
            "reason": reason,
        })

    def _select_best_cell(self, board: Board) -> Optional[Tuple[int, int, List[int]]]:
        best: Optional[Tuple[int, int, List[int]]] = None
        for row, col in board.find_empty_cells():
            candidates = sorted(generate_candidates(board, row, col))
            if not candidates:
                return row, col, []
            if best is None or len(candidates) < len(best[2]):
                best = (row, col, candidates)
        return best

    def _search(self, board: Board) -> bool:
        selection = self._select_best_cell(board)
        if selection is None:
            return True

        row, col, candidates = selection
        if not candidates:
            self._record("dead_end", row, col, None, "No legal candidates remain for this cell.")
            return False

        self._record("candidate_test", row, col, None, f"Evaluating candidates {candidates}.")

        for value in candidates:
            if not board.is_valid_move(row, col, value):
                self._record("reject", row, col, value, "Candidate violates Sudoku constraints.")
                continue

            board.set_cell(row, col, value)
            self._record("assignment", row, col, value, "Chosen as the next legal move.")

            if self._search(board):
                return True

            board.set_cell(row, col, 0)
            self._record("backtrack", row, col, value, "Recursive branch failed; undoing assignment.")

        self._record("dead_end", row, col, None, "No candidate led to a valid completion.")
        return False

    def solve(self, grid: Sequence[Sequence[int]]) -> Optional[List[List[int]]]:
        board = _to_board(grid)
        self.trace.clear()

        if board.has_conflicts():
            self._record("invalid", -1, -1, None, "Board violates row, column, or box constraints.")
            return None

        if self._search(board):
            return [row[:] for row in board.grid]
        return None

    def solve_with_trace(self, grid: Sequence[Sequence[int]]) -> List[dict]:
        self.solve(grid)
        return list(self.trace)


def solve_sudoku(grid: Sequence[Sequence[int]]) -> Optional[List[List[int]]]:
    solver = SudokuSolver()
    return solver.solve(grid)


def main() -> None:
    sample = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    solver = SudokuSolver()
    solution = solver.solve(sample)
    if solution is None:
        print("No solution found.")
        return

    print("Solved board:")
    for row in solution:
        print(" ".join(str(value) for value in row))

    print("\nTrace:")
    for event in solver.trace[:10]:
        print(event)


if __name__ == "__main__":
    main()
