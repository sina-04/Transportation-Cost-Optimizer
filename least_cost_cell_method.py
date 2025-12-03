from abc import ABC

from approximation_method import ApproximationMethod
import numpy as np

class LeastCostCellMethod(ApproximationMethod, ABC):

    def __init__(self, file):
        # This will:
        #   - read supply/demand/costs from file
        #   - balance the problem (dummy rows/cols if needed)
        #   - create assign_table and transportation_table
        super().__init__(file=file)

    def solve(self) -> None:
        """
        Builds an initial solution using the Least Cost method:
        always pick the globally cheapest available cell.
        """
        # Keep assigning while there are rows/columns left
        while self.has_rows_and_columns_left():
            self.choose_cost()

        # Write initial solution & cost
        self.writer.write_initial_solution(
            self.assign_table,
            demand=self.cost_table[self.demand_row],
            supply=self.cost_table[:, self.supply_column],
        )
        self.writer.write_initial_cost(self.total_cost())

        # Try to improve with the MODI/transportation algorithm
        self.improve()

    def choose_cost(self) -> None:
        """
        Find the globally cheapest available (non-deleted) cost cell
        and assign as much as possible to it.
        """
        min_cost = np.inf
        min_i, min_j = -1, -1

        # Search over all still-available cells
        for i in range(self.demand_row):           # skip the demand row
            if i in self.deleted_rows:
                continue
            for j in range(self.supply_column):    # skip the supply column
                if j in self.deleted_cols:
                    continue

                c = self.cost_table[i][j]
                if c < min_cost:
                    min_cost = c
                    min_i, min_j = i, j

        # Safety check: should not happen if has_rows_and_columns_left() is True
        if min_i == -1 or min_j == -1:
            self.halt("No feasible cell found in LeastCostCellMethod.choose_cost()")

        # Assign min(demand, supply) to that cell.
        # best_value_at(i, j) returns (best, i, j) and also updates deleted rows/cols.
        self.assign(*self.best_value_at(min_i, min_j))
