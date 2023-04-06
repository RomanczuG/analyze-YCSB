import pandas as pd
import numpy as np

def analyze_results(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    data = {
        'operation': [],
        'latency': [],
        'throughput': []
    }

    for line in lines:
        if line.startswith("[READ]") or line.startswith("[UPDATE]"):
            parts = line.strip().split()
            data['operation'].append(parts[0][1:-1])
            if parts[1] == "AverageLatency(us)":
                data['latency'].append(float(parts[2]))
            elif parts[1] == "Throughput(ops/sec)":
                data['throughput'].append(float(parts[2]))

    df = pd.DataFrame(data)
    p95_latency = df['latency'].quantile(0.95)
    avg_throughput = df['throughput'].mean()

    print("P95 Latency (us):", p95_latency)
    print("Average Throughput (ops/sec):", avg_throughput)

if __name__ == "__main__":
    analyze_results("./outputRun.txt")