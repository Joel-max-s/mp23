import math

example_list : list[list[bool]] = [
    [0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
    [0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1],
    [1,1,0,0,0,1,0,1,1,1,1,0,0,0,0,0,1,1,1],
    [0,1,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0],
    [1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
]

class Matrix:
    start_row: int
    elems: list[list[bool]]

    def __init__(self, e: list[list[bool]], s: int) -> None:
        self.elems = e
        self.start_row = s

class Island:
    elems: set[tuple[int, int]]

    def __str__(self) -> str:
        return str(self.elems)

    def __init__(self, e: set[tuple[int, int]]) -> None:
        self.elems = e

    def merge(self, other: 'Island'):
        self.elems.update(other.elems)

    def collide(self, other: 'Island') -> bool:
        if self.elems.intersection(other.elems):
            return True
        return False
    
class Row:
    islands: set[Island]

    def __str__(self) -> str:
        s = ""
        for i in self.islands:
            s += f"{i}\n"
        return s

    def __init__(self, i: set[Island]) -> None:
        self.islands = i

    def merge(self, other: 'Row'):
        to_delete: set[Island] = set()

        for o in other.islands:
            for s in self.islands:
                if s.collide(o):
                    s.merge(o)
                    to_delete.add(o)

        other.islands.difference_update(to_delete)

        to_delete: set[Island] = set()

        for s1 in self.islands:
            for s2 in self.islands:
                if s1 == s2:
                    continue
                if s1 in to_delete:
                    continue
                if s1.collide(s2):
                    s1.merge(s2)
                    to_delete.add(s2)

        self.islands.difference_update(to_delete)
        
        self.islands.update(other.islands)

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
                arr[val-1].append((i+matrix.start_row,j))
            
    islands: list[Island] = []
    for i, e in enumerate(arr):
        islands.append(Island(set(e)))

    return Row(set(islands))

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
            if is_safe(matrix, visited, s[0]+rowNeighours[k], s[1]+colNeighours[k]):
                stack.append((s[0]+rowNeighours[k], s[1]+colNeighours[k]))


def is_safe(matrix: list[list[bool]], visited: list[list[int]], i: int, j: int) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])
    return (i >= 0 and i < rows and j >= 0 and j < cols and visited[i][j] == 0 and matrix[i][j])

def split_matrix(matrix: Matrix, splits: int):
    rows = len(matrix.elems)
    avg_size = math.ceil(rows / splits)
    splitted : list[Matrix] = [] 
    for i in range(splits):
        temp = []
        for j in range(avg_size + 1):
            row = i * avg_size + j
            if row < rows:
                temp.append(matrix.elems[row])
        splitted.append(Matrix(temp, matrix.start_row+i*avg_size))
    return splitted

def list_to_matrix(l: list[list[bool]]) -> Matrix:
    return Matrix(l,0)

if __name__ == "__main__":
    m = list_to_matrix(example_list)
    row = countIslands(m)
    print(len(row.islands))