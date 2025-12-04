from abc import ABC

from approximation_method import ApproximationMethod
import numpy as np

class LeastCostColumnMethod(ApproximationMethod, ABC):

    def __init__(self, file):
        # Reads supply/demand/costs, balances, creates tables
        super().__init__(file=file)
        # Start from the first column (0-based, excluding the supply column)
        self._current_col = 0

    def solve(self) -> None:
        """
        Builds an initial solution using the Least Cost Column method:
        column 1, column 2, ..., last column, then back to column 1, and so on;
        in each column choose the cheapest feasible cell (supply > 0, row not deleted).
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

    def _next_active_column(self, start_index: int) -> int:
        """
        Returns the next column index (>= 0 and < supply_column) that:
            - is not deleted, and
            - still has remaining demand.
        Starting from start_index (inclusive) and wrapping around.
        """
        n = self.supply_column  # last column is supply, so usable cols are [0 .. supply_column-1]

        for offset in range(n):
            j = (start_index + offset) % n
            if j in self.deleted_cols:
                continue
            # Remaining demand is in the last row of assign_table
            if self.assign_table[self.demand_row][j] > 0:
                return j

        # No column can accept further demand
        self.halt("No active columns left in LeastCostColumnMethod.")

    def choose_cost(self) -> None:
        """
        Pick the next column in round-robin order, then in that column choose the
        cheapest feasible row (not deleted, remaining supply > 0), and assign as much as possible to that cell.
        """
        # Find the column we will work on this iteration
        col = self._next_active_column(self._current_col)

        min_cost = np.inf
        min_i = -1

        # Search for the cheapest feasible row in this column
        for i in range(self.demand_row):  # exclude the demand row itself
            if i in self.deleted_rows:
                continue

            # Remaining supply is stored in the last column of assign_table
            if self.assign_table[i][self.supply_column] == 0:
                continue

            c = self.cost_table[i][col]
            if c < min_cost:
                min_cost = c
                min_i = i

        # If no row is feasible for this column, mark column as deleted and move on
        if min_i == -1:
            self.deleted_cols.add(col)
            # Advance column pointer for next time and let the main loop call again
            self._current_col = (col + 1) % self.supply_column
            return

        # Assign min(remaining supply, remaining demand) to that cell.
        # best_value_at(min_i, col) returns (best, i, j) and updates deleted rows/cols
        self.assign(*self.best_value_at(min_i, col))

        # Move to the next column for the next iteration (round-robin)
        self._current_col = (col + 1) % self.supply_column
