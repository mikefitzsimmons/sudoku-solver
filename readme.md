Plan: Explainable Sudoku Solver
Status: Implemented and verified.

TL;DR: A pure-Python Sudoku solver was built around a compact 9x9 board, set-based constraint checks, recursive backtracking, and a lightweight trace of each decision. The implementation prioritizes readability, correctness, and educational value while keeping the board and solver logic straightforward and testable.

Completed design
Define the board model and public API.
- Implemented a mutable Board class with get_cell, set_cell, is_valid_move, find_empty_cells, is_complete, has_conflicts, and a copy method.
- This keeps the solver logic separate from the board representation and makes validation easy to test.

Implement constraint logic with Python-native structures.
- Added generate_candidates using set operations and row/column/3x3 box checks.
- Candidate generation is the core explanation for why a move is legal.

Build the recursive solver engine.
- Implemented a SudokuSolver using deterministic candidate ordering and "pick the cell with the fewest candidates" logic.
- Recursive calls assign a value, recurse, and backtrack cleanly when a branch fails.

Add trace events for step-by-step walkthroughs.
- Each solver run records assignment, candidate test, rejection, dead-end, and backtrack events with reasons.
- The trace is stored separately from the board state, which keeps the logic testable and the output readable.

Add validation and edge-case coverage.
- Included tests for a standard puzzle, solved puzzle, unsolvable puzzle, illegal move detection, and a backtracking-heavy puzzle.
- The solver returns None for invalid or unsolvable states instead of crashing or looping.

Relevant components
- Core board and constraint module: sudoku_solver.py
- Demo runner: demo.py
- Tests: tests/test_sudoku_solver.py

Verification
- The suite verifies solving correctness for a standard Sudoku, already-solved board, unsolvable board, and a board requiring backtracking.
- The trace includes assignment and backtrack reasons, and the solver reports impossible states cleanly.
- Final verification command:
  "C:\Users\mikee\AppData\Local\Programs\Python\Python312\python.exe" -m pytest -q

Decisions made
- Python built-ins such as sets, tuples, and lists are used for readability and speed.
- Candidate ordering and empty-cell selection are deterministic and reproducible.
- The solver is focused on a small, explicit API rather than over-engineered abstractions.
- The trace remains independent from the board state so it can be tested without presentation-specific details.

Further considerations
- A richer step-by-step mode can be added later by pausing after each assignment.
- Additional heuristics such as hidden singles can be layered on after the core solver is stable.
- The design remains reusable as a library and runnable as a demo script.
