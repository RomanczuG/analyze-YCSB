import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_results(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    data = {
        'operation': [],
        'average_latency': [],
        '95_latency': [],
        '99_latency': [],
        # 'throughput': []
    }
    overall = {
        'Runtime(ms)': [],
        'Throughput(ops/sec)': [],
    }

    for line in lines:
        if line.startswith("[READ]") or line.startswith("[UPDATE]") or line.startswith("[INSERT]") or line.startswith("[CLEANUP]"):
            parts = line.strip().split()
            for operation in ["[READ]", "[UPDATE]", "[INSERT]", "[CLEANUP]"]:
                if operation not in data['operation'] and operation == parts[0][0:-1]:
                    data['operation'].append(parts[0][0:-1])
            
            if parts[1] == "AverageLatency(us),":
                data['average_latency'].append(float(parts[2]))
            if parts[1] == "95thPercentileLatency(us),":
                data['95_latency'].append(float(parts[2]))
            if parts[1] == "99thPercentileLatency(us),":
                data['99_latency'].append(float(parts[2]))
            elif parts[1] == "Throughput(ops/sec),":
                data['throughput'].append(float(parts[2]))
        elif line.startswith("[OVERALL]"):
            parts = line.strip().split()
            if parts[1] == "RunTime(ms),":
                overall['Runtime(ms)'].append(float(parts[2]))
            elif parts[1] == "Throughput(ops/sec),":
                overall['Throughput(ops/sec)'].append(float(parts[2]))
    print(file_path)
    dfR = pd.DataFrame(data)
    dfO = pd.DataFrame(overall)
    print (dfR)
    print (dfO)
    return dfR, dfO

def create_grouped_bar_plots(df_dict, title, ylabel, measurements):
    configurations = list(df_dict.keys())
    num_configurations = len(configurations)
    
    # measurements = []
    num_measurements = len(measurements)
    
    bar_width = 0.25
    bar_spacing = 0.05
    group_spacing = 0.3
    group_width = num_configurations * bar_width + (num_configurations - 1) * bar_spacing
    
    fig, ax = plt.subplots()
    
    colors = plt.cm.get_cmap('tab10', num_configurations)
    
    for j, measurement in enumerate(measurements):
        for i, config in enumerate(configurations):
            if measurement in df_dict[config]['operation'].values:
                data = df_dict[config].loc[df_dict[config]['operation'] == measurement, 'average_latency'].values[0]
                ax.bar(j * (group_width + group_spacing) + i * (bar_width + bar_spacing), data, bar_width, label=config if j == 0 else "", color=colors(i))
    
    ax.set_xlabel('Measurement')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(np.arange(num_measurements) * (group_width + group_spacing) + (group_width - bar_width) / 2)
    ax.set_xticklabels(measurements)
    ax.legend()
    
    fig.tight_layout()
    plt.show()


def create_another_bar(dfOa, title, ylabel):
    configurations = list(dfOa.keys())
    measurements = dfOa[configurations[0]].columns.tolist()
    num_configurations = len(configurations)
    num_measurements = len(measurements)
    bar_width = 0.15
    indices = np.arange(num_measurements)
    fig, ax = plt.subplots()

    colors = plt.cm.get_cmap('tab10', num_configurations)
    
    for i, config in enumerate(configurations):
        values = dfOa[config].loc[0].tolist()
        ax.bar(indices + i * bar_width, values, bar_width, color=colors.colors[i], label=config)

    ax.set_xlabel('Measurement')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(indices + bar_width * (num_configurations - 1) / 2)
    ax.set_xticklabels(measurements)
    ax.legend(title='Configurations')

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    # analyze_results("../YCSB/outputRun.txt")
    dfRa = {}
    dfOa = {}
    for configuration in ["outputRun_50_50_mem_50mb.txt", "outputRun_50_50_mem_150mb.txt", "outputRun_50_50_mem_1gb.txt"]: 
        dfR, df0 = analyze_results(configuration)
        dfRa[configuration] = dfR
        dfOa[configuration] = df0
    
    create_grouped_bar_plots(dfRa, 'Run test for different memory allocation', 'Latency (us)', ['[READ]', '[UPDATE]', '[CLEANUP]'])
    # create_another_bar(dfOa['outputRun_50_50_mem_50mb.txt'], 'Run test for different memory allocation', 'Runtime (ms)')
    create_another_bar(dfOa, 'Run test for different memory allocation', '')
    dfRa = {}
    dfOa = {}
    for configuration in ["outputLoad_50_50_mem_50mb.txt", "outputLoad_50_50_mem_150mb.txt", "outputLoad_50_50_mem_1gb.txt"]:
        dfR, df0 = analyze_results(configuration)
        dfRa[configuration] = dfR
        dfOa[configuration] = df0
    create_grouped_bar_plots(dfRa, 'Load test for different memory allocation', 'Latency (us)', ['[CLEANUP]', '[INSERT]'])
    create_another_bar(dfOa, 'Load test for different memory allocation', '')
    dfRa = {}
    dfOa = {}

    for configuration in ["outputRun_50_50.txt", "outputRun_90_10.txt"]:
        dfR, df0 = analyze_results(configuration)
        dfRa[configuration] = dfR
        dfOa[configuration] = df0
    create_grouped_bar_plots(dfRa, 'Run test for different ratio of update operations', 'Latency (us)', ['[READ]', '[UPDATE]', '[CLEANUP]'])
    create_another_bar(dfOa, 'Run test for different ratio of update operations', '')
    dfRa = {}
    dfOa = {}
    for configuration in [ "outputLoad_50_50.txt", "outputLoad_90_10.txt"]:
        dfR, df0 = analyze_results(configuration)
        dfRa[configuration] = dfR
        dfOa[configuration] = df0
    create_grouped_bar_plots(dfRa, 'Load test for different ratio of update operations', 'Latency (us)', ['[CLEANUP]', '[INSERT]'])
    create_another_bar(dfOa, 'Load test for different ratio of update operations', '')


