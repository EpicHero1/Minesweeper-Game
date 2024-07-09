import pygame
from random import randint
from classes import *
from variables import *

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont('consolas', textSize)

clock = pygame.time.Clock()

#Make a grid
grid = []
for i in range(gridWidth * gridHeight):
    tile = Tile((tileSize + frameSize) * int(i % gridWidth), int(i / gridWidth) * (tileSize + frameSize))
    if i % gridWidth == 0:
        grid.append([])
    grid[len(grid) - 1].append(tile)

#Put mines
for i in range(bombCount):
    index = (randint(0, gridWidth - 1), randint(0, gridHeight - 1))
    grid[index[1]][index[0]].bomb = True

pause = False
win = True
first = True

#Main Loop
while True:
    screen.fill(backgroundColor)

    win = True
    for row in grid:
        for tile in row:
            tile.main(screen)
            if tile.color == backgroundColor and tile.adjacent != 0:
                #Display the number of adjacent mines
                textScreen = font.render(str(tile.adjacent), True, colors[tile.adjacent - 1], backgroundColor)
                textRect = textScreen.get_rect()
                textRect.topleft = (tile.rect.x + 8, tile.rect.y)
                screen.blit(textScreen, textRect)
            if tile.bomb == False and tile.color != backgroundColor:
                win = False
            if tile.color == bombColor:
                pause = True
            if pause == True and tile.bomb == True:
                if win == True:
                    tile.color = winColor
                else:
                    tile.color = bombColor
    
    if win == True:
        pause = True 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pause == False:
            i = -1
            j = -1
            for row in grid:
                i += 1
                for tile in row:
                    j += 1
                    if tile.rect.collidepoint(event.pos):
                        if first == True and event.button == 1:
                            firstClick(grid, j % gridWidth, i)
                            first = False
                            #Check adjacent tiles for mines (after the first click)
                            for y in range(gridHeight):
                                for x in range(gridWidth):
                                    grid[y][x].adjacent = adjacent(grid, x, y)
                        if tile.color == tileColor and event.button == 1 and tile.bomb == False:
                            openTiles(grid, j % gridWidth, i)
                        tile.update(event)

    clock.tick(60)
    pygame.display.update()