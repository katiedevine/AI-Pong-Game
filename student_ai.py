# student_ai

# This program is designed to defeat the Chaser_AI player within the PongAIvAI game

import os, sys, time, math, random
import pygame
from pygame.locals import *

#importing clock module
clock = pygame.time.Clock()
start_time = time.time()

#making empty lists for specific parameters (ball positions & slope)
change_in_x = []
change_in_y = []
slope_list = []
ball_x = []
ball_y = []

class PongAI:
    def __init__(self, table_size):
        self.table_size = table_size
        
    def pong_ai(self, paddle_rect, other_paddle_rect, ball_rect):
        
        #when paddle is on the left side
        if paddle_rect.pos[0] < (self.table_size[0] / 2):
            #append ball x & y positions into lists
            ball_x.append(ball_rect.pos[0])
            ball_y.append(ball_rect.pos[1])
                
            #once these lists are greater than 1, can calculate the change in each (change in x & change in y)
            if len(ball_x) > 1 and len(ball_y) > 1:
                        
                x_start = ball_x[-2]
                x_end = ball_x[-1]
                        
                y_start = ball_y[-2]
                y_end = ball_y[-1]
                        
                change_in_x.append(x_end - x_start)
                change_in_y.append(y_end - y_start)
            
            #if there are more numbers of 
            if len(change_in_x) > 1 and x_start < x_end:
                
                if (paddle_rect.pos[1] + (paddle_rect.size[1])/2)  > (self.table_size[1] / 2):
                                
                    return "up"
                            
                else:
                                
                    return "down"
                    
            else: #follow the y position of the ball when the ball isn't going right
                if paddle_rect.pos[1]+paddle_rect.size[1]/2 < ball_rect.pos[1]+ball_rect.size[1]/2:
                    return "down" # move paddle down
                        
                else: # paddle's y-coordinate must be below the ball's y-coordinate
                    return "up" # move paddle up
                
        #when paddle is on the right side       
        else:
            ball_x.append(ball_rect.pos[0])
            ball_y.append(ball_rect.pos[1])
            
            #if there are more than 1 x & y positions
            if len(ball_x) > 1 and len(ball_y) > 1:
                    
                x_start = ball_x[-2] 
                x_end = ball_x[-1]
                    
                y_start = ball_y[-2]
                y_end = ball_y[-1]
                
                #append the changes in x & y
                change_in_x.append(x_end - x_start)
                change_in_y.append(y_end - y_start)
                
                #when the ball is traveling to the left (towards the other paddle), our paddle will go to the middle
                if len(change_in_x) > 1 and x_start > x_end:
                    if (paddle_rect.pos[1] + (paddle_rect.size[1])/2)  > (self.table_size[1] / 2):
                            
                        return "up"
                        
                    else:
                            
                        return "down"
                    
                #when there is a change in x
                if (x_end - x_start) != 0:
                    slope_list.append((y_end - y_start) / (x_end - x_start))
                    slope = (y_end - y_start) / (x_end - x_start)
                    
                else: # if there is not a big change in x, divide by a number close to 0
                    slope = (y_end - y_start) / 0.01
                    
                        
                
                if slope == 0: #if there is no change in y & slope ends up being 0
                    reference_x = y_start / 1
                    
                else:
                    reference_x = y_start / slope
                
                #the next following lines, we used similar triangles to figure out if the ball is going to hit the side walls
                    #before reaching the other paddle
                distance_ball_to_paddle = paddle_rect.pos[0] - x_start
                
                if reference_x > distance_ball_to_paddle:
                #when ball doesn't hit wall, slope method to predict where ball will land
                    
                    #target y for where the ball is supposedly is to hit
                    target = y_start - (slope * distance_ball_to_paddle)
                    
                    if paddle_rect.pos[1] > target:
                        return "up"
                    
                    if paddle_rect.pos[1] < target:
                        return "down"
                    
                else: #use the chaser_ai method
                    if paddle_rect.pos[1]+paddle_rect.size[1]/2 < ball_rect.pos[1]+ball_rect.size[1]/2:
                        return "down" # move paddle down
                        
                    else: # paddle's y-coordinate must be below the ball's y-coordinate
                        return "up" # move paddle up
                               
              
             
end_time = time.time()
print("Time taken: {} seconds".format(end_time - start_time))   
