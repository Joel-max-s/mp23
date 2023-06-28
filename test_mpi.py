from mpi4py import MPI
import generator
import pruefung
import time
import matrix as mx
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()



# l = [[0,1,0,0,0,0,0,0],
#      [0,1,0,0,0,1,0,0],
#      [0,0,1,0,1,0,0,0],
#      [0,0,0,1,0,0,0,0]]

# matrix = generator.generate_with_isles(1000, 1000, 100)

start = time.time()
if rank == 0:
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
    if rank in [1,4]:
        data = comm.recv()
        d = mx.split_matrix(data, 2)
        comm.send(d[0], rank+1, tag=rank)
        comm.send(d[1], rank+2, tag=rank)
        m1 = comm.recv(source=rank+1)
        m2 = comm.recv(source=rank+2)
        m1.merge(m2)
        comm.send(m1, 0)
    else:
        d: mx.Matrix = comm.recv()
        r = mx.countIslands(d)
        if rank in [2,5]:
            comm.send(r, rank-1)
        elif rank in [3,6]:
            comm.send(r, rank-2)

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