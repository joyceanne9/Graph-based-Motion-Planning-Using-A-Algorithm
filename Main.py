import pygame
from Node import Node
import math
import time

print("==========INPUT HERE==========")
while True:
    choice = input("Do you want to enter custom grid size? Yes/No? ::  ").upper()
    if choice == "YES" or choice == "Y":
        x = int(input("Enter custom grid size(square) :: "))
        break
    elif choice == "NO" or choice == "N":
        #custom size is 10x10
        x = 10
        break
    else:
        print("OOPS! TRY AGAIN!!!")
print("\n==========INSTRUCTIONS==========\n"
      "Left click your desired square(node) to set a starting position, ; click again if you want to remove it\n"
      "Right click your desired square(node) to set a goal position; click again if you want to remove it \n"
      "Press control key while left clicking the square(node) to set obstacle\n"
      "Press r key to reset grid\n"
      "Press 4 key to find path using taxicab geometry distance (4 directions)\n"
      "Press 8 key to find path using Euclidian distance (8 directions)\n")
WIDTH, HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAPH-BASED PATH PLANNING USING A* ALGORITHM")
FPS = 60
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

rows, cols = x,x
sleepTime = 0.01
squareHeight = HEIGHT / rows
squareWidth = WIDTH / cols

openSet = []
closedSet = []
startNode = None
endNode = None
path = []


def create2DArray():
    squares = []
    for i in range(rows):
        row = []
        for j in range(cols):
            col = Node(WINDOW, i, j, squareHeight)
            row.append(col)
        squares.append(row)
    return squares


squares = create2DArray()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                checkKeyDown(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClick(event)
        draw_all()
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] and keys[pygame.K_LCTRL]:
            drawWalls()

    pygame.quit()


def AStar(neigh):
    global startNode, endNode, openSet, closedSet, path
    if (startNode == None or endNode == None):
        return
    openSet.append(startNode)
    while openSet != []:
        time.sleep(sleepTime)
        draw_all()
        lowestFCostIndex = 0
        for i, x in enumerate(openSet):
            if x.f < openSet[lowestFCostIndex].f:
                lowestFCostIndex = i

        current = openSet[lowestFCostIndex]

        if current == endNode:
            temp = current
            if temp.state != 1:
                temp.state = 5
            path.append(temp)
            while temp.previous:
                draw_all()
                time.sleep(sleepTime)
                if temp.previous.state != 1:
                    temp.previous.state = 5
                path.append(temp.previous)
                temp = temp.previous
            return

        openSet.remove(current)
        closedSet.append(current)
        if current.state != 1:
            current.state = 4
        if neigh == 4:
            currentNeighbours = checkNeighbours4(current.x, current.y)
        elif neigh == 8:
            currentNeighbours = checkNeighbours8(current.x, current.y)
        for neighbour in currentNeighbours:
            if neighbour in closedSet:
                continue

            if current.x != neighbour.x and current.y != neighbour.y:
                tentGScore = current.g + math.sqrt(2)
            else:
                tentGScore = current.g + 1
            if neighbour not in openSet:
                openSet.append(neighbour)
                if neighbour.state != 1:
                    neighbour.state = 0
            elif tentGScore >= neighbour.g:
                continue

            neighbour.previous = current
            neighbour.g = tentGScore
            neighbour.h = generateHeuristic(neighbour, endNode)
            neighbour.f = neighbour.g + neighbour.h


def generateHeuristic(neighbour, end):
    neighborPos = pygame.math.Vector2(neighbour.x, neighbour.y)
    endPos = pygame.math.Vector2(end.x, end.y)
    dist = neighborPos.distance_to(endPos)
    return dist


def draw_all():
    draw_window()
    draw_board()
    update_display()


def draw_board():
    for x in range(rows):
        for y in range(cols):
            squares[x][y].draw()


def drawWalls():
    global squares
    mouse_pos = pygame.mouse.get_pos()
    xIndex = math.floor((mouse_pos[0] / squareHeight))
    yIndex = math.floor((mouse_pos[1] / squareWidth))
    if squares[xIndex][yIndex].state == -1:
        squares[xIndex][yIndex].state = 3


def checkMouseClick(event):
    global startNode, endNode, squares
    mouse_pos = pygame.mouse.get_pos()
    xIndex = math.floor((mouse_pos[0] / squareHeight))
    yIndex = math.floor((mouse_pos[1] / squareWidth))
    if event.button == 1:  # left click
        if startNode == None:
            if squares[xIndex][yIndex].state == -1:
                squares[xIndex][yIndex].state = 1
                startNode = squares[xIndex][yIndex]
        else:
            if squares[xIndex][yIndex].state == 1:
                squares[xIndex][yIndex].state = -1
                startNode = None
    elif event.button == 2:  # middle click
        if squares[xIndex][yIndex].state == 3:
            squares[xIndex][yIndex].state = -1
        elif squares[xIndex][yIndex].state == -1:
            squares[xIndex][yIndex].state = 3
    elif event.button == 3:  # right click
        if endNode == None:
            if squares[xIndex][yIndex].state == -1:
                squares[xIndex][yIndex].state = 1
                endNode = squares[xIndex][yIndex]
        else:
            if squares[xIndex][yIndex].state == 1:
                squares[xIndex][yIndex].state = -1
                endNode = None


def checkKeyDown(event):
    global startNode, endNode, path, squares, openSet, closedSet
    if event.key == pygame.K_r:
        openSet = []
        closedSet = []
        for x in range(rows):
            for y in range(cols):
                squares[x][y].state = -1
                squares[x][y].f = 0
                squares[x][y].g = 0
                squares[x][y].h = 0
                squares[x][y].previous = None
        startNode = None
        endNode = None
        path = []
    if event.key == pygame.K_4:
        AStar(4)
    elif event.key == pygame.K_8:
        AStar(8)


# Checks 8 neighbours around
def checkNeighbours8(x, y):
    neighbourCount = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = x + i
            row = y + j
            if (col > -1 and col < cols) and (row > -1 and row < rows):  # and (col != x and row != y):
                if squares[col][row].state != 3:
                    neighbourCount.append(squares[col][row])
    return neighbourCount


# Checks 4 neighbours around
def checkNeighbours4(x, y):
    global squares
    neighbours = []
    if x < cols - 1 and squares[x + 1][y].state != 3:
        neighbours.append(squares[x + 1][y])
    if x > 0 and squares[x - 1][y].state != 3:
        neighbours.append(squares[x - 1][y])
    if y < rows - 1 and squares[x][y + 1].state != 3:
        neighbours.append(squares[x][y + 1])
    if y > 0 and squares[x][y - 1].state != 3:
        neighbours.append(squares[x][y - 1])
    return neighbours


def draw_window():
    WINDOW.fill(WHITE)


def update_display():
    pygame.display.update()


if __name__ == "__main__":
    main()
