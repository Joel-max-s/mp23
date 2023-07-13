import math
import random

def generate(rows: int, cols: int) -> list[list[bool]]:
    """Generates a random matrix with given sizes

    The number of 'Islands' is derived from the number of cells in the matrix.
    It is random, but there are maximum of sqrt(rows*cols) number of islands.
    The size of the islands are also random, the length of them is between 1 and sqrt(rows*cols)

    Args:
        rows (int): Number of rows of the matrix
        cols (int): Number of columns of the matrix
        seed (int): Seed for the random number generator, optional

    Returns:
        list[list[bool]]: 2d matrix of bools, the 'Island-parts' are True
    """
    matrix: list[list[bool]] = [x[:] for x in [[0] * cols] * rows]
    number_of_isles = random.randint(1, int(math.sqrt(rows*cols)))

    for i in range(number_of_isles):
        island_length = random.randint(1, int(math.sqrt(rows*cols)))
        point = (random.randint(0, rows-1), random.randint(0, cols-1))
        matrix[point[0]][point[1]] = 1
        for j in range(island_length):
            point = getNextPoint(rows, cols, point)
            matrix[point[0]][point[1]] = 1

    return matrix            

def getNextPoint(rows: int, cols: int, currentPoint: tuple[int, int]) -> tuple[int, int]:
    """Generates the next island-part

    Random walk from the current point to a random neighbour.

    Args:
        rows (int): Number of rows of the matrix
        cols (int): Number of columns of the matrix
        currentPoint (tuple[int, int]): The point from where to walk

    Returns:
        tuple[int, int]: The new island-part
    """
    rowNeighours = [-1, -1, -1, 0, 0, 1, 1, 1]
    colNeighours = [-1, 0, 1, -1, 1, -1, 0, 1]
    nextPoint = (-1, -1)

    while not (nextPoint[0] >= 0 and nextPoint[0] < rows and nextPoint[1] >= 0 and nextPoint[1] < cols):
        direction = random.randint(0, 7)
        nextPoint = (currentPoint[0] + rowNeighours[direction], currentPoint[1] + colNeighours[direction])

    return nextPoint

if __name__ == "__main__":
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in generate(10, 10)]))