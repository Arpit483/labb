# A2: Greedy algorithm for Job Sequencing with deadlines.
# Idea: sort jobs by profit (descending); put each job in the latest free slot
# on or before its deadline.

def job_sequencing(jobs):
    # jobs: list of (job_id, deadline, profit)
    jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(j[1] for j in jobs)
    slots = [None] * (max_deadline + 1)   # slots[1..max_deadline]

    total_profit = 0
    for job_id, deadline, profit in jobs:
        for t in range(deadline, 0, -1):
            if slots[t] is None:
                slots[t] = job_id
                total_profit += profit
                break

    sequence = [s for s in slots[1:] if s is not None]
    return sequence, total_profit


n = int(input("Enter number of jobs: "))
jobs = []
for i in range(n):
    job_id = input(f"Enter job id {i + 1}: ")
    deadline = int(input(f"Enter deadline of job {job_id}: "))
    profit = int(input(f"Enter profit of job {job_id}: "))
    jobs.append((job_id, deadline, profit))

if any(d <= 0 or p < 0 for _, d, p in jobs):
    print("Error: Deadlines must be positive and profits non-negative.")
else:
    sequence, total_profit = job_sequencing(jobs)
    print("Job sequence:", sequence)
    print("Maximum profit:", total_profit)

# Time complexity: O(n^2) (O(n log n) with a disjoint-set structure)
