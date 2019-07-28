# Import a library of functions called 'pygame'
import pygame
import socket
import time
from pygame.locals import *
HOST = '192.168.43.214'
PORT = 8090
cmd = '0'

def send():
    global HOST, cmd

    #for i in range(3):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    sent = client_socket.send(cmd.encode('utf-8'))
        #time.sleep(0.001)
        
##def control():
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
 
# Set the height and width of the screen
size   = [400, 300]
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("consolas", 20)
 
pygame.display.set_caption("Keyboard Controller")
  
#Loop until the user clicks the close button.
done  = False
flag  = None
clock = pygame.time.Clock()

    
 
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
     
    # Main Event Loop
    for event in pygame.event.get(): # User did something

    

        if event.type == pygame.KEYDOWN: # If user press a key
            pressed = pygame.key.get_pressed()
            #print(pressed)
            buttons = [pygame.key.name(k) for k,v in enumerate(pressed) if v]
            #print("k: " + k + "v: " + v)
            print(buttons)
            flag = True
            
            #print("buttons : ",buttons[0])

            if buttons[0] == 'w':
                cmd = 'F'
                print("FFF")
                send()
            elif buttons[0] == 's':
                cmd = 'B'
                send()
            elif buttons[0] == 'a':
                cmd = 'L'
                send()
            elif buttons[0] == 'd':
                cmd = 'R'
                send()
            elif (buttons[0] == 'b'):
                cmd = 'S'
                send()
            
           
        elif event.type == pygame.KEYUP: # If user release what he pressed
            flag = False
            if (event.key == K_w) or (event.key == K_s) or (event.key == K_b):
                cmd = 'M'
            else :
                cmd = 'N'
            send()
            print("Key up!!")

        elif event.type == pygame.QUIT:  # If user clicked close.
            done = True                 
 

 
# Be IDLE friendly
pygame.quit()


#출처: https://kkamikoon.tistory.com/132?category=797804 [컴퓨터를 다루다]
