from mpi4py import MPI
import generator
import pruefung
import time
import matrix as mx
import math

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nprocs = comm.Get_size()

matrix: mx.Matrix
if my_rank == 0:
    l = generator.generate(1000, 1000)
    matrix = mx.list_to_matrix(l)


gens = math.ceil(math.log2(nprocs))
for gen in range(gens):
    if 2**gen <= my_rank and my_rank < 2**(gen-1):
        recv = comm.recv(source=my_rank-2**gen)
        
    if my_rank < 2**gen:
        m = mx.split_matrix(matrix, 2)
        matrix = m[0]
        comm.send(m[1], my_rank+2**gen)



# l = [[0,1,0,0,0,0,0,0],
#      [0,1,0,0,0,1,0,0],
#      [0,0,1,0,1,0,0,0],
#      [0,0,0,1,0,0,0,0]]

# matrix = generator.generate_with_isles(1000, 1000, 100)

start = time.time()
if my_rank == 0:
    l = generator.generate(1000, 1000)
    matrix = mx.list_to_matrix(l)
    m = mx.split_matrix(matrix, 2)

    if nprocs >= 2:
        s = math.ceil(nprocs / 2)
        comm.send(m[0], 1)
        comm.send(m[1], 4)
        calced = comm.recv(source=1)
        m2 = comm.recv(source=4)
        calced.merge(m2)
        end = time.time()
        print(f'Parallel: {end-start}')

    start = time.time()
    seq = mx.countIslands(matrix)
    end = time.time()
    print(f'Sequenziell: {end-start}')
    print(len(calced.islands))
    print(len(seq.islands))

else:
    if my_rank in [1,4]:
        data = comm.recv()
        d = mx.split_matrix(data, 2)
        comm.send(d[0], my_rank+1, tag=my_rank)
        comm.send(d[1], my_rank+2, tag=my_rank)
        m1 = comm.recv(source=my_rank+1)
        m2 = comm.recv(source=my_rank+2)
        m1.merge(m2)
        comm.send(m1, 0)
    else:
        d: mx.Matrix = comm.recv()
        r = mx.countIslands(d)
        if my_rank in [2,5]:
            comm.send(r, my_rank-1)
        elif my_rank in [3,6]:
            comm.send(r, my_rank-2)

# else:
#     data = comm.recv(source=0)
#     calced = mx.countIslands(data)
#     comm.send(calced, 0)
    
# else:
#     data = comm.recv(source=0)
#     calced = pruefung.countIslands(data)
#     if rank % 2 == 0:
#         recv = comm.recv(source=rank+1)
#         calced.mergeRow(recv)
#         comm.send(calced, 0)
#     else:
#         comm.send(calced, rank-1)