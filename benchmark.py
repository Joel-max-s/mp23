from mpi4py import MPI
import math
import matrix as mx
import generator
import time
import argparse

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nprocs = comm.Get_size()

ROWS = 10
COLUMNS = 10

def run():
    start_p: float

    matrix: mx.Matrix
    if my_rank == 0:
        l = generator.generate(ROWS, COLUMNS)
        # l = [[0,1,0,0,0,0,0,0],
        #      [0,1,0,0,0,1,0,0],
        #      [0,0,1,0,1,0,0,0],
        #      [0,0,0,1,0,0,0,0]]
        start_p = time.time()
        matrix = mx.list_to_matrix(l)

    gens = math.ceil(math.log2(nprocs))
    for gen in range(gens):
        if 2**gen <= my_rank and my_rank < 2**(gen+1):
            get_from = my_rank-(2**gen)
            if get_from < nprocs:
                matrix = comm.recv(source=get_from)
        if my_rank < 2**gen:
            send_to = my_rank+2**gen
            if send_to < nprocs:
                m = mx.split_matrix(matrix, 2)
                matrix = m[0]
                comm.send(m[1], send_to)
                # print(f"Send {my_rank} to {send_to}")           

    r = mx.count_islands(matrix)

    for gen in range(gens-1,-1,-1):
        if 2**gen <= my_rank and my_rank < 2**(gen+1):
            send_to = my_rank-2**gen
            if send_to < nprocs:
                comm.send(r, send_to)
        if my_rank < 2**gen:
            get_from = my_rank+(2**gen)
            if get_from < nprocs:
                r2 = comm.recv(source=get_from)
                r.merge(r2)
                # print(f"Merged {my_rank} with {get_from}")
                # print(r)

    if my_rank == 0:
        end_p = time.time()
        # print(len(r.islands))

        start_s = time.time()
        matrix2 = mx.list_to_matrix(l)
        seq = mx.count_islands(matrix2)
        end_s = time.time()
        # print(len(seq.islands))

        # print(f"Parallel: {end_p-start_p}")
        # print(f"Sequenziell: {end_s-start_s}")


        # print(r)
        # print("\n"*3)
        # print(seq)
        return [r, seq, end_p-start_p, end_s-start_s]
    

if my_rank == 0:
    parser = argparse.ArgumentParser(prog="Pruefungsprojekt mp23", exit_on_error=False)
    parser.add_argument('rows', type=int)
    parser.add_argument('columns', type=int)
    parser.add_argument('-b', '--benchmark', type=int)
    try:
        args = parser.parse_args()
        ROWS = int(args.rows)
        COLUMNS = int(args.columns)

    except argparse.ArgumentError:
        print('You need to specify the number of rows and columns')
        print('Example: mpirun --use-hwthread-cpus -np 8 python3 main.py 100 100')
        comm.Abort(1)

    
count = 0
par_times = []
seq_times = []
for _ in range(100):
    ret = run()
    if my_rank == 0:
        print(count)
        if len(ret[0].islands) != len(ret[1].islands):
            break
        par_times.append(ret[2])
        seq_times.append(ret[3])
    count += 1

if my_rank == 0:
    print(f'Successfully ran {len(par_times)} times')
    print(f'Avg. parallel time: {sum(par_times)/len(par_times)}')
    print(f'Avg. seq time:      {sum(seq_times)/len(seq_times)}')    