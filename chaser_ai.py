# This is the sample AI that your AI must defeat.
#   Note: You can modify this file, but we will test your AI
#   against the original, unmodified file.
#   We will not use your version of this file
#   (so there is no reason to submit it).

class PongAI:
    def __init__(self, table_size):
        """
        table_size --   A tuple representing the dimensions of the table.
                        The x and y dimensions of the table are represented by
                                    table_size[0], table_size[1]
                        respectively.
        """
        self.table_size = table_size

    def pong_ai(self, paddle_rect, other_paddle_rect, ball_rect):
        """Return "up" or "down", depending on which way the paddle should go to
        align its centre with the centre of the ball
   
        Keyword arguments:
        paddle_rect -- A rectangle object representing the coordinates of your paddle.
                       The top-left corner of the rectangle is represented by the tuple
                                    paddle_rect.pos[0], paddle_rect.pos[1]
                       The dimensions (width, height) of the paddle are represented by
                                    paddle_rect.size[0], paddle_rect.size[1]
    
        other_paddle_rect -- A rectangle representing the opponent's paddle.
                        It is the same kind of object as above and its attributes
                        can be accessed in the same manner described above.
   
        ball_rect --    A rectangle representing the ball. It is the same kind of object
                        as the two above.
   
        Coordinates start at (0, 0) in the top-left corner.
        They look as follows:
   
   
                0             x
                |------------->
                |
                |             
                |
            y   v
        """
    
        # Check if paddle's y-coordinate is above the ball's y-coordinate
        if paddle_rect.pos[1]+paddle_rect.size[1]/2 < ball_rect.pos[1]+ball_rect.size[1]/2:
            return "down" # move paddle down
        else: # paddle's y-coordinate must be below the ball's y-coordinate
            return "up" # move paddle up