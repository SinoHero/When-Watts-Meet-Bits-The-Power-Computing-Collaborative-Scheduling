import csv

with open("Tasks.csv", "r") as f:
    reader = csv.reader(f)
    tasks = [[float(value) for value in row] for row in list(reader)[1:]]

# Read and convert values in Costs.csv to floats
with open("Costs.csv", "r") as f:
    reader = csv.reader(f)
    costs = [[float(value) for value in row] for row in list(reader)[1:]]

cost = 0
for line in list(tasks)[1:]:
    energy = line[2] * 80 + line[3] * 50 + line[4] * 30
    mintrad = 99999
    mintradindex = -1
    for hour in costs[1:]:
        if line[0] <= hour[0] < line[1] and energy >= hour[2]*1000:
            energy -= int(hour[2])
            print(f"Used {hour[2]} clean at hour {hour[0]} for {hour[1]} per, total {hour[1] * hour[2] *1000}")
            cost += hour[1] * hour[2] *1000
        elif line[0] <= hour[0] < line[1] and energy < hour[2]*1000:
            cost += energy * hour[1]
            print(f"Used {hour[2]} clean at hour {hour[0]} for {hour[1]} per, total {energy * hour[1]}")
            energy = 0
        if line[0] <= hour[0] < line[1] and hour[3] < mintrad:
            mintrad = min(mintrad, hour[3])
            mintradindex = hour[0]
    
    cost += energy * (mintrad+0.2)
    print(f"Used {energy} kWh at hour {mintradindex} with a price of {mintrad+0.2}/kWh")

print(cost)