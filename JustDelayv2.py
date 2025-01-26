import csv

with open("Tasks.csv", "r") as f:
    reader = csv.reader(f)
    tasks = [[float(value) for value in row] for row in list(reader)[1:]]

# Read and convert values in Costs.csv to floats
with open("Costs.csv", "r") as f:
    reader = csv.reader(f)
    costs = [[float(value) for value in row] for row in list(reader)[1:]]


tasksraw = [(line[0], line[2] * 80 + line[3] * 50 + line[4] * 30) for line in tasks]
tasks = [0] * 24
for a, b in tasksraw:
    tasks[int(a)] = int(int(b)/10)
energy_per_task = [1] * 24 #2 energy per task
cheap_energy_quota = [int(costs[i][2]*100) for i in range(24)]
cheap_energy_price = [int(costs[i][1]*10) for i in range(24)]
expensive_energy_price = [int(costs[i][3]*10+2) for i in range(24)]

total = int(sum(tasks))


dp = []

for i in range(tasks[0]):
    energy_use = tasks[0] - i
    if energy_use > cheap_energy_quota[0]:
        dp.append(cheap_energy_price[0] * cheap_energy_quota[0] + expensive_energy_price[0] * (energy_use - cheap_energy_quota[0]))
    else:
        dp.append(cheap_energy_price[0] * energy_use)
dp.append(0)
for _ in range(total-tasks[0]-1):
    dp.append(9999999)

for i in range(24):
    if i == 0:
        continue
    for j in range(total):
        for k in range(total-1, j-1, -1):
            energy_use = k-j
            if energy_use <= cheap_energy_quota[i]:
                dp[j] = min(dp[j], dp[k] + cheap_energy_price[i] * energy_use)
            else:
                dp[j] = min(dp[j], dp[k] + cheap_energy_price[i] * cheap_energy_quota[i] + expensive_energy_price[i] * (energy_use - cheap_energy_quota[i]))

    for j in range(total-1, tasks[i]-1, -1):
        dp[j] = dp[j-tasks[i]]
    for j in range(tasks[i]):
        dp[j] = 99999999
    print(f'{i} done, cost:{dp[tasks[i]]}')