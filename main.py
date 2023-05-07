#! /usr/bin/python3
from lib.game import Game
import numpy as np
import argparse
from tqdm import tqdm
import multiprocessing


NUM_PROCESSES = 20
ITER_PER_PROCESS = 50


def benchmark_helper(res, proc_id, ITER_PER_PROCESS):
    options = {"portal": True, "block": True, "bot": True}
    game = Game(options, event_cycle=1)
    for i in tqdm(range(ITER_PER_PROCESS)):
        res[i + (proc_id * ITER_PER_PROCESS)] = game.one_iter()


def benchmark():
    arr = multiprocessing.Array('i', [0] * (ITER_PER_PROCESS * NUM_PROCESSES))
    processes = [None] * NUM_PROCESSES
    for i in range(NUM_PROCESSES):
        processes[i] = multiprocessing.Process(
            target=benchmark_helper, args=(arr, i, ITER_PER_PROCESS,))

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    res = np.array(arr)
    print(res)
    print("Mean:", np.mean(res))
    print("Median:", np.median(res))
    print("Std:", np.std(res))
    print("Max:", np.amax(res))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--benchmark', action="store_true")
    parser.add_argument('-p', '--processes', type=int)
    parser.add_argument('-i', '--iteration', type=int)
    args = parser.parse_args()

    if args.processes is not None:
        NUM_PROCESSES = args.processes
    if args.iteration is not None:
        ITER_PER_PROCESS = args.iteration

    if args.benchmark:
        benchmark()
    else:
        options = {"portal": True, "block": True, "bot": False}
        game = Game(options)
        game.game_start()
