import math
import random

def generate(rows: int, cols: int) -> list[list[bool]]:
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

def generate_with_isles(rows: int, cols: int, number_of_isles) -> list[list[bool]]:
    matrix: list[list[bool]] = [x[:] for x in [[0] * cols] * rows]

    for i in range(number_of_isles):
        island_length = random.randint(1, int(math.sqrt(rows*cols)))
        point = (random.randint(0, rows-1), random.randint(0, cols-1))
        matrix[point[0]][point[1]] = 1
        for j in range(island_length):
            point = getNextPoint(rows, cols, point)
            matrix[point[0]][point[1]] = 1

    return matrix
            

def getNextPoint(rows, cols, currentPoint) -> tuple[int, int]:
    rowNeighours = [-1, -1, -1, 0, 0, 1, 1, 1]
    colNeighours = [-1, 0, 1, -1, 1, -1, 0, 1]
    nextPoint = (-1, -1)

    while not (nextPoint[0] >= 0 and nextPoint[0] < rows and nextPoint[1] >= 0 and nextPoint[1] < cols):
        direction = random.randint(0, 7)
        nextPoint = (currentPoint[0] + rowNeighours[direction], currentPoint[1] + colNeighours[direction])

    return nextPoint

if __name__ == "__main__":
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in generate(10, 10)]))