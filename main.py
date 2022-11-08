import pygame
import numpy as np
import sys
import os
import time

#colors
one = (255, 255, 255)
two = (0, 0, 0)
grey = (220,220,220)

text ="hello i"

pygame.init()

size = (800, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Handwriting Keyboard AI")

smallfont = pygame.font.SysFont("Helvetica", 35) 
width = 20
height = 20
margin = 0

grid = [[0 for x in range(28)] for y in range(28)]

done = False
clock = pygame.time.Clock()
neighbour=[]

while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                    print("Exit")
                    pygame.quit()
             if event.key == pygame.K_BACKSPACE:
                    print("backspace",text[:-1])
                    if text!="":
                        text = text[:-1]
             if event.key == pygame.K_r:
                grid = [[0 for x in range(28)] for y in range(28)]

        if pygame.mouse.get_pressed()[0]:
            column = pos[0] // (width + margin)- 6 if pos[0] // (width + margin)- 6 >0 else 0
            row = pos[1] // (height + margin) - 8 if pos[1] // (width + margin)- 8 >0 else 0
            try:
                grid[row][column] = 1
            except:
                d = 4
        
    
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    screen.fill(grey)
    pygame.draw.rect(screen, one, pygame.Rect(50, 30, 700, 100),  50, 4)
    textbox = smallfont.render(text , True , two) 
    screen.blit(textbox , (70,65)) 
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == 1:
                color = two
            else:
                color = one
            pygame.draw.rect(screen, color, [120+margin + (margin + width) * column, 160+margin + (margin + height) * row, width, height],60, 5)
    pygame.display.flip()
    clock.tick(120)
pygame.quit()
