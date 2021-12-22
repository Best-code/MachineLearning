import random
from base_game_model import BaseGameModel
from point import Point
from action import Action
 
class DirectPathSolver(BaseGameModel):
    
    def __init__(self):
        BaseGameModel.__init__(self, "Direct Path")
        
    def move(self, environment):
        BaseGameModel.move(self, environment)
        
        preferred_actions = []
        #Check the location of the fruit relative to the snake head
        if (environment.fruit[0].x > environment.snake[0].x):
            #If the fruit is to the right of the snake
            preferred_actions.append(Action.right)
        elif (environment.fruit[0].x < environment.snake[0].x):
            #If the fruit is to the right of the snake
            preferred_actions.append(Action.left)
        
        #Check the location of the fruit relative to the snake head
        if (environment.fruit[0].y < environment.snake[0].y):
            #If the fruit is above the snake
            preferred_actions.append(Action.up)
        elif (environment.fruit[0].y > environment.snake[0].y):
            #If the fruit is below the snake
            preferred_actions.append(Action.down)
            
        #Pick an action from the preferred list
        picked_action = self.check_path(environment, preferred_actions)
        #If you can't use any preferred actions without dying,
        #pick a random action to perform
        if (picked_action is None):
            all_actions = environment.possible_actions_for_current_action(environment.snake_action)
            avoidance_action = self.check_path(environment, all_actions)
            if (avoidance_action is None):
                return environment.snake_action
            else:
                return avoidance_action
        else:
            return picked_action
            
    def check_path(self, environment, actions_list):
        obstacle_avoidance_actions = []
        for action in actions_list:
            head = environment.snake[0]
            x, y = action
            new = Point(x=(head.x + x),
                        y=(head.y + y))
            #If you won't run into a wall 
            if ((not new in environment.snake) and (not new in environment.wall)):
                obstacle_avoidance_actions.append(action)
        
        if (len(obstacle_avoidance_actions) == 0):
            return None
        else:
            return random.choice(obstacle_avoidance_actions)
            