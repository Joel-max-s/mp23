from mpi4py import MPI
import generator
import pruefung
import time
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()



# l = [[0,1,0,0,0,0,0,0],
#      [0,1,0,0,0,1,0,0],
#      [0,0,1,0,1,0,0,0],
#      [0,0,0,1,0,0,0,0]]

# matrix = generator.generate_with_isles(1000, 1000, 100)

print(math.log2(8))
start = time.time()
if rank == 0:
    l = generator.generate(1000, 1000)
    matrix = pruefung.list_to_matrix(l)
    m = pruefung.splitMatrix(matrix, nprocs)

    if nprocs >= 2:
        for i in range(1, nprocs):
            comm.send(m[i], i)
        calced = pruefung.countIslands(m[0])
        recv : pruefung.Row = comm.recv(source=rank+1)
        calced.mergeRow(recv)
        recv = comm.recv(source=2)
        calced.mergeRow(recv)
        end = time.time()
        print(f'Parallel: {end-start}')

    start = time.time()
    seq = pruefung.countIslands(matrix)
    end = time.time()
    print(f'Sequenziell: {end-start}')
    print(len(calced.islands))
    print(len(seq.islands))
    
else:
    data = comm.recv(source=0)
    calced = pruefung.countIslands(data)
    if rank % 2 == 0:
        recv = comm.recv(source=rank+1)
        calced.mergeRow(recv)
        comm.send(calced, 0)
    else:
        comm.send(calced, rank-1)