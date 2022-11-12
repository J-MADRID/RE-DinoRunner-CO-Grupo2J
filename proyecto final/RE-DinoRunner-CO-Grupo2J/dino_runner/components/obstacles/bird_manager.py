from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import BIRD
import pygame

class BirdManager:

    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            new_obstacle = Bird(BIRD)
            self.obstacles.append(new_obstacle)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
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
                    break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)