window_width = 1280
window_height = 720
game_width = int(window_width/2)

frames_per_second = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

ship_acceleration = 100
enemy_move_speed = 16
enemy_spawn_rate = 8

#How fast the bullets will move
player_bullet_speed = 320
enemy_bullet_speed = 160
#Enemy bullets will move down in the y axis
enemy_bullet_direction = (0, 1)
#Player bullets will move up in the y axis
player_bullet_direction = (0, -1)
#Will need to wait this long in seconds before firing again
enemy_shot_cooldown = 0.5
player_shot_cooldown = 0.3

# New Constants
score_for_damage = 50
starting_health = 100
player_bullet_damage = 10
# Here, the enemy will do less damage than the player, but feel free to change it if you want a bigger challenge
enemy_bullet_damage = 5
#