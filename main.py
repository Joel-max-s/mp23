from mpi4py import MPI
import math
import matrix as mx
import generator
import argparse

save_file = False
comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nprocs = comm.Get_size()

ROWS = 10
COLUMNS = 10
PRINT_MATRIX = False

def run() -> mx.Row:
    """calculate the number of islands

    Returns:
        mx.Row: the final "ROW", there are all rows in it
    """

    # generate a random matrix of the given size
    matrix: mx.Matrix
    if my_rank == 0:
        l = generator.generate(ROWS, COLUMNS)
        matrix = mx.list_to_matrix(l)
        if PRINT_MATRIX:
            print(matrix)

    # split the matrix and send them to their receivers
    # this is done in a binary-tree
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

    r = mx.count_islands(matrix)

    # send the calculated results to their receivers
    # merge the results
    # this is also done in a binary tree
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

    return r
    

if my_rank == 0:
    parser = argparse.ArgumentParser(prog="Pruefungsprojekt mp23", exit_on_error=False, add_help=False)
    parser.add_argument('rows', type=int)
    parser.add_argument('columns', type=int)
    parser.add_argument('--print-matrix', dest='print_matrix', action='store_true')
    parser.set_defaults(print_matrix=False)
    try:
        args = parser.parse_args()
        ROWS = int(args.rows)
        COLUMNS = int(args.columns)
        PRINT_MATRIX = args.print_matrix

    except:
        print('You need to specify the number of rows and columns')
        print('Example: mpirun --use-hwthread-cpus -np 8 python3 main.py 100 100')
        comm.Abort(1)

result = run()

if my_rank == 0:
    result.print_info()