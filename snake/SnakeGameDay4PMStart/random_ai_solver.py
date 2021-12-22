import random
from base_game_model import BaseGameModel
 
class RandomSolver(BaseGameModel):
 
    def __init__(self):
        BaseGameModel.__init__(self, "Random")
 
    def move(self, environment):
        potential_actions = environment.possible_actions_for_current_action(environment.snake_action)
        return random.choice(potential_actions)
				  