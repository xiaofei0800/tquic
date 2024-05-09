#!/usr/bin/env python3

import os
import sys

import json
import matplotlib.pyplot as plt
import numpy as np
import prettytable
import termcolor

# Benchmark scenarios
SCENARIO = ["long", "short"]

# QUIC implements
IMPLS = ["tquic", "lsquic"]

# File sizes in long connection scenario benchmark
LONG_FILE_SIZES = ["15K", "50K", "2M"]

# File sizes in short connection scenario benchmark
SHORT_FILE_SIZES = ["1K"]

# Different concurrent connections
LONG_CONNS = [10]

# Different concurrent connections
SHORT_CONNS = [10]

# Different concurrent streams
LONG_STREAMS = [1, 10]

# Different concurrent streams
SHORT_STREAMS = [1]

# Read data from benchmark result file.
def read_data(data_dir, scen, impl, size, conn, stream):
    dirname = "benchmark_%s_%s_%s_%d_%d" % (scen, impl, size, conn, stream)
    filename = "benchmark_%s_%s_%s_%d_%d" % (scen, impl, size, conn, stream)
    path = os.path.join(data_dir, dirname, filename)
    try:
        with open(path) as f:
            data = f.read().strip()
            return float(data)
    except:
        return 0.0

# Put benchmark result in array according to implement.
def prepare_data(data_dir):
    titles = [' ' for _ in range((len(LONG_FILE_SIZES)*len(LONG_CONNS)*len(LONG_STREAMS) + len(SHORT_FILE_SIZES)*len(SHORT_CONNS)*len(SHORT_STREAMS)))]
    result = [[0.0 for _ in range(len(LONG_FILE_SIZES)*len(LONG_CONNS)*len(LONG_STREAMS) + len(SHORT_FILE_SIZES)*len(SHORT_CONNS)*len(SHORT_STREAMS))] for _ in range(len(IMPLS))]


    I = len(LONG_FILE_SIZES)
    J = len(LONG_CONNS)
    K = len(LONG_STREAMS)
    N = len(IMPLS)
    for i in range(I):
        for j in range(J):
            for k in range(K):
                titles[i*J*K+j*K+k] = "long %s %d %d" % (LONG_FILE_SIZES[i], LONG_CONNS[j], LONG_STREAMS[k])
                for n in range(N):
                    result[n][i*J*K+j*K+k] = read_data(data_dir, "long", IMPLS[n], LONG_FILE_SIZES[i], LONG_CONNS[j], LONG_STREAMS[k])

    M = len(LONG_FILE_SIZES)*len(LONG_CONNS)*len(LONG_STREAMS)
    I = len(SHORT_FILE_SIZES)
    J = len(SHORT_CONNS)
    K = len(SHORT_STREAMS)
    N = len(IMPLS)
    for i in range(I):
        for j in range(J):
            for k in range(K):
                titles[M+i*J*K+j*K+k] = "short %s %d %d" % (SHORT_FILE_SIZES[i], SHORT_CONNS[j], SHORT_STREAMS[k])
                for n in range(N):
                    result[n][M+i*J*K+j*K+k] = read_data(data_dir, "short", IMPLS[n], SHORT_FILE_SIZES[i], SHORT_CONNS[j], LONG_STREAMS[k])

    return titles, result

# Print benchmark performance result to stdout.
def show(titles, result):
    titles.insert(0, '')

    table = prettytable.PrettyTable()
    table.field_names = titles

    for i in range(len(result)):
        colored_row_name = termcolor.colored(IMPLS[i], 'green')
        table.add_row([colored_row_name] + result[i])

    print(table)

def plot(titles, result):

    N = len(titles)
    M = len(result)

    width = 0.35
    gap = 0.5

    ind = np.arange(N) * (width * M + gap)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    for i in range(M):
        ax.bar(ind + i*width, result[i], width, label=IMPLS[i])

    ax.set_ylabel('RPS')
    ax.set_title('TQUIC benchmark')
    ax.set_xticks(ind + width * M / 2)
    ax.set_xticklabels(titles, rotation=45)

    ax.legend()

    plt.savefig("benchmark_all.png", dpi=300)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s [data_dir]" % (sys.argv[0]))
        exit(1)

    data_dir= sys.argv[1]
    titles, result = prepare_data(data_dir)
    plot(titles, result)
    show(titles, result)


