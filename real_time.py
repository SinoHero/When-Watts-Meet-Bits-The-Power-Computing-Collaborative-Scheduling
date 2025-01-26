import pandas as pd

green_energy_prices = [
    0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.4, 0.4,
    0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.5,
    0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6
]

data = {
    'Time（hour）': ['0～1', '1～2', '2～3', '3～4', '4～5', '5～6', '6～7', '7～8', '8～9', '9～10', '10～11', '11～12',
                   '12～13', '13～14', '14～15', '15～16', '16～17', '17～18', '18～19', '19～20', '20～21', '21～22',
                   '22～23', '23～24'],
    'Green Energy Supply (KWh)': [0, 0, 0, 0, 500, 1400, 1800, 2100, 2400, 2400, 2800, 3200, 3400, 3300, 3100, 2900, 2600,
                                  2500, 2300, 1500, 1000, 0, 0, 0],
    'Traditional Energy Price (RMB)': [0.5, 0.5, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0, 1.0,
                                       1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 0.8, 0.6],
    'Carbon Tax Added (RMB)': [0.7, 0.7, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.5, 1.4, 1.3, 1.2, 1.2, 1.3, 1.4,
                               1.5, 1.4, 1.3, 1.2, 1.0, 0.8],
    'Delay Penalty (RMB/h)': [0.2] + [None] * 23
}
df = pd.DataFrame(data)

input_time = input("请输入当前的时间段（格式为：几时-几时，例如：8-9）：")
required_energy = float(input("请输入所需电量（千瓦时）："))

start_hour, end_hour = map(int, input_time.split('-'))

green_energy_used = 0
green_energy_cost = 0
for hour in range(start_hour, end_hour):
    supply = df[df['Time（hour）'].str.startswith(str(hour))]['Green Energy Supply (KWh)'].values[0]
    available = min(required_energy - green_energy_used, supply)
    green_energy_used += available
    green_energy_cost += available * green_energy_prices[hour]

remaining_energy = max(0, required_energy - green_energy_used)

min_cost = float('inf')
min_cost_hour = None

for index in range(start_hour, 24):
    row = df.iloc[index]
    hour_price = row['Carbon Tax Added (RMB)']
    delay_hours = index - end_hour if index >= end_hour else 0
    penalty = delay_hours * 0.02
    total_cost = (remaining_energy * (hour_price + penalty)) + green_energy_cost

    if total_cost < min_cost:
        min_cost = total_cost
        min_cost_hour = index

print(f"最便宜的方案是在 {df.iloc[min_cost_hour]['Time（hour）']} 使用传统能源完成任务，一共需要花费 {min_cost:.2f} RMB")