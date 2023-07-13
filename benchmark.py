from mpi4py import MPI
import math
import matrix as mx
import generator
import random
from datetime import datetime
import time
import statistics

save_file = False
comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nprocs = comm.Get_size()

ROWS = 100
COLUMNS = 100

ROUNDS = 50

padding = 20
pad_round = 15

start:float = 0.0
end:float = 0.0

def round_pad(num: float):
    return round(num, pad_round)

def run(procs: int) -> mx.Row:
    """calculate the number of islands

    Returns:
        mx.Row: the final "ROW", there are all rows in it
    """

    global start
    global end
    if my_rank >= procs:
        return

    # generate a random matrix of the given size
    matrix: mx.Matrix
    if my_rank == 0:
        l = generator.generate(ROWS, COLUMNS)
        matrix = mx.list_to_matrix(l)

    # split the matrix and send them to their receivers
    # this is done in a binary-tree
    start = time.time()
    gens = math.ceil(math.log2(procs))
    for gen in range(gens):
        if 2**gen <= my_rank and my_rank < 2**(gen+1):
            get_from = my_rank-(2**gen)
            if get_from < procs:
                matrix = comm.recv(source=get_from)
        if my_rank < 2**gen:
            send_to = my_rank+2**gen
            if send_to < procs:
                m = mx.split_matrix(matrix, 2)
                matrix = m[0]
                comm.send(m[1], send_to)

    r = mx.count_islands(matrix)

    # send the calculated results to their receivers
    # merge the results
    # this is also done in a binary tree
    for gen in range(gens-1,-1,-1):
        if 2**gen <= my_rank and my_rank < 2**(gen+1):
            send_to = my_rank-2**gen
            if send_to < procs:
                comm.send(r, send_to)
        if my_rank < 2**gen:
            get_from = my_rank+(2**gen)
            if get_from < procs:
                r2 = comm.recv(source=get_from)
                r.merge(r2)

    end = time.time()
    return r

cores = []
i = 0
while 2**i <= nprocs:
    cores.append(2**i)
    i += 1
# for i in range(1, 33):
#     cores.append(i)

seed = int(round(datetime.now().timestamp()))
# for i in [100, 200, 400, 800, 1600, 3200, 6400]:
# for i in [1000]:
for i in [100, 200, 400, 800, 1600]:
    if my_rank == 0:
        print(f"Matrix size {i}x{i}:")
        print(f'{"Prozesse": <{10}} {"Durchschnitt": <{padding}} {"Standardabweichung": <{padding}} {"Median": <{padding}} {"Min": <{padding}} {"Max": <{padding}} {"Gesamt": <{padding}}')
        ROWS = i
        COLUMNS = i
    

    for core in cores:
        times = []
        random.seed(seed)
        for _ in range(ROUNDS):
            result = run(core)
            times.append(end-start)

        if my_rank == 0:
            print(f'{core: <{10}} ', end="")
            print(f'{round_pad(statistics.mean(times)): <{padding}} ' ,end="")
            print(f'{round_pad(statistics.stdev(times)): <{padding}} ' ,end="")
            print(f'{round_pad(statistics.median(times)): <{padding}} ' ,end="")
            print(f'{round_pad(min(times)): <{padding}} ', end="")
            print(f'{round_pad(max(times)): <{padding}} ', end="")
            print(f'{round_pad(sum(times)): <{padding}} ')

    if my_rank == 0:
        print("\n")
