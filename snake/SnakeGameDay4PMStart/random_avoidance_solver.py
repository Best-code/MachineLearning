import random
from base_game_model import BaseGameModel
from point import Point
 
 
class RandomAvoidanceSolver(BaseGameModel):
 
    action = None
    
    def __init__(self):
        BaseGameModel.__init__(self, "Random_Avoidance")
 
    def move(self, environment):
        BaseGameModel.move(self, environment)
        all_actions = environment.possible_actions_for_current_action(environment.snake_action)
        
        #This list will contain all actions which avoid obstacles
        obstacle_avoidance_actions = []
        for action in all_actions:
            head = environment.snake[0]
            x, y = action
            new = Point(x=(head.x + x),
                        y=(head.y + y))
            #Check to see that the new point you made does not contain a snake point or a wall point
            if ((not new in environment.snake) and (not new in environment.wall)):
                #If the new position caused by that action does not cause an immediate crash, add it to our list
                obstacle_avoidance_actions.append(action)
        
        #If there is no action that will allow you to avoid a crash, just keep going forwards
        if (len(obstacle_avoidance_actions) == 0):
            return environment.snake_action
        else:
            return random.choice(obstacle_avoidance_actions)