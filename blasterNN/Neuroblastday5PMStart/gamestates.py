import pygame
from game_utils import display_text
from game_utils import load_font
import constants
from actors import Player
from actors import Enemy
import brain
import game_utils


class GameState():
    def update(self, screen, event_queue, delta_time, clock):
        return self
    
class Menu(GameState):
    def __init__(self):
        self.logo = pygame.image.load("art/neuro-blast_logo.png")
        load_font(24)
        self.menu_selection = 2
        
    def update(self, screen, event_queue, delta_time, clock):
        screen.blit(self.logo,(screen.get_width() / 4 - 265,screen.get_height() * 3 / 4-500))
        
        display_text('Play', screen.get_width() / 4 - 20, screen.get_height() * 3 / 4
                    - 80, constants.WHITE, screen)
        display_text('Train', screen.get_width() / 4 - 20, screen.get_height() * 3 / 4
                    - 40, constants.WHITE, screen)
        display_text('Exit', screen.get_width() / 4 - 20, screen.get_height() * 3 / 4,
                    constants.WHITE, screen)
        display_text(u'\u00bb', screen.get_width() / 4 - 60, screen.get_height() * 3 / 4
                    - 40*self.menu_selection, constants.WHITE, screen)
        
        next_state = self
        # Logic for handling key presses
        for event in event_queue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu_selection -= 1
                    #wrap from bottom to top
                    if self.menu_selection == -1:
                        self.menu_selection = 2
                if event.key == pygame.K_UP:
                    self.menu_selection += 1
                    #wrap from top to bottom
                    if self.menu_selection == 3:
                        self.menu_selection = 0
                 # New Logic: If the "Play" mode is selected, add the False argument
                if event.key == pygame.K_RETURN:
                    if self.menu_selection == 2:
                        next_state = Play(False)
                    elif self.menu_selection == 1:
                        next_state = Play(True)
                #
                    else:
                        #Exit the game
                        next_state = None
        return next_state
    
class Play(GameState):
    
     # The initialization will now take in the "training_mode" variable
    def __init__(self, training_mode):
    #
        self.userBullets = pygame.sprite.Group()
        self.player = Player(self.userBullets)
        self.userGroup = pygame.sprite.Group()
        self.userGroup.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        
        # Use an existing brain, or set up a new brain
        self.training_mode = training_mode
        if game_utils.trained_brain:
            self.play_brain = game_utils.trained_brain
        else:  
            self.play_brain = brain.StaticBrain()
        #
        
        self.enemy = Enemy(self.enemyBullets, self.play_brain)
        self.enemies.add(self.enemy)
 
        self.spawntimer = 0
        self.spawnbreak = constants.enemy_spawn_rate
        
        # Time for retraining the system
        self.training_timer = 0
        self.retrain_time = 3
        #
        
        self.score = 0
		#
        
    
    def update(self, screen, event_queue, delta_time, clock):
        
        self.player.update(screen, event_queue, delta_time)
        self.userGroup.draw(screen)
        
        # Get the player's information and pass it to the enemy's update method
        player_position = (self.player.x, self.player.y)
        player_velocity = (self.player.velx, self.player.vely)
        
        # Have enemies take in whether or not the game is in training mode
        self.enemies.update(screen, event_queue, delta_time, player_position, player_velocity, self.training_mode)
        self.enemies.draw(screen)
        #
        
        self.enemies.update(screen, event_queue, delta_time, player_position, player_velocity)
        #
        
        self.enemies.update(screen, event_queue, delta_time)
        self.enemies.draw(screen)
        
		# Update enemy bullets and draw them on screen
        self.enemyBullets.update(delta_time)
        self.enemyBullets.draw(screen)
		#
        
        # Update the bullets on the screen
        self.userBullets.update(delta_time)
        self.userBullets.draw(screen)
		#
        
        # Add collision
        enemies_hit = pygame.sprite.groupcollide(self.enemies,self.userBullets,False,True)
        for enemy, bullets in enemies_hit.items():
            enemy.TakeDamage(constants.player_bullet_damage)
            for b in bullets:
                self.score += constants.score_for_damage
        #
        # When the player is hit, update the logic to store hits in the brain
        # Also, only take damage in the play mode, not in the training mode
        player_hit = pygame.sprite.spritecollide(self.player,self.enemyBullets, True)
        for bullet in player_hit:
            self.play_brain.record_hit(bullet)
            if not self.training_mode:
                self.player.TakeDamage(constants.enemy_bullet_damage)
        #
        # Retrain the brain every 3 seconds
        self.training_timer += delta_time
        if (self.training_timer > self.retrain_time):
            self.play_brain.train()
            self.training_timer = 0
        #
        
        # Logic for hitting the player
        player_hit = pygame.sprite.spritecollide(self.player,self.enemyBullets, True)
        for bullet in player_hit:
            self.player.TakeDamage(constants.enemy_bullet_damage)
		#
        
        self.spawntimer += delta_time
        if self.spawntimer > self.spawnbreak:
			# Spawned enemies should use the brain we set up
            self.enemies.add(Enemy(self.enemyBullets, self.play_brain))
            #
            self.spawntimer = 0
        
        for event in event_queue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Update the escape key press to have it save the brain
                    self.play_brain.train()
                    game_utils.trained_brain = self.play_brain
                    return Menu()
                    #
                
        # Will display the score and health variables at the top of the screen
        display_text("Score: "+str(self.score), 200, 20, constants.WHITE, screen)
        display_text("Health: "+str(self.player.health), 350, 20, constants.WHITE, screen)    
		#        
        
        return self