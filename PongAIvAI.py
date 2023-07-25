#   Note: You can modify this file, but we will test your AI
#   against the original, unmodified file.
#   We will not use your version of this file
#   (so there is no reason to submit it).

#   PongAIvAI
#   Authors: Michael Guerzhoy and Denis Begun, 2014-2016.
#   http://www.cs.toronto.edu/~guerzhoy/
#   Email: guerzhoy at cs.toronto.edu
#   Modified by Jonathan Campbell for COMP 208 Winter 2020.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version. You must credit the authors
#   for the original parts of this code.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Parts of the code are based on T. S. Hayden Dennison's PongClone (2011)
#   http://www.pygame.org/project-PongClone-1740-3032.html

import os, sys, time, math, random

import pygame
from pygame.locals import *

# defining color RGB values
white = [255, 255, 255]
black = [0, 0, 0]

# clock to manage the FPS (frames per second)
clock = pygame.time.Clock()

class Rectf:
    # A class that stores coordinates of a rectangle in floating-point
    # with useful methods that can be performed on them
    
    def __init__(self, pos, size):
        # Create a rectangle with the given (x, y) position
        # and (height, width) size.
        
        self.pos = (pos[0], pos[1]) # (x, y)
        self.size = (size[0], size[1]) # (width, height)
    
    def move(self, x, y):
        # Move this rectangle by +x, +y units and return the new rectangle.
        # Size is kept the same.
        
        return Rectf((self.pos[0]+x, self.pos[1]+y), self.size)

    def move_ip(self, x, y, move_factor = 1):
        # Move this rectangle by +x*factor, +y*factor units in-place.
        
        self.pos = (self.pos[0] + x*move_factor, self.pos[1] + y*move_factor)

    def get_rect(self):
        # Return a copy (clone) of this rectangle cast to a PyGame Rect object.
        
        return Rect(self.pos, self.size)

    def copy(self):
        # Return a copy (clone) of this rectangle.
        
        return Rectf(self.pos, self.size)

    def intersect(self, other_Rectf):
        # Check if this rectangle intersects with other_Rectf.
        # Two rectangles intersect iff both x and y projections intersect.
        
        for i in range(2):
            if self.pos[i] < other_Rectf.pos[i]: # projection of self begins to the left
                if other_Rectf.pos[i] >= self.pos[i] + self.size[i]:
                    return 0
            elif self.pos[i] > other_Rectf.pos[i]:
                if self.pos[i] >= other_Rectf.pos[i] + other_Rectf.size[i]:
                    return 0
        return 1 #self.size > 0 and other_Rectf.size > 0


class Paddle:
    def __init__(self, pos, size, speed, max_angle,  facing, timeout):
        # Create a new Paddle.
        
        # The paddle is a rectangular object, so store its coordinates
        # in a Rectf object.
        self.Rectf = Rectf((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        
        self.speed = speed
        self.size = size
        self.facing = facing
        self.max_angle = max_angle
        self.timeout = timeout

    def factor_accelerate(self, factor):
        self.speed = factor*self.speed

    def move(self, enemy_Rectf, ball_Rectf, table_size):
        # Move the paddle.
        
        # The program crashes if move_getter crashes. The runtime of 
        # move_getter is not limited
        direction = self.move_getter.pong_ai(self.Rectf.copy(), enemy_Rectf.copy(), ball_Rectf.copy())
        
        # The program continues if move_getter crashes. The runtime of
        # move_getter is limited
        # direction = timeout(self.move_getter.pong_ai, (self.Rectf.copy(), enemy_Rectf.copy(), ball_Rectf.copy()), {}, self.timeout)
        
        if direction == "up":
            self.Rectf.move_ip(0, -self.speed)
        elif direction == "down":
            self.Rectf.move_ip(0, self.speed)

        to_bottom = (self.Rectf.pos[1]+self.Rectf.size[1])-table_size[1]
        if to_bottom > 0:
            self.Rectf.move_ip(0, -to_bottom)
        
        to_top = self.Rectf.pos[1]
        if to_top < 0:
            self.Rectf.move_ip(0, -to_top)

    def get_face_pts(self):
        return ((self.Rectf.pos[0] + self.Rectf.size[0]*self.facing, self.Rectf.pos[1]),
                (self.Rectf.pos[0] + self.Rectf.size[0]*self.facing, self.Rectf.pos[1] + self.Rectf.size[1]-1)
                )

    def get_angle(self, y):
        # For a ball hitting the paddle at the given y coordinate,
        # return the angle at which the ball should bounce back.
        
        # Determine the y-coordinate for the center of the paddle.
        center = self.Rectf.pos[1]+self.size[1]/2
        
        # How much does the given y deviate from the center?
        rel_dist_from_c = ((y-center)/self.size[1])
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        
        # What side of the center is the given y on?
        sign = 1 - 2*self.facing # will be 1 or -1

        return sign*rel_dist_from_c*self.max_angle*math.pi/180

class Ball:
    def __init__(self, table_size, size, paddle_bounce, wall_bounce, dust_error, init_speed_mag):
        # Create a new ball object.
        
        # Start with a random (x, y) speed vector.
        rand_ang = (.4+.4*random.random())*math.pi*(1-2*(random.random()>.5))+.5*math.pi
        speed = (init_speed_mag*math.cos(rand_ang), init_speed_mag*math.sin(rand_ang))
        
        # Start the ball in the middle of the board.
        pos = (table_size[0]/2, table_size[1]/2)
        
        # Rectangle representing the ball's position.
        self.Rectf = Rectf((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        
        self.speed = speed
        self.size = size
        self.paddle_bounce = paddle_bounce
        self.wall_bounce = wall_bounce
        self.dust_error = dust_error
        self.init_speed_mag = init_speed_mag
        self.prev_bounce = None

    def get_center(self):
        # Return the center (x, y) coordinate of the ball.
        
        return (self.Rectf.pos[0] + .5*self.Rectf.size[0], self.Rectf.pos[1] + .5*self.Rectf.size[1])

    def get_speed_mag(self):
        # Return the magnitude of the speed vector.
        
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    def factor_accelerate(self, factor):
        self.speed = (factor*self.speed[0], factor*self.speed[1])

    def move(self, paddles, table_size, move_factor):
        # Move the ball.
        
        moved = 0
        
        # The borders of the window serve as impassable walls.
        walls_Rects = [Rect((-100, -100), (table_size[0]+200, 100)),
                       Rect((-100, table_size[1]), (table_size[0]+200, 100))]

        # Check if the ball has collided with any of the walls.
        for wall_rect in walls_Rects:
            if self.Rectf.get_rect().colliderect(wall_rect):
                # A collision did occur.
                
                c = 0
                
                while self.Rectf.get_rect().colliderect(wall_rect):
                    self.Rectf.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)
                    c += 1 # this basically tells us how far the ball has traveled into the wall
                r1 = 1+2*(random.random()-.5)*self.dust_error
                r2 = 1+2*(random.random()-.5)*self.dust_error

                self.speed = (self.wall_bounce*self.speed[0]*r1, -self.wall_bounce*self.speed[1]*r2)
                
                while c > 0 or self.Rectf.get_rect().colliderect(wall_rect):
                    self.Rectf.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)
                    c -= 1 # move by roughly the same amount as the ball had traveled into the wall
                moved = 1
                
        # Check if the ball has collided with a paddle.
        for paddle in paddles:
            if self.Rectf.intersect(paddle.Rectf):
                # A collision did occur.
                
                if (paddle.facing == 1 and self.get_center()[0] < paddle.Rectf.pos[0] + paddle.Rectf.size[0]/2) or \
                (paddle.facing == 0 and self.get_center()[0] > paddle.Rectf.pos[0] + paddle.Rectf.size[0]/2):
                    continue
                
                c = 0
                
                while self.Rectf.intersect(paddle.Rectf) and not self.Rectf.get_rect().colliderect(walls_Rects[0]) and not self.Rectf.get_rect().colliderect(walls_Rects[1]):
                    self.Rectf.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)
                    c += 1
                
                theta = paddle.get_angle(self.Rectf.pos[1]+.5*self.Rectf.size[1])
                

                v = self.speed
                
                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                             math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0]

                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                              math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]


                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                if  v[0]*(2*paddle.facing-1) < 1: # ball is not traveling (a) away from paddle (b) at a sufficient speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) # transform y velocity so as to maintain the speed
                    v[0] = (2*paddle.facing-1) # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to the  increase by 1.2

                #a bit hacky, prevent multiple bounces from accelerating
                #the ball too much
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce, v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle
                

                while c > 0 or self.Rectf.intersect(paddle.Rectf):
                    self.Rectf.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)
                    c -= 1
                
                moved = 1

        if not moved:
            self.Rectf.move_ip(self.speed[0], self.speed[1], move_factor)

class HumanInput():
    def __init__(self, table_size):
        self.table_size = table_size
    
    def pong_ai(self, paddle_rect, other_paddle_rect, ball_rect):
        # Handle user input (up/down arrows).
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            return "up"
        elif keys[pygame.K_DOWN]:
            return "down"
        else:
            return None

def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''From: http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
    
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        print("TIMEOUT")
        return default
    else:
        return it.result

def render(screen, paddles, ball, score, table_size):
    # Draw the Pong board to the screen.
    screen.fill(black) # fill screen with black color

    # Draw paddle rectangles.
    pygame.draw.rect(screen, white, paddles[0].Rectf.get_rect())
    pygame.draw.rect(screen, white, paddles[1].Rectf.get_rect())

    # Draw circle for ball.
    pygame.draw.circle(screen, white, (int(ball.get_center()[0]), int(ball.get_center()[1])),  int(ball.Rectf.size[0]/2), 0)

    # Draw line separating sides.
    pygame.draw.line(screen, white, [screen.get_width()/2, 0], [screen.get_width()/2, screen.get_height()])

    # Draw scores
    score_font = pygame.font.Font(None, 32)
    screen.blit(score_font.render(str(score[0]), True, white), [int(0.4*table_size[0])-8, 0])
    screen.blit(score_font.render(str(score[1]), True, white), [int(0.6*table_size[0])-8, 0])

    # Flip drawing to screen
    pygame.display.flip()

def check_point(score, ball, table_size):
    # Check if a point has been scored and return the updated score.
    
    if ball.Rectf.pos[0]+ball.size[0]/2 < 0:
        score[1] += 1
        ball = Ball(table_size, ball.size, ball.paddle_bounce, ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        return (ball, score)
    elif ball.Rectf.pos[0]+ball.size[0]/2 >= table_size[0]:
        ball = Ball(table_size, ball.size, ball.paddle_bounce, ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        score[0] += 1
        return (ball, score)

    return (ball, score)


def game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, display):
    # Main game loop.
    
    score = [0, 0]

    # Continue until a player has reached max score (won the game)
    while max(score) < score_to_win:
        old_score = score[:]
        
        # Check if a point has been scored.
        ball, score = check_point(score, ball, table_size)
        
        # Move the paddles.
        paddles[0].move(paddles[1].Rectf, ball.Rectf, table_size)
        paddles[1].move(paddles[0].Rectf, ball.Rectf, table_size)
        
        # Move the ball.
        inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5)
        if inv_move_factor > 0:
            for i in range(inv_move_factor):
                ball.move(paddles, table_size, 1./inv_move_factor)
        else:
            ball.move(paddles, table_size, 1)
        
        
        if not display:
            continue
        if score != old_score:
            # Print a message if a point has been scored.
            font = pygame.font.Font(None, 32)
            if score[0] != old_score[0]:
                screen.blit(font.render("Left scores!", True, white, black), [0, 32])
            else:
                screen.blit(font.render("Right scores!", True, white, black), [int(table_size[0]/2+20), 32])

            pygame.display.flip()
            clock.tick(turn_wait_rate)


        # Update the screen.
        render(screen, paddles, ball, score, table_size)
        
        # Handle user input (q for quit).
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            return

        clock.tick(clock_rate)

    # Print a message for the winner.
    font = pygame.font.Font(None, 64)
    if score[0] > score[1]:
        screen.blit(font.render("Left wins!", True, white, black), [24, 32])
    else:
        screen.blit(font.render("Right wins!", True, white, black), [24, 32])
    pygame.display.flip()
    clock.tick(2)

    pygame.event.pump()
    while any(pygame.key.get_pressed()):
        pygame.event.pump()
        clock.tick(30)

    print(score)

def init_game():
    table_size = (440, 280)
    paddle_size = (10, 70)
    ball_size = (15, 15)
    paddle_speed = 1
    max_angle = 45

    paddle_bounce = 1.2
    wall_bounce = 1.00
    dust_error = 0.00
    init_speed_mag = 2
    timeout = 0.0003
    clock_rate = 80
    turn_wait_rate = 3
    score_to_win = 10

    screen = pygame.display.set_mode(table_size)
    pygame.display.set_caption('PongAIvAI')

    paddles = [Paddle((20, table_size[1]/2), paddle_size, paddle_speed, max_angle,  1, timeout),
               Paddle((table_size[0]-20, table_size[1]/2), paddle_size, paddle_speed, max_angle, 0, timeout)]
    ball = Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag)

    
    
    import student_ai
    import chaser_ai
    
    # These lines control the AI used for the two sides.

    paddles[0].move_getter = chaser_ai.PongAI(tuple(table_size))
    #paddles[1].move_getter = chaser_ai.PongAI(tuple(table_size))
    
    # To play a side yourself (using the arrow keys),
    # un-comment the line below with 'directions_from_input'
    # and comment out line 437.

    #paddles[1].move_getter = HumanInput(table_size)
    
    # To play a side using your AI,
    # uncomment the line below
    # and comment out line 437.
    
    paddles[1].move_getter = student_ai.PongAI(table_size)
                        
    
    
    game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, 1)
    
    screen.blit(pygame.font.Font(None, 32).render(str('SWITCHING SIDES'), True, white), [int(0.6*table_size[0])-8, 0])
    
    pygame.display.flip()
    clock.tick(4)
    
    paddles[0].move_getter, paddles[1].move_getter = paddles[1].move_getter, paddles[0].move_getter
    
    game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, 1)
    
    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    init_game()
