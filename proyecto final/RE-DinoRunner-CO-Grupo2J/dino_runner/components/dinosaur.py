import pygame
from dino_runner.utils.constants import (DEFAULT_TYPE, DUCKING, DUCKING_HAMMER,
                                         DUCKING_SHIELD, HAMMER_TYPE, JUMPING,
                                         JUMPING_HAMMER, JUMPING_SHIELD,
                                         RUNNING, RUNNING_HAMMER,
                                         RUNNING_SHIELD, SHIELD_TYPE)


class Dinosaur():
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    def __init__(self):
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.time_up = 0
        self.sound_jump = pygame.mixer.Sound(r'C:\Users\hp\Desktop\proyecto\RE-DinoRunner-CO-Grupo2J\dino_runner\jump.wav')
        self.setup_state_boolean()
        

    def setup_state_boolean(self):
        self.has_powerup = False 
        self.shield =False 
        self.show_text=False 
        self.shield_time_up=0   

    # Agregar el evento de agacharse para el dino -> pygame.K_DOWN
    def event(self, user_input):
        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        
            
        elif user_input[pygame.K_UP] and not self.dino_duck:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.sound_jump.play()
            
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
       
    def update(self):
        # self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()
        if self.dino_duck:
            self.duck()
        
        if self.step_index >= 10:
            self.step_index = 0
    def run(self):
        self.image = self.run_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img[self.type]
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
    def duck(self):
        self.image = self.duck_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def check_visibility(self,screen):
        if self.shield:
            time_to_show = round( (self.shield_time_up - pygame.time.get_ticks())/1000,2 )
            if(time_to_show>=0):
                fond = pygame.font.Font('freesansbold.ttf',18)
                text = fond.render(f'shield enable for {time_to_show}',True,(0,0,0))
                textRect = text.get_rect()
                textRect.center = (500,40)
                screen.blit(text,textRect)
            else:
                self.shield = False 
                self.update_to_default(SHIELD_TYPE)

    def update_to_default(self, current_type):
        if(self.type == current_type):
            self.type = DEFAULT_TYPE
            
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
    




