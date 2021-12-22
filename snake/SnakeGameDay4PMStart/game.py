import pygame
import sys
from constants import Constants
from point import Point
from color import Color
from environment import Environment
from objects import WallScreenObject, SnakeScreenObject, FruitScreenObject
from action import Action
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_q
from pygame.locals import K_q
from human_solver import HumanSolver
from random_ai_solver import RandomSolver
from random_avoidance_solver import RandomAvoidanceSolver
from direct_path_solver import DirectPathSolver
from customAI import Custom

class Game:

    pygame.init()
    pygame.display.set_caption("Snake Game")
    action = None

    def __init__(self, model, fps, screen_width, screen_height):
 
        self.model = model
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.fps = fps
        self.pixel_size = Constants.PIXEL_SIZE
        self.navigation_bar_height = Constants.NAVIGATION_BAR_HEIGHT
        self.horizontal_pixels = int(screen_width / self.pixel_size)
        self.vertical_pixels = int((screen_height-self.navigation_bar_height) / self.pixel_size)
        self.game_started = False
        
        while True:
            if self.game_started:
                self.play_screen()
            else:
                self.start_screen()
    
    def start_screen(self):

        font = pygame.font.SysFont("Arial", 25)

        button_start = pygame.Rect(60, 130, 80, 40)
        pygame.draw.rect(self.screen, [0, 255, 0], button_start)
        start_text = font.render('Start', True, (0, 0, 0))
        self.screen.blit(start_text, (60, 130)) 

        button_quit = pygame.Rect(160, 130, 80, 40)
        pygame.draw.rect(self.screen, [255, 0, 0], button_quit)
        quit_text = font.render('Quit', True, (0, 0, 0))
        self.screen.blit(quit_text, (160, 130))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                if button_start.collidepoint(mouse_position):
                    print("Start button was pressed")
                    self.game_started = True
                    self.setup_world()
                if button_quit.collidepoint(mouse_position):
                    print("Quit button was pressed")
                    self.quit_game()
            if event.type == pygame.QUIT:
                self.quit_game()
        pygame.display.update()
        pygame.time.Clock().tick(self.fps)
        
    def setup_world(self):
        self.screen_objects = []
        self.environment = Environment(width=self.horizontal_pixels,
                                       height=self.vertical_pixels)

        self.wall = WallScreenObject(self)
        self.wall.points = list([self.screen_normalized_point(x) for x in self.environment.set_wall()])
        self.screen_objects.append(self.wall)
        
        self.fruit = FruitScreenObject(self)
        self.fruit.points = list([self.screen_normalized_point(x) for x in self.environment.set_fruit()])
        self.screen_objects.append(self.fruit)
        
        self.snake = SnakeScreenObject(self)
        self.snake.points = list([self.screen_normalized_point(x) for x in self.environment.set_snake()])
        self.screen_objects.append(self.snake)

    def quit_game(self):
        pygame.quit()
        sys.exit()      
        
    def play_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q):
                    self.quit_game()
                else:
                    self.model.user_input(event)
        pygame.time.Clock().tick(self.fps)
        self.environment.eat_fruit_if_possible()
        move_action = self.model.move(self.environment)
        if (self.environment.step(move_action) == False):
            self.game_started = False
        self.sync_screen_with_environment()
        self.draw_screen()
        pygame.display.update()
        
    def move(self, environment):
        if (self.action == None):
            return environment.snake_action
        backward_action = (self.action[0] == environment.snake_action[0] * -1) or (self.action[1] == environment.snake_action[1] * -1)
        return environment.snake_action if backward_action else self.action
        
    def user_input(self, event):
        if event.key == K_UP:
            self.action = Action.up
        elif event.key == K_DOWN:
            solver = HumanSolver()
            self.action = Action.down
        elif event.key == K_LEFT:
            self.action = Action.left
        elif event.key == K_RIGHT:
            self.action = Action.right
        elif event.key == K_q:
            self.quit_game()
        
        
    def sync_screen_with_environment(self):
        self.fruit.points = list([self.screen_normalized_point(x) for x in self.environment.fruit])
        self.snake.points = list([self.screen_normalized_point(x) for x in self.environment.snake])
    
    def screen_normalized_point(self, point):
        return Point(point.x * self.pixel_size, self.navigation_bar_height + (point.y * self.pixel_size))
        
    def draw_pixel(self, screen, color, point):
        rect = pygame.Rect(point.x, point.y, self.pixel_size, self.pixel_size)
        pygame.draw.rect(screen, color, rect)
        
    def draw_screen(self):
        self.screen.fill(Color.white)
        
        for game_object in self.screen_objects:
            game_object.draw(self.screen)
        
        for x in range(0, (self.horizontal_pixels*self.pixel_size)+1):
            self.draw_pixel(self.screen, Color.gray, Point(x, 0))
            for y in range(0, (self.navigation_bar_height-self.pixel_size)+1):
                self.draw_pixel(self.screen, Color.gray, Point(x, y))
        
        font = pygame.font.SysFont("Arial", int(self.navigation_bar_height / 1.3))
        score_text = font.render(str(self.environment.reward()), True, Color.green)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (self.navigation_bar_height/2, self.navigation_bar_height/2)
        self.screen.blit(score_text, score_text_rect)


# solver = HumanSolver()
# solver = RandomSolver()
# solver = RandomAvoidanceSolver()
# solver = DirectPathSolver()
solver = Custom()
Game(solver, Constants.FPS, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT+Constants.NAVIGATION_BAR_HEIGHT)
			