import pygame
import numpy as np
import sys
import os
import time
import joblib
import tensorflow as tf
from datetime import datetime
import subprocess
import platform
#colors
one = (255, 255, 255)
pfive = (50,50,50)
two = (0, 0, 0)
grey = (220,220,220)
grey2 = (200,200,200)

text =""

labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
model = joblib.load("model.pkl")

pygame.init()

size = (800, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Handwriting Keyboard AI")

smallfont = pygame.font.SysFont("Geneva", 35) 
width = 20
height = 20
margin = 0
w,h = 800,800
grid = [[0 for x in range(28)] for y in range(28)]

done = False
clock = pygame.time.Clock()
neighbour=[]

lastclick = 0 
startstop = False
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Exit")
                pygame.quit()
            if event.key == pygame.K_SPACE:
                text = text + " "
        
            if event.key == pygame.K_BACKSPACE:
                print("backspace",text[:-1])
                if text!="":
                    text = text[:-1]
            if event.key == pygame.K_r:
                grid = [[0 for x in range(28)] for y in range(28)]

        if pygame.mouse.get_pressed()[0]:
            if 300 <= pos[0] <= w/2+140 and h/2+330 <= pos[1] <= h/2+390: 
                if platform.system() == 'Windows':
                    cmd='echo '+text.strip()+'|clip'
                    subprocess.check_call(cmd, shell=True)
                else:
                    cmd='echo '+text.strip()+'|pbcopy'
                    subprocess.check_call(cmd, shell=True)
                text = ""
                
            column = pos[0] // (width + margin)- 6 if pos[0] // (width + margin)- 6 >0 else 0
            row = pos[1] // (height + margin) - 8 if pos[1] // (width + margin)- 8 >0 else 0
            try:
                if grid[row+1][column] != 1:
                    grid[row+1][column] = 0.5
                if grid[row-1][column] != 1:
                    grid[row-1][column] = 0.5
                if grid[row][column+1] != 1:
                    grid[row][column+1] = 0.5
                if grid[row][column-1] != 1:
                    grid[row][column-1] = 0.5
                grid[row][column] = 1
            except:
                try:
                    grid[row][column] = 1
                except:
                    d = 4
                d = 4
            lastclick = datetime.now()
            startstop = True
    if startstop:
        temp = datetime.now()
        if (temp-lastclick).total_seconds() >0.5:
            try:
                    classes = model.predict(np.array([grid]).T.reshape(1,28,28))
                    temp = np.round(classes)
                    pred = labels[int(list(np.where(temp==1))[1])]
                    print(pred)
                    # print(labels[int(list(np.where(temp==1))[1])])
                    if text != "":
                        if text[len(text)-1].isnumeric()== False and pred == "0":
                            pred = "o"
                        if pred.isnumeric() == False:
                            pred = pred.lower()
                    else:
                        if pred.isnumeric()== False:
                            pred = pred.upper()
                    print(pred) 
                    text = text + str(pred)
            except:
                print("Failed to recognise")
            grid = [[0 for x in range(28)] for y in range(28)]
            startstop = False
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    screen.fill(grey)
    pygame.draw.rect(screen, one, pygame.Rect(50, 30, 700, 100),  50, 4)
    if text != "":
        textbox = smallfont.render(text , True , two) 
    else:
        textbox = smallfont.render("Start Drawing Letters To Type" , True , grey) 
        
    screen.blit(textbox , (70,60)) 
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == 1:
                color = two
            elif grid[row][column] == 0.5:
                color = pfive
            else:
                color = one
            pygame.draw.rect(screen, color, [120+margin + (margin + width) * column, 160+margin + (margin + height) * row, width, height],60, 5)
    
    cp = smallfont.render('Copy Text' , True , two) 
    
    if 300 <= pos[0] <= w/2+140 and h/2+330 <= pos[1] <= h/2+390: 
        pygame.draw.rect(screen,one,[w/2-140,h/2+330,300,60]) 
          
    else: 
        pygame.draw.rect(screen,grey2,[w/2-140,h/2+330,300,60]) 
    screen.blit(cp , (w/2-85,h/2+335)) 
    pygame.display.flip()
    clock.tick(150)
pygame.quit()

