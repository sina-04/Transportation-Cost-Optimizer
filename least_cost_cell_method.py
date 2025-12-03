import numpy as np
import timeit

Supply = [300, 400, 500]
Demand = [250, 350, 400, 200]

costs_matrix = np.array([
    [3, 1, 7, 4],
    [2, 6, 5, 9],
    [8, 3, 3, 2]
])

# Allocation matrix (same shape as cost matrix)
allocation = np.zeros_like(costs_matrix, dtype=int)

# While any supply or demand is still left
while sum(Supply) > 0 and sum(Demand) > 0:

    # Convert to float so infinity masking works
    masked_costs = costs_matrix.astype(float).copy()

    # Mask exhausted rows and columns
    for i in range(len(Supply)):
        if Supply[i] == 0:
            masked_costs[i, :] = np.inf

    for j in range(len(Demand)):
        if Demand[j] == 0:
            masked_costs[:, j] = np.inf

    # If everything is masked, stop
    if np.all(masked_costs == np.inf):
        break

    # Find minimum cost cell
    least_cost = np.min(masked_costs)
    row, col = np.where(masked_costs == least_cost)
    row, col = int(row[0]), int(col[0])

    # Allocate max possible amount
    quantity = min(Supply[row], Demand[col])
    allocation[row, col] = quantity

    # Reduce supply/demand
    Supply[row] -= quantity
    Demand[col] -= quantity

    print(f"Allocated {quantity} units to cell ({row}, {col}) with cost {least_cost}")
    print("Remaining Supply:", Supply)
    print("Remaining Demand:", Demand)
    print("---")

# Compute total cost
total_cost = np.sum(allocation * costs_matrix)

print("\nFinal Allocation Matrix:")
print(allocation)

print("\nTotal Transportation Cost:", total_cost)

t = timeit.timeit("sum(i*i for i in range(1000))", number=1000)
print(round(t, 4))