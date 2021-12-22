import pygame
import pygame.freetype

# Add the trained_brain variable
trained_brain = None
#
# Utility functions
def load_font(size):
    global font
    font = pygame.freetype.Font('font/De Valencia (beta).otf', size)

def display_text(text, x, y, color, surface):
    global font
    text_color = pygame.Color(*color)
    text = font.render(text, text_color)
    text_position = text[0].get_rect(centerx=x, centery=y)
    surface.blit(text[0], text_position)