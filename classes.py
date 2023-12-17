import pygame
from variables import *

class Tile:
    def __init__(self, x, y) -> None:
        self.color = tileColor
        self.bomb = False
        self.flag = False
        self.adjacent = 0
        self.rect = pygame.Rect(x, y, tileSize, tileSize)
    def __str__(self) -> str:
        return f"Tile({self.rect.x},{self.rect.x})"
    def main(self, display):
        pygame.draw.rect(display, self.color, self.rect)

    def update(self, event):
        if event.button == 1 and self.flag == False:
            if self.bomb == True:
                self.color = bombColor
            else:
                self.color = backgroundColor
        elif event.button == 3 and (self.color == tileColor or self.color == flagColor):
            if self.flag == True:
                self.flag = False
                self.color = tileColor
            else:
                self.flag = True
                self.color = flagColor

def adjacent(matrix, x, y):
    count = 0
    width = len(matrix[0]) - 1
    height = len(matrix) - 1
    for i in range(-1 if x > 0 else 0, 2 if x < width else 1):
        for j in range(-1 if y > 0 else 0, 2 if y < height else 1):
            if matrix[y + j][x + i].bomb == True and (i != 0 or j != 0):
                count += 1
    return count

def openTiles(matrix, x, y):
    width = len(matrix[0]) - 1
    height = len(matrix) - 1
    #Look into adjacent tiles and check bombs recursively
    for i in range(-1 if x > 0 else 0, 2 if x < width else 1):
        for j in range(-1 if y > 0 else 0, 2 if y < height else 1):
            if matrix[y + j][x + i].color != backgroundColor:
                if matrix[y + j][x + i].bomb == False:
                    matrix[y + j][x + i].color = backgroundColor
                    if matrix[y + j][x + i].adjacent == 0:
                        openTiles(matrix, x + i, y + j)

def firstClick(matrix, x, y):
    matrix[y][x].bomb = False