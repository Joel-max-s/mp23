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
    """The input.
    """
    start_row: int
    elems: list[list[bool]]

    def __init__(self, e: list[list[bool]], s: int) -> None:
        """Initialize the Matrix

        Args:
            e (list[list[bool]]): The matrix as 2d list of bools
            s (int): The global start row, if the matrix was already splitted, else it should be 0
        """
        self.elems = e
        self.start_row = s

    def __str__(self) -> str:
        s = "[\n"
        for e in self.elems:
            s += f"\t{e}\n"
        s += "]\n"
        return s

class Island:
    """An island is a set off points in the matrix that are neighbours.
    """
    elems: set[tuple[int, int]]
    min_row: int
    is_min_island: bool

    def __str__(self) -> str:
        return str(self.elems)

    def __init__(self, e: set[tuple[int, int]], min_r: int) -> None:
        """Initialize the Island

        Args:
            e (set[tuple[int, int]]): the elements of the island
            min_r (_type_): the smallest row in the global Matrix that is present in this Island
        """
        self.elems = e
        self.min_row = min_r
        self.is_min_island = any(a[0] == self.min_row for a in self.elems)

    def merge(self, other: 'Island'):
        """Add the elems of an other Island to the own island

        Args:
            other (Island): the other Island
        """
        self.elems.update(other.elems)

    def collide(self, other: 'Island') -> bool:
        """Checks if the island collides with the other Island

        Args:
            other (Island): the other Island

        Returns:
            bool: If True the Island collide, else not
        """
        if self.elems.intersection(other.elems):
            return True
        return False
    
    def print_info(self):
        print(f"size: {len(self.elems): <10} one Member: {next(iter(self.elems))}")
    
class Row:
    """Contains rows from the global Matrix
    """
    min_row: int
    islands: set[Island]
    min_islands: set[Island]

    def __str__(self) -> str:
        s = "islands:\n"
        for i in self.islands:
            s += f"\t{i}\n"
        s += "min_islands:\n"
        for i in self.min_islands:
            s += f"\t{i}\n"
        s += f"min_row: {self.min_row}"
        return s

    def __init__(self, i: set[Island], min_r: int) -> None:
        """Initialize the Row

        Args:
            i (set[Island]): the islands that are present in the row
            min_r (int): the smallest row in the global Matrix that is present in this Row
        """
        self.islands = i
        self.min_row = min_r
        self.compute_min_islands()

    def compute_min_islands(self):
        """compute all min Islands

        Min islands are Islands that have an elemt in the min row.
        If an island is an min_island it could be merged with an other island from an other row.
        """
        self.min_islands = set(filter(lambda a: any(b[0] == self.min_row for b in a.elems), self.islands))
        

    def merge(self, other: 'Row'):
        """Add the elements of an other row to this row.

        Args:
            other (Row): the other Row
        """
        merge_row = other.min_row

        # the own islands that are contestants for merging
        own_merge_contestants = set(filter(lambda a: any(b[0] == merge_row for b in a.elems), self.islands))
        self.islands.difference_update(own_merge_contestants)

        to_delete: set[Island] = set()

        # merge colliding islands
        for o in other.min_islands:
            for s in own_merge_contestants:
                if s.collide(o):
                    s.merge(o)
                    to_delete.add(o)

        other.islands.difference_update(to_delete)

        to_delete: set[Island] = set()

        # check if through merging with the other row, the changed merged rows now collide
        # if yes merge them
        for s1 in own_merge_contestants:
            for s2 in own_merge_contestants:
                if s1 == s2:
                    continue
                if s1 in to_delete:
                    continue
                if s1.collide(s2):
                    s1.merge(s2)
                    to_delete.add(s2)

        own_merge_contestants.difference_update(to_delete)
        
        self.islands.update(other.islands, own_merge_contestants)
        self.compute_min_islands()

    def print_info(self) -> None:
        print(f'There are {len(self.islands)} different Islands')
        print('Here are the Stats of the Islands:')
        for i in self.islands:
            i.print_info()

def count_islands(matrix: Matrix) -> Row:
    """Count how many Islands there are in the given Matrix

    Get the islands through a depht-first-search

    Args:
        matrix (Matrix): the matrix

    Returns:
        Row: contains all islands and some extra info
    """
    rows = len(matrix.elems)
    cols = len(matrix.elems[0])

    visited: list[list[int]] = [x[:] for x in [[0] * cols] * rows]

    # search all Islands
    count: int = 0
    for i in range(rows):
        for j in range(cols):
            if matrix.elems[i][j] and visited[i][j] == 0:
                idephtSearch(matrix.elems, visited, i, j, count+1)
                count += 1

    # generate list with coordinates of islands instead of global view
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
        islands.append(Island(set(e), matrix.start_row))

    return Row(set(islands), matrix.start_row)

def idephtSearch(matrix: list[list[bool]], visited: list[list[int]], i: int, j: int, count: int):
    """An iterative depht-first-search algorithm

    Seach all neighbours if there is also an island-part.

    Args:
        matrix (list[list[bool]]): 2d list of marked island-parts
        visited (list[list[int]]): already visited island-parts
        i (int): start Row
        j (int): start Column
        count (int): this is the 'count' Island
    """
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
    """Check if square is safe to visit

    Args:
        matrix (list[list[bool]]): 2d list of marked island-parts
        visited (list[list[int]]): already visited island-parts
        i (int): Row
        j (int): Column

    Returns:
        bool: True if it is safe to visit
    """
    rows = len(matrix)
    cols = len(matrix[0])
    return (i >= 0 and i < rows and j >= 0 and j < cols and visited[i][j] == 0 and matrix[i][j])

def split_matrix(matrix: Matrix, splits: int) -> list[Matrix]:
    """Split a big matrix into smaller matrices

    Args:
        matrix (Matrix): the big matrix to split
        splits (int): split into 'splits' partts

    Returns:
        list[Matrix]: splitted matrices
    """
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
    """convert a 2d list of bools to a Matrix

    Args:
        l (list[list[bool]]): 2d list of bools

    Returns:
        Matrix: the converted matrix
    """
    return Matrix(l,0)

if __name__ == "__main__":
    m = list_to_matrix(example_list)
    print(m)
    row = count_islands(m)
    row.print_info()