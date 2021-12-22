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