def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for item in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[item - 1] <= w:
                include = (
                    dp[item - 1][w - weights[item - 1]]
                    + values[item - 1]
                )
                exclude = dp[item - 1][w]
                dp[item][w] = max(include, exclude)
            else:
                dp[item][w] = dp[item - 1][w]

    return dp[n][capacity]


if __name__ == "__main__":
    values = list(map(int, input("Enter values: ").split()))
    weights = list(map(int, input("Enter weights: ").split()))
    capacity = int(input("Enter capacity: "))

    if len(values) != len(weights):
        print("Error: Values and weights must have equal lengths.")
    elif capacity < 0 or any(w < 0 for w in weights):
        print("Error: Capacity and weights must be non-negative.")
    else:
        print("Maximum value:", knapsack(values, weights, capacity))
