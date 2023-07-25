# AI-Pong-Game

# Objective:
The objective of this assignment is to create a Python script, named student_ai.py, that implements 
an AI player capable of defeating the default AI player, chaser_ai.py, in a virtual game of Pong. 
The student's AI will compete against the chaser AI within the script pong_ai_v_ai.py.

# Game Overview:
Pong is a classic two-dimensional table tennis-like game, where two paddles (players) move vertically 
on either side of the screen to hit a ball back and forth. The objective is to prevent the ball from 
passing your paddle while trying to make the ball pass the opponent's paddle. The game ends when one 
player reaches a pre-defined score or when a specific time limit is reached.

# Script Components:
student_ai.py: The Python script the student will develop. It should contain the AI logic to control 
the student's paddle and make strategic decisions to outperform the chaser AI.
chaser_ai.py: The default AI script provided, representing the opponent that actively chases and attempts 
to hit the ball back towards the student's paddle.
pong_ai_v_ai.py: The main script that orchestrates the Pong game between the student's AI and the chaser 
AI. It will handle the game loop, ball movement, scoring, and communication between the AI scripts.

# Requirements:
- The student's AI should be written in Python, utilizing appropriate data structures and algorithms to 
control the paddle's movement and decision-making process.
- The student should avoid hardcoding specific ball movement patterns or paddle positions but instead create 
a dynamic AI that adapts to the ball's trajectory and aims to outsmart the chaser AI.
- The AI scripts should be capable of interfacing with the game environment in pong_ai_v_ai.py, which includes 
accessing the game state, ball position, paddle positions, and sending control signals to move the student's 
paddle.
- The game should be fair, with a reasonable level of difficulty, allowing the student's AI a chance to win 
against the chaser AI. The student should experiment with different strategies and fine-tune their AI's 
parameters to achieve the best possible performance.
