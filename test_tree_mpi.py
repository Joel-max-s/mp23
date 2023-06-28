from mpi4py import MPI
import math
import matrix as mx
import generator
import time

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nprocs = comm.Get_size()

start_p: float

matrix: mx.Matrix
if my_rank == 0:
    l = generator.generate(1000, 1000)
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

r = mx.countIslands(matrix)

for gen in range(gens-1, -1, -1):
    if 2**gen <= my_rank and my_rank < 2**(gen+1):
        send_to = my_rank-2**gen
        if send_to < nprocs:
            comm.send(r, send_to)
    if my_rank < 2**gen:
        get_from = my_rank+(2**gen)
        if get_from < nprocs:
            r2 = comm.recv(source=get_from)
            r.merge(r2)

if my_rank == 0:
    end_p = time.time()
    print(len(r.islands))

    start_s = time.time()
    matrix2 = mx.list_to_matrix(l)
    seq = mx.countIslands(matrix2)
    end_s = time.time()
    print(len(seq.islands))

    print(f"Parallel: {end_p-start_p}")
    print(f"Sequenziell: {end_s-start_s}")
