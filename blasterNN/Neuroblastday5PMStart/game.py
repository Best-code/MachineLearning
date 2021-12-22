import pygame
import constants
import gamestates

class Game:
    def __init__(self):
        
        pygame.init()
        
        #Create the window
        resolution = (constants.window_width, constants.window_height)
        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("NeuroBlast")
        
        #Set up the clock to manage the frames per second
        clock = pygame.time.Clock()
        exit_game = False
        
        background = pygame.image.load('art/python-game_background.png')
        bgsize = background.get_size()
        #Because the sprite is larger than our window size, we need to resize the background so it will fit
        w, h = bgsize
        aspect = w/h
        wscale = constants.game_width
        hscale = wscale/aspect
        bgscaled = pygame.transform.scale(background, (constants.game_width, int(hscale)))
        
        state = gamestates.Menu()
        
        #Game Loop, lets the player click the exit button to quit
        while not exit_game:
            event_queue = pygame.event.get()
            for event in event_queue:
                if event.type == pygame.QUIT:
                    exit_game = True
                    
            #Create the background on our screen using the blit function
            #It takes in the rescaled sprite, a position to display the sprite, and the rect parameters for the resized sprite
            screen.blit(bgscaled,(0,0),(0,0,constants.game_width,constants.window_height))
            
            state = state.update(screen, event_queue, clock.get_time()/1000.0, clock)
            if state == None:
                exit_game = True
            pygame.display.flip()
            clock.tick(constants.frames_per_second)
                
        pygame.quit()
        
Game()