from game_utils import display_text
import constants
import pygame

class Brain:
    
    def __init__(self):
        self.trained = True
        self.brain_name = "AI: Fire Constantly"
        self.mapShots = {}
        self.mapHits = {}
        
        
    # Should I fire right now?
    def fire_decision(self, player_variables):
        return True
    
    # Track a fired bullet for learning
    def add_shot(self, bullet, player_variables):
        self.mapShots[bullet] = player_variables
    
    # Track hit bullets
    def record_hit(self, bullet):
        self.mapHits[bullet] = 1
    
    # Tracked missed bullets
    def record_miss(self, bullet):
        self.mapHits[bullet] = 0
    
    # Basic Brain never learns
    def train(self):
        pass
    
    def draw(self, screen):
        # This code will put a black background on the right side of the screen for us to draw over
        surf = pygame.Surface((640,720))
        surf.fill((0,0,0))
        screen.blit(surf,(640,0))
        #
        
        display_text(self.brain_name, 960, 60, constants.WHITE, screen)
        
class StaticBrain(Brain):
    
    # Initialization updated to store variables about number of hits and misses
    def __init__(self):
        Brain.__init__(self)
        self.brain_name = "AI: Fire When Player Below"
        self.total_bullets = 0
        self.total_hits = 0
        self.total_misses = 0
    #
    
    # Our "training" will simply be counting the number of total shots, total hits, and total misses
    def train(self):
        self.total_bullets = len(self.mapShots)
        self.total_hits = sum(self.mapHits.values())
        self.total_misses = len(self.mapHits.values()) - self.total_hits
    #
    
    # "Drawing" the brain will just be showing counts of shots, hits, and misses
    def draw(self, screen):
        super().draw(screen)
        
        display_text("Total Bullets Fired: " + str(self.total_bullets), 960, 90, constants.WHITE, screen)
        display_text("Total Bullets Hit: " + str(self.total_hits), 960, 120, constants.WHITE, screen)
        display_text("Total Bullets Missed: " + str(self.total_misses), 960, 150, constants.WHITE, screen)