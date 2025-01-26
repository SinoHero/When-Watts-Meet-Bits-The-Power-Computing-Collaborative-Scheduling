import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 绿色能源每小时价格
green_energy_prices = [
    0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.4, 0.4,
    0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.5,
    0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6
]

# 假设数据存储在一个 DataFrame 中，这里简单模拟数据
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
}
df = pd.DataFrame(data)

# 传统能源每小时供给上限
traditional_energy_supply_limit = 1000

# 给绿色能源供给添加扰动
# 假设扰动是一个 -10% 到 10% 的随机数
for i in range(len(df)):
    perturbation = np.random.uniform(-0.1, 0.1)
    df.at[i, 'Green Energy Supply (KWh)'] = max(0, df.at[i, 'Green Energy Supply (KWh)'] * (1 + perturbation))

# 获取用户输入
input_time = input("请输入当前的时间段（格式为：几时-几时，例如：8-9）：")
required_energy = float(input("请输入所需电量（千瓦时）："))

# 解析输入的时间段
start_hour, end_hour = map(int, input_time.split('-'))

# 计算输入时间段内绿色能源的总供应量
green_energy_used = 0
green_energy_cost = 0
for hour in range(start_hour, end_hour):
    supply = df[df['Time（hour）'].str.startswith(str(hour))]['Green Energy Supply (KWh)'].values[0]
    available = min(required_energy - green_energy_used, supply)
    green_energy_used += available
    green_energy_cost += available * green_energy_prices[hour]

# 计算需要传统能源补充的电量
remaining_energy = max(0, required_energy - green_energy_used)

# 用于存储每个小时的 price、penalty 和总费用
cost_info = []
for index in range(start_hour, 24):
    row = df.iloc[index]
    hour_price = row['Carbon Tax Added (RMB)']
    delay_hours = index - end_hour if index >= end_hour else 0
    penalty = delay_hours * 0.01
    total_cost_per_kwh = hour_price + penalty
    cost_info.append((index, total_cost_per_kwh))

# 按总费用排序
cost_info.sort(key=lambda x: x[1])

# 开始分配传统能源
traditional_energy_cost = 0
for index, total_cost_per_kwh in cost_info:
    if remaining_energy <= 0:
        break
    supply = min(remaining_energy, traditional_energy_supply_limit)
    traditional_energy_cost += supply * total_cost_per_kwh
    remaining_energy -= supply

total_cost = green_energy_cost + traditional_energy_cost
best_time_slot = df.iloc[cost_info[0][0]]['Time（hour）']
print(f"最便宜的方案起始时段是 {best_time_slot}，一共需要花费 {total_cost:.2f} RMB")

# 用于绘制柱状图的数据
prices = []
penalties = []
hours = []
for index in range(start_hour, 24):
    row = df.iloc[index]
    hour_price = row['Traditional Energy Price (RMB)'] + row['Carbon Tax Added (RMB)']
    delay_hours = index - start_hour if index >= end_hour else 0
    penalty = delay_hours * 0.01
    prices.append(hour_price)
    penalties.append(penalty)
    hours.append(df.iloc[index]['Time（hour）'])

# 绘制柱状图
fig, ax = plt.subplots()
bottom = [0] * len(hours)
bars_price = ax.bar(hours, prices, label='Price', bottom=bottom, color='#BDCDEA')
bottom = [p for p in prices]
bars_penalty = ax.bar(hours, penalties, label='Penalty', bottom=bottom, color='#EDE2A4')

# 添加图例
ax.legend()

# 添加标题和坐标轴标签
ax.set_title('Price + Penalty over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Cost (RMB)')

# 旋转 x 轴标签以便更好显示
plt.xticks(rotation=45)

# 显示图形
plt.show()