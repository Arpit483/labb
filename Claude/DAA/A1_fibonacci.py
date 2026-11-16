# A1: Generate Fibonacci numbers and determine the number of computational steps required.
# F(1) = 0, F(2) = 1, F(3) = 1, ...

steps_iter = 0
steps_rec = 0


def fibonacci_iterative(n: int):
    global steps_iter
    steps_iter = 0
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        dp = [0] * n
        dp[0] = 0
        dp[1] = 1
        for i in range(2, n):
            dp[i] = dp[i - 1] + dp[i - 2]
            steps_iter += 1          # one addition per loop iteration
        return dp[n - 1]


def fibonacci_recursive(n):
    global steps_rec
    steps_rec = 0
    cache = {
        1: 0,
        2: 1
    }
    return helper(n, cache)


def helper(n: int, cache):
    global steps_rec
    steps_rec += 1                   # one step per function call
    if n in cache:
        return cache[n]
    else:
        return helper(n - 1, cache) + helper(n - 2, cache)


n = int(input("Enter value of n(nth Fibonacci number): "))
print("First", n, "Fibonacci numbers:", [fibonacci_iterative(i) for i in range(1, n + 1)])

print(f"Fibonacci Number(Iterative): {fibonacci_iterative(n)}")
print(f"Steps (Iterative): {steps_iter}")

print(f"Fibonacci Number(Recursive): {fibonacci_recursive(n)}")
print(f"Steps (Recursive calls): {steps_rec}")

# Time complexity:
#   Iterative : O(n) time, O(n) space (n-2 additions)
#   Recursive : O(2^n) time as written (the cache is never filled, so subproblems repeat)
