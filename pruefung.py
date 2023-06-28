from mpi4py import MPI
import generator
import math
import numpy as np

matrix : list[list[bool]] = [
    [0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
    [0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1],
    [1,1,0,0,0,1,0,1,1,1,1,0,0,0,0,0,1,1,1],
    [0,1,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0],
    [1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    # [0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
]

class Matrix:
    min_row: int
    max_row: int
    elems: list[list[bool]]

    def __init__(self, min_r: int, max_r: int, e: list[list[bool]]) -> None:
        self.min_row = min_r
        self.max_row = max_r
        self.elems = e


class Island:
    min_row: int
    max_row: int
    index: int
    members: list[tuple[int, int]]
    lower_bound_members: list[tuple[int, int]]
    upper_bound_members: list[tuple[int, int]]
    is_upper_bound_island: bool
    is_lower_bound_island: bool

    def __str__(self) -> str:
        return f"Members: {self.members}"

    def __init__(self, i: int, min_r: int, max_r: int, m: list[tuple[int, int]]) -> None:
        self.index = i
        self.members = m
        self.min_row = min_r
        self.max_row = max_r
        self.calculate_corner_members()

    def calculate_corner_members(self) -> None:
        self.is_lower_bound_island = False
        self.is_upper_bound_island = False
        self.upper_bound_members = list(filter(lambda a: a[0] == self.max_row, self.members))
        if(len(self.upper_bound_members)):
            self.is_upper_bound_island = True
        self.lower_bound_members = list(filter(lambda a: a[0] == self.min_row, self.members))
        if(len(self.lower_bound_members)):
            self.is_lower_bound_island = True

    def merge_Island(self, i: 'Island'):
        for m in i.members:
            if m not in self.members:
                self.members.append(m)
        self.calculate_corner_members()

    def islands_collide(self, isle: 'Island') -> bool:
        for ubm in self.upper_bound_members:
            if list(filter(lambda a: a[1] == ubm[1], isle.lower_bound_members)):
                return True
        return False
    
    def islands_up_collide(self, isle: 'Island') -> bool:
        for ubm in self.upper_bound_members:
            if list(filter(lambda a: a[1] == ubm[1], isle.upper_bound_members)):
                return True
        return False
    
class Row:
    min_row: int
    max_row: int
    islands: list[Island]
    upper_bound_islands: list[Island]
    lower_bound_islands: list[Island]

    def __str__(self) -> str:
        a = ""
        for i in self.islands:
            a += str(i) + "\n"
        return a

    def __init__(self, min_r: int, max_r: int, i: list[Island]) -> None:
        self.min_row = min_r
        self.max_row = max_r
        self.islands = i
        self.calculate_corner_islands()

    def calculate_corner_islands(self):
        self.upper_bound_islands = list(filter(lambda a: a.is_upper_bound_island, self.islands))
        self.lower_bound_islands = list(filter(lambda a: a.is_lower_bound_island, self.islands))

    def update_bounds(self):
        for i in self.islands:
            i.max_row = self.max_row

    def mergeRow(self, r: 'Row'):
        for ubi in self.upper_bound_islands:
            for lbi in r.lower_bound_islands:
                if ubi.islands_collide(lbi):
                    ubi.merge_Island(lbi)
                    if lbi in r.islands:
                        r.islands.remove(lbi)

        for ubi1 in self.upper_bound_islands:
            for ubi2 in self.upper_bound_islands:
                if ubi1 == ubi2:
                    continue
                if ubi1.islands_up_collide(ubi2):
                    ubi1.merge_Island(ubi2)
                    self.upper_bound_islands.remove(ubi2)
                    self.islands.remove(ubi2)
                        
        self.islands.extend(list(set(r.islands)))
        self.max_row = r.max_row
        self.update_bounds()
        self.calculate_corner_islands()     

def countIslands(matrix: Matrix) -> Row:
    rows = len(matrix.elems)
    cols = len(matrix.elems[0])

    visited: list[list[int]] = [x[:] for x in [[0] * cols] * rows]

    count: int = 0
    for i in range(rows):
        for j in range(cols):
            if matrix.elems[i][j] and visited[i][j] == 0:
                idephtSearch(matrix.elems, visited, i, j, count+1)
                count += 1

    arr: list[list[tuple[int, int]]] = []
    for i in range(count):
        arr.append([])
    for i in range(len(visited)):
        for j in range(len(visited[i])):
            val = visited[i][j]
            if val > 0:
                arr[val-1].append((i+matrix.min_row,j))
            
    islands: list[Island] = []
    for i, e in enumerate(arr):
        islands.append(Island(i+1, matrix.min_row, rows-1+matrix.min_row, e))

    return Row(matrix.min_row, matrix.max_row, islands)

def idephtSearch(matrix: list[list[bool]], visited: list[list[int]], i: int, j: int, count: int):
    rowNeighours = [-1, -1, -1, 0, 0, 1, 1, 1]
    colNeighours = [-1, 0, 1, -1, 1, -1, 0, 1]

    if matrix[i][j]:
        visited[i][j] = count
    else:
        visited[i][j] = -1

    stack : list[tuple[int, int]] = []
    stack.append((i,j))

    while(len(stack)):
        s = stack.pop()

        if matrix[s[0]][s[1]]:
            visited[s[0]][s[1]] = count

        for k in range(len(rowNeighours)):
            if isSafe(matrix, visited, s[0]+rowNeighours[k], s[1]+colNeighours[k]):
                stack.append((s[0]+rowNeighours[k], s[1]+colNeighours[k]))


def isSafe(matrix: list[list[bool]], visited: list[list[int]], i: int, j: int) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])
    return (i >= 0 and i < rows and j >= 0 and j < cols and visited[i][j] == 0 and matrix[i][j])

def splitMatrix(matrix: Matrix, parts: int) -> list[Matrix]:
    len_matrix = len(matrix.elems)
    avg_size = math.ceil(len_matrix / parts)
    splitted : list[Matrix] = [] 
    for i in range(parts):
        temp = []
        for j in range(avg_size + 1):
            row = i * avg_size + j
            if row < len_matrix:
                temp.append(matrix.elems[row])
        splitted.append(Matrix(i*avg_size, min(i*avg_size + avg_size, len_matrix), temp))
    return splitted

def halfMatrix(matrix: Matrix) -> list[Matrix]:
    return splitMatrix(matrix, 2)

def list_to_matrix(l: list[list[bool]]) -> Matrix:
    return Matrix(0, len(l) - 1, l)

if __name__ == "__main__":
    # matrix = generator.generate(100, 100)
    isles = countIslands(matrix)
    print(isles)
    # m = halfMatrix(matrix)
    # print(m[0][-1] == m[1][0])