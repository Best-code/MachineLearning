from color import Color

class ScreenObject:

    points = []

    def __init__(self, game, color):
        self.game = game
        self.color = color

    def draw(self, screen):
        for point in self.points:
            self.game.draw_pixel(screen, self.color, point)
            
class WallScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.black)
        
class SnakeScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.green)
        
class FruitScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.red)