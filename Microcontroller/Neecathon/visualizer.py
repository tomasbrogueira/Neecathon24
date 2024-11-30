# Import matplotlib
import matplotlib.pyplot as plt

values = []

with open("data.txt", "r") as f:
    for line in f:
        values.append(int(line))

n = len(values)
step = 0.1 # seconds

time_series = [i * step for i in range(n)]

plt.plot(time_series, values)
plt.xlabel("Time (s)")
plt.ylabel("ADC Value")
plt.title("ADC Value vs Time")

plt.show()