import random
from base_game_model import BaseGameModel
from point import Point
from action import Action
 
class AvoidanceLookAheadSolver(BaseGameModel):
    
    def __init__(self):
        BaseGameModel.__init__(self, "Direct Path")
        
    def move(self, environment):
        BaseGameModel.move(self, environment)
        
        preferred_actions = []
        #Check the location of the fruit relative to the snake head
        if environment.fruit[0].x > environment.snake[0].x:
            #If the fruit is to the right of the snake
            preferred_actions.append(Action.right)
        elif environment.fruit[0].x < environment.snake[0].x:
            #If the fruit is to the right of the snake
            preferred_actions.append(Action.left)
        
        #Check the location of the fruit relative to the snake head
        if environment.fruit[0].y < environment.snake[0].y:
            #If the fruit is above the snake
            preferred_actions.append(Action.up)
        elif environment.fruit[0].y > environment.snake[0].y:
            #If the fruit is below the snake
            preferred_actions.append(Action.down)
        
        #Pick an action from the preferred list
        
        
        #####
        #picked_action = self.check_path(environment, preferred_actions)
        
        
        
        
        #####
        #If you can't use any preferred actions without dying,
        #pick a random action to perform
        
        #environment.snake[0] is the head of the snake
        #environment.snake_action is our last action
        
        # #
        #    
        #     if (avoidance_action is None):
        #         return environment.snake_action
        #     else:
        #         return avoidance_action
        # #else:
        #     #return picked_action
        # if (picked_action is None):
        #     avoidance_action = self.check_paths_at_point(environment, environment.snake[0], environment.snake_action, 10)
        #     if (len(avoidance_action) == 0):
        #         return environment.snake_action
        #     else:
        #         return random.choice(avoidance_action)
        # else:
        #     return picked_action
        print("hello")
        avoidance_action = self.check_paths_at_point(environment, environment.snake[0], environment.snake_action, 2)
        if (len(avoidance_action) == 0):
            return environment.snake_action
        else:
            return random.choice(avoidance_action)
        
				  
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
        
    def check_paths_at_point(self, environment, point, input_action, my_current_depth):
        print("Checking Paths")
        all_valid_actions = environment.possible_actions_for_current_action(input_action)
        obstacle_avoidance_actions = []
        for looped_action in all_valid_actions:
            x, y = looped_action
            new_point = Point(x=(point.x + x),
                        y=(point.y + y))
            #If you won't run into a wall 
            if ((not new_point in environment.snake) and (not new_point in environment.wall)):
                print("Won't crash here")
                #if (my_current_depth > 0):
                if (abs(new_point.x - environment.snake[0].x) < 2 and abs(new_point.y - environment.snake[0].y) < 2):
                    obstacle_avoidance_actions.append(looped_action)
                    print("Loop through below")
                    paths_checked_below = self.check_paths_at_point(environment, new_point, looped_action, my_current_depth - 1)
                    
                # print("Point is:", 
                #       str(point.x) + "," + str(point.y), 
                #       "Input Action:", 
                #       str(input_action), 
                #       "ValidActions At that point with that input:", 
                #       str(len(paths_checked_below)))
                    # if (len(paths_checked_below) > 0):
                    #     obstacle_avoidance_actions.append(looped_action)
                        
        #if (len(obstacle_avoidance_actions) == 0):
        #    return []
        #else:
            #return random.choice(obstacle_avoidance_actions)
        #    return obstacle_avoidance_actions
        return obstacle_avoidance_actions