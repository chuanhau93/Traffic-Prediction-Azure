import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("traffic.csv")

df['DateTime'] = pd.to_datetime(df['DateTime'])

print(df.head())

print(df.info())

df['hour'] = df['DateTime'].dt.hour
df['days_of_week'] = df['DateTime'].dt.dayofweek
df['month'] = df['DateTime'].dt.month
df['is_weekend'] = df['days_of_week'].isin([5, 6]).astype(int)

print(df[['DateTime', 'hour', 'days_of_week', 'is_weekend']].head(10))

print("=== Average vehicles by hour of day (Junction 1) ===")

print(df[df['Junction'] == 1].groupby('hour')['Vehicles'].mean().round(1))

print("\n=== Average vehicles: Weekday vs Weekend (Junction 1) ===")

print(df[df['Junction'] == 1].groupby('is_weekend')['Vehicles'].mean().round(1))

plt.figure(figsize = (10, 5))

for j in sorted(df['Junction'].unique()):
    sub = df[df['Junction'] == j].groupby('hour')['Vehicles'].mean()
    plt.plot(sub.index, sub.values, marker = 'o', label = f'Junction{j}')

plt.title('Average Vehicles by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Average Vehicle Count')
plt.legend()
plt.grid(alpha = 0.3)
plt.savefig('eda_chart.png', dpi = 120)
plt.show()