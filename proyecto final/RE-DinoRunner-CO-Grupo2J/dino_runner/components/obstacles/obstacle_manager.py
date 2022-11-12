import random
import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import (LARGE_CACTUS, SMALL_CACTUS)
class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    def update(self, game):
        if len(self.obstacles) == 0:
            cactus_size = random.randint(0,1)
            if cactus_size == 0:
                largeCactus = Cactus(LARGE_CACTUS)
                largeCactus.rect.y -= 30
                self.obstacles.append(largeCactus)
            else:
                self.obstacles.append(Cactus(SMALL_CACTUS))
        

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect) and game.player.shield == False:
                pygame.time.delay(100)
                game.player_heart_manager.reduce_heart()
        


                if game.player_heart_manager.heart_count > 0:
                    game.player.has_lives = True
                    self.obstacles.pop()
                    start_time = pygame.time.get_ticks()
                    game.player.time_up = start_time + 1000
                else:
                    pygame.time.delay(500)
                    self.obstacles.remove(obstacle)
                    game.playing = False
                    game.player.has_lives = False
                    game.death_count += 1
                    break
                        
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
        self.obstacles = []