def fractional_knapsack(values, weights, capacity):
    n = len(values)

    # Calculate value-to-weight ratio for each item
    items = []
    for i in range(n):
        ratio = values[i] / weights[i]
        items.append((ratio, values[i], weights[i]))

    # Sort items by ratio in descending order
    items.sort(reverse=True)

    total_value = 0.0

    for ratio, value, weight in items:
        if capacity >= weight:
            # Take the complete item
            total_value += value
            capacity -= weight
        else:
            # Take the fraction that fits
            total_value += ratio * capacity
            break

    return total_value


if __name__ == "__main__":
    values = list(map(int, input("Enter values: ").split()))
    weights = list(map(int, input("Enter weights: ").split()))
    capacity = int(input("Enter capacity: "))

    if len(values) != len(weights):
        print("Error: Values and weights must have equal lengths.")
    elif capacity < 0 or any(w <= 0 for w in weights):
        print("Error: Capacity must be non-negative and weights must be positive.")
    else:
        maximum_value = fractional_knapsack(values, weights, capacity)
        print("Maximum value:", maximum_value)
