import pygame
import constants
from random import randrange
import math

class SpriteSequence():
    def __init__(self,sheet,rect):
        self.sheet = sheet
        self.rect = rect
        
    def update(self, surface, pos):
        surface.blit(self.sheet,pos,(self.rect.x,
                                        self.rect.y,
                                        self.rect.w,self.rect.h))
        

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        self.spritesheet = pygame.image.load("art/python-sprites.png")
        self.sprite_sequence = None
		# Add a new variable for the ship's health
        self.health = constants.starting_health
		#
    
	# Add the TakeDamage Method
    def TakeDamage(self, damage):
        # This is a failsafe in case two bullets hit a ship on the same frame
        # If one bullet would cause the ship to be destroyed, the next
        # bullet would try to destroy the ship too. 
        if self.health<=0:
            return
        
        self.health -= damage
        if self.health <= 0:
            self.Die()

    def Die(self):
        self.kill()
	#
        
class Bullet(pygame.sprite.Sprite):
    # On initialization, it can take in a brain variable. When the player makes bullets, it won't store them in a brain
    def __init__(self, x, y, color, container, brain = None):
    #
        pygame.sprite.Sprite.__init__(self, container)
        self.spritesheet = pygame.image.load("art/python-sprites.png")
        self.image = pygame.Surface((16,16), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        basex = 423
        # Enemy bullets will be red, player bullets will be green
        if color==constants.RED:
            basex += 96
            self.speed = constants.enemy_bullet_speed
            self.direction = constants.enemy_bullet_direction
        else:
            self.speed = constants.player_bullet_speed
            self.direction = constants.player_bullet_direction
        # Generate the sprite image from spritesheet
        ssrect = pygame.Rect((basex,710,16,16))
        self.image.blit(self.spritesheet,(0,0),ssrect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        #Set up the brain to be used later
        self.brain = brain
        #
        
    def update(self, delta_time):
        (x, y) = self.rect.center
        y += self.direction[1] * self.speed * delta_time
        x += self.direction[0] * self.speed * delta_time
        self.rect.center = (x, y)
        # If the bullet leaves the frame, destroy it so we don't have to track it anymore
        if y <= 0 or y >= constants.window_height or x <= 0 or x >= constants.game_width:
            # When you leave the visible window, and you haven't yet hit the player, record a miss in the brain
            if self.brain:
                self.brain.record_miss(self)
            #
            self.kill()
        
        
class Player(Ship):
	# Add the bullet group setup
    def __init__(self, bullet_group):
	#
        super(Player, self).__init__()
        #Start Position
        self.x = 320
        self.y = 500
        #When you start, you're not moving
        self.velx = 0
        self.vely = 0      
        #Ensuring that the image will be 96x96 pixels
        self.image = pygame.Surface((96,96))
        self.rect = self.image.get_rect()
        ## Generate the sprite image from spritesheet
        ssrect = pygame.Rect((96,96,96,96))
        self.image.blit(self.spritesheet,(0,0),ssrect)
        self.image.convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        #Pick the specific image from the sprite sheet to use
        self.idle_sequence = SpriteSequence(self.spritesheet,pygame.Rect(96,576,96,192))
        
		# Add the setup for firing the bullets
        self.can_fire = True
        self.bullets = bullet_group
        self.shot_cooldown = constants.player_shot_cooldown
        self.cooldown_timer = 0
		# 
 
    def update(self, screen, event_queue, delta_time):
        
        self.rect.center = (self.x, self.y)
        self.image.fill((0,0,0))
        self.idle_sequence.update(self.image,(0,0))
        
        # Add firing cooldown logic
        if not(self.can_fire):
            self.cooldown_timer += delta_time
            if self.cooldown_timer>self.shot_cooldown:
                self.can_fire = True
                self.cooldown_timer = 0
		#
        
        keys=pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velx = -constants.ship_acceleration
        if keys[pygame.K_RIGHT]:
            self.velx = constants.ship_acceleration
        if keys[pygame.K_UP]:
            self.vely = -constants.ship_acceleration
        if keys[pygame.K_DOWN]:
            self.vely = constants.ship_acceleration
        # Add if statement to fire a bullet if the player presses the space bar
        if keys[pygame.K_SPACE] and self.can_fire:
            Bullet(self.x, self.y-42, constants.BLUE, self.bullets)
            self.can_fire = False
		#

        #When the player is not pressing a key, change the velocity to 0
        if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.vely = 0
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.velx = 0
            
        #Ensures that the player cannot move outside the boundaries of the screen
        if self.x+(self.velx*delta_time)>640-48 or self.x+(self.velx*delta_time)<48:
            self.velx = 0
        if self.y+(self.vely*delta_time)>720-48 or self.y+(self.vely*delta_time)<48:
            self.vely = 0
        
        #This code ensures that the movement speed is not affected by the framerate
        self.x += self.velx * delta_time
        self.y += self.vely * delta_time
        
class Enemy(Ship):
    def __init__(self, bullet_group, brain):
        super(Enemy, self).__init__()
        # Enemy specific stuff here
        self.brain = brain
        self.x = randrange(0,450)
        self.y = -50
        self.velx = 0
        self.vely = constants.enemy_move_speed       # wish there was a vector class
        self.image = pygame.Surface((96,192))
        self.rect = self.image.get_rect()
        ## Generate the sprite image from spritesheet
        ssrect = pygame.Rect((96,192,96,192))
        self.image.blit(self.spritesheet,(0,0),ssrect)
        self.image.convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect.center = (self.x, self.y)
        self.spawntime = pygame.time.get_ticks()
        self.idle_sequence = SpriteSequence(self.spritesheet,pygame.Rect(96,192,96,192))
        
        self.bullets = bullet_group
        self.shot_cooldown = constants.enemy_shot_cooldown
        self.cooldown_timer = 0
        self.can_fire = True
        

        
    def update(self, screen, event_queue, delta_time, player_position, player_velocity, training_mode):
        if not self.alive():
            return
        
    
        self.velx = math.sin((pygame.time.get_ticks()-self.spawntime)/1800) * 40 
        self.x += self.velx * delta_time
        self.y += self.vely * delta_time

        self.rect.center = (self.x, self.y)

        self.image.fill((0,0,0))
        self.idle_sequence.update(self.image,(0,0))
        
        # Add code to figure out the normalized differences between this enemy and the player
        player_x, player_y = player_position
        player_velx, player_vely = player_velocity
        
        x_difference = (self.x - player_x) / constants.game_width
        y_difference = (self.y - player_y) / constants.window_height
        x_velocity_difference = (self.velx - player_velx) / 60
        y_velocity_difference = (self.vely - player_vely) / 60
        
        player_variables = (x_difference, y_difference, x_velocity_difference, y_velocity_difference)
        #
        
        if not(self.can_fire):
            self.cooldown_timer += delta_time
            if self.cooldown_timer>self.shot_cooldown:
                self.can_fire = True
                self.cooldown_timer = 0
        
        # Have the brain make the decision whether or not to fire based on the player variables
        if self.can_fire:
            # If the computer is in training mode, every frame there is a 1 in 20 chance the enemy will fire
            # We're also going to pass the brain to the bullet, so that when the bullet misses it can record that miss to the brain
            if training_mode:
                if (randrange(0, 100) < 5):
                    bullet = Bullet(self.x,self.y+96,constants.RED,self.bullets, self.brain)
                    self.brain.add_shot(bullet, player_variables)
                    self.can_fire = False
            else:
                if (self.brain.fire_decision(player_variables)):
                    bullet = Bullet(self.x,self.y+96,constants.RED,self.bullets, self.brain)
                    self.brain.add_shot(bullet, player_variables)
                    self.can_fire = False
            #
                