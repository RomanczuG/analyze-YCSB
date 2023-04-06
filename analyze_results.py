import pandas as pd

def analyze_results(file_path):
    """
    Use ``analyze_results(file_path)`` to analyze the results of a benchmark test.
    This function will read the file at the given file path, parse the data, and
    print out two dataframes containing the results of the benchmark test.

    Parameters
    ----------
    file_path : str
        The path to the file containing the benchmark test results

    Returns
    ----------
    dfR : pandas.DataFrame
        DataFrame containing the results of the benchmark test for each operation
    dfO : pandas.DataFrame
        DataFrame containing the overall results of the benchmark test
    """
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

if __name__ == "__main__":
    # analyze_results("../YCSB/outputRun.txt")
    analyze_results("outputRun_50_50_mem_50mb.txt")