# A5: Calculate binomial coefficients using dynamic programming.
# C(n, k) = C(n-1, k-1) + C(n-1, k),  C(n, 0) = C(n, n) = 1

def binomial_coefficient(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]

    return dp[n][k], dp


n = int(input("Enter n: "))
k = int(input("Enter k: "))

if n < 0 or k < 0 or k > n:
    print("Error: n and k must be non-negative with k <= n.")
else:
    result, table = binomial_coefficient(n, k)
    print("DP table:")
    for row in table:
        print(row)
    print(f"C({n}, {k}) =", result)

# Time complexity: O(n*k), Space complexity: O(n*k)
