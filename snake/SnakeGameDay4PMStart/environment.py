from constants import Constants
from tile import Tile
from point import Point
import random
from action import Action

class Environment:
    
    snake_action = None
    snake_length = 1
	
    def __init__(self, width=Constants.ENV_WIDTH, height=Constants.ENV_HEIGHT):
        self.width = width
        self.height = height
        self.tiles = []
        
        for y in range(0, self.height):
            self.tiles.append([])
            for x in range(0, self.width):
                self.tiles[y].append(Tile.empty)
                
    def set_wall(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    self.tiles[y][x] = Tile.wall
        self.wall = self.points_of(Tile.wall)
        return self.wall
    
    def points_of(self, environment_object):
        points = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                if tile == environment_object:
                    points.append(Point(x, y))
        return points
    
    def random_available_position(self, distance_from_edge = 0):
        tile = None
        while tile is None or tile is not Tile.empty:
            random_x = random.randint(distance_from_edge, self.width-(distance_from_edge+1))
            random_y = random.randint(distance_from_edge, self.height-(distance_from_edge+1))
            tile = self.tiles[random_x][random_y]
        return Point(random_x, random_y)
    
    def set_snake(self):
        self.clear_environment_for(Tile.snake)
        random_position = self.random_available_position(distance_from_edge = 3)
        self.tiles[random_position.x][random_position.y] = Tile.snake
        self.snake = self.points_of(Tile.snake)
        if self.snake_action is None:
            self.snake_action = random.choice(Action.all())
        return self.snake
    
    def step(self, action):
        self.snake_action = action
        head = self.snake[0]
        x, y = self.snake_action
        new = Point(x=(head.x + x),
                    y=(head.y + y))
        if new in self.snake:
            print("Hit Snake, game over!")
            return False
        elif new in self.wall:
            print("Hit Wall, game over!")
            return False
        else:
            self.snake.insert(0, new)
            self.tiles[new.y][new.x] = Tile.snake
            if len(self.snake) > self.reward():
                last = self.snake.pop()
                self.tiles[last.y][last.x] = Tile.empty
            return True
    
    def set_fruit(self):
        self.clear_environment_for(Tile.fruit)
        random_position = self.random_available_position()
        self.tiles[random_position.x][random_position.y] = Tile.fruit
        self.fruit = self.points_of(Tile.fruit)
        return self.fruit
    
    def clear_environment_for(self, environment_object):
        points_to_clear = self.points_of(environment_object)
        for point in points_to_clear:
            self.tiles[point.y][point.x] = Tile.empty
            
    def reward(self):
        return self.snake_length
    
    def eat_fruit_if_possible(self):
        if self.fruit[0] == self.snake[0]:
            self.snake_length += 1
            self.set_fruit()
            return True
        return False
    
    def possible_actions_for_current_action(self, current_action):
        actions = Action.all()
        reverse_action = (current_action[0] * -1, current_action[1] * -1)
        actions.remove(reverse_action)
        return actions
				 