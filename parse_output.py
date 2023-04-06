import re
import matplotlib.pyplot as plt

def parse_ycsb_output(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    throughput = float(re.search(r"Throughput\(ops/sec\), ([\d\.]+)", content).group(1))
    p95_latency = float(re.search(r"READ], 95thPercentileLatency\(us\), ([\d\.]+)", content).group(1))

    return throughput, p95_latency

# Replace the file paths with the paths of your YCSB output files
output_files = ["output_256MB.txt", "output_512MB.txt", "output_1024MB.txt"]

throughput = []
p95_latency = []

for file_path in output_files:
    t, l = parse_ycsb_output(file_path)
    throughput.append(t)
    p95_latency.append(l)

memory_allocations = [256, 512, 1024]

# Use the provided visualization script to plot the results
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Memory Allocation (MB)')
ax1.set_ylabel('Throughput (ops/sec)', color=color)
ax1.plot(memory_allocations, throughput, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('P95 Latency (us)', color=color)
ax2.plot(memory_allocations, p95_latency, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Throughput and P95 Latency vs Memory Allocation')
plt.show()