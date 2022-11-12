import pygame

from dino_runner.components import text_utils
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.bird_manager import BirdManager
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import \
    PlayerHeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.power_ups.hammer_manager import HammerManager
from dino_runner.utils.constants import (BG, FPS, ICON, SCREEN_HEIGHT,
                                         SCREEN_WIDTH, TITLE, RUNNING)
from dino_runner.components.elementos.cloud import Cloud
background = pygame.image.load(r"C:\Users\hp\Desktop\proyecto\RE-DinoRunner-CO-Grupo2J\dino_runner\FONDO.jpg")

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.player_heart_manager = PlayerHeartManager()
        self.bird_manager = BirdManager()
        self.power_up_manager = PowerUpManager()
        self.hammer_manager = HammerManager()
        self.cloud = Cloud()
        pygame.mixer.music.load(r'C:\Users\hp\Desktop\proyecto\RE-DinoRunner-CO-Grupo2J\dino_runner\intro.mp3')
        pygame.mixer.music.play()
    

        
        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacles()
        self.player_heart_manager.reset_hearts()
        self.power_up_manager.reset_power_ups(self.points)

        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
    def events(self):
        user_input = pygame.key.get_pressed()
        self.player.event(user_input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
        self.screen.fill((255, 255, 255))

    def update(self):
        self.player.update()
        self.obstacle_manager.update(self)
        self.bird_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.hammer_manager.update(self.points, self.game_speed, self.player)
        self.cloud.update(self)
        self.score

    def draw(self):
        self.score()
        self.clock.tick(FPS)
        self.screen.blit(background, [-100, -170])
        self.draw_background()
        self.power_up_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        
        self.hammer_manager.draw(self.screen)
        self.cloud.draw(self.screen)
        self.bird_manager.draw(self.screen)
        self.score()
        
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg)) # (x,y)
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to Start')
            self.screen.blit(text, text_rect)
        elif self.death_count > 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to Restart')

            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.points),
                                                                height=half_screen_height + 50)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count),
                                                                height=half_screen_height + 100)
            self.screen.blit(score, score_rect)

            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)
            
        self.screen.blit(RUNNING[0], (half_screen_width - 20, half_screen_height - 140))
    def show_menu(self):
        self.running = True
        # Print the background to white
        fondo = pygame.image.load(r"C:\Users\hp\Desktop\proyecto\RE-DinoRunner-CO-Grupo2J\dino_runner\FONDO.jpg")
        self.screen.blit(fondo, [0, 0])
        # Print the element that are in the menu
        self.print_menu_elements()
        # The view of the game is updated
        pygame.display.update()
        self.handle_key_events_on_menu()

    def score(self):
        self.points += 1
        # aumentando la complejidad del juego cada q llegue a 100pts
        if self.points % 100 == 0:
            self.game_speed += 1

        # Imprimimos el score
        text, text_rect = text_utils.get_score_element(self.points)
        self.player.check_visibility(self.screen)
        self.screen.blit(text, text_rect)
