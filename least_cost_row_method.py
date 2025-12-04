from abc import ABC

from approximation_method import ApproximationMethod
import numpy as np


class LeastCostRowMethod(ApproximationMethod, ABC):

    def __init__(self, file):
        # Reads supply/demand/costs, balances, creates tables
        super().__init__(file=file)
        # Start from the first row (0-based)
        self._current_row = 0

    def solve(self) -> None:
        """
        Builds an initial solution using the Least Cost Row method:
        row 1, row 2, ..., last row, then back to row 1, and so on;
        in each row choose the cheapest feasible cell (demand > 0,
        column not deleted).
        """
        while self.has_rows_and_columns_left():
            self.choose_cost()

        # Write initial solution & cost
        self.writer.write_initial_solution(
            self.assign_table,
            demand=self.cost_table[self.demand_row],
            supply=self.cost_table[:, self.supply_column],
        )
        self.writer.write_initial_cost(self.total_cost())

        # Try to improve with MODI / stepping-stone style improvement
        self.improve()

    def _next_active_row(self, start_index: int) -> int:
        """
        Returns the next row index (>= 0 and < demand_row) that:
            - is not deleted, and
            - still has remaining supply.
        Starting from start_index (inclusive) and wrapping around.
        """
        n = self.demand_row  # last row is demand row, so rows are [0 .. demand_row-1]

        for offset in range(n):
            i = (start_index + offset) % n
            if i in self.deleted_rows:
                continue
            # Remaining supply is in the last column of assign_table
            if self.assign_table[i][self.supply_column] > 0:
                return i

        # No row can provide further supply
        self.halt("No active rows left in LeastCostRowMethod.")

    def choose_cost(self) -> None:
        """
        Pick the next row in round-robin order, then in that row choose the
        cheapest feasible column (not deleted, remaining demand > 0), and
        assign as much as possible to that cell.
        """
        # Find the row we will work on this iteration
        row = self._next_active_row(self._current_row)

        min_cost = np.inf
        min_j = -1

        # Search for the cheapest feasible column in this row
        for j in range(self.supply_column):  # exclude the supply column itself
            if j in self.deleted_cols:
                continue

            # Remaining demand is stored in the last row of assign_table
            if self.assign_table[self.demand_row][j] == 0:
                continue

            c = self.cost_table[row][j]
            if c < min_cost:
                min_cost = c
                min_j = j

        # If no column is feasible for this row, mark row as deleted and move on
        if min_j == -1:
            self.deleted_rows.add(row)
            # Advance row pointer for next time and let the main loop call again
            self._current_row = (row + 1) % self.demand_row
            return

        # Assign min(remaining supply, remaining demand) to that cell.
        # best_value_at(row, min_j) returns (best, i, j) and updates deleted rows/cols
        self.assign(*self.best_value_at(row, min_j))

        # Move to the next row for the next iteration (round-robin)
        self._current_row = (row + 1) % self.demand_row