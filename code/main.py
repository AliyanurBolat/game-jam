from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from player import Player
from ui import UI

pygame.mixer.init()
bg_music = pygame.mixer.Sound(join('', 'audio', 'siren.wav'))
siren = pygame.mixer.Sound(join('', 'audio', 'bg.mp3'))
bg_music.play(-1)
siren.play(-1)
pygame.mixer.pause()

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = '#92a9ce'
        self.text_surf = pygame.font.Font(None, 36).render(text, True, 'black')
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Slider():
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, text):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.knob_rect = pygame.Rect(x + (width - 20) * ((initial_value - min_value) / (max_value - min_value)), y - 10, 20, height + 20)
        self.dragging = False
        self.text_surf = pygame.font.Font(None, 36).render(text, True, 'black')
        

    def draw(self, screen):
        pygame.draw.rect(screen, 'lightgray', self.rect)
        pygame.draw.rect(screen, "darkgray", self.knob_rect)
        screen.blit(self.text_surf, self.text_surf.get_rect(center=self.rect.center))
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_rect.x = min(max(self.rect.x, event.pos[0] - 10), self.rect.right - 10)
            self.value = self.min_value + (self.knob_rect.x - self.rect.x) / (self.rect.width - 20) * (self.max_value - self.min_value)
            bg_music.set_volume(self.value)
            siren.set_volume(self.value)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.in_menu = True
        self.in_settings = False
        self.in_game_settings = False
        self.in_pause = False
        self.in_volume = False
        self.text_surf = pygame.font.Font(None, 36)
        self.pause_text_surf = self.text_surf.render("Paused", True, 'black')
        self.pause_text_rect = self.pause_text_surf.get_rect()
        self.pause_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.fail_surf = self.level_frames['fail']
        self.win_surf = self.level_frames['win']
        
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('', 'data', 'levels', 'kbtu_omni.tmx'))
            }

        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        self.buttons = [
            Button("Play", 170, 100, 300, 50, self.start_game),
            Button("Settings", 170, 200, 300, 50, self.open_settings),
            Button("Exit", 170, 300, 300, 50, self.exit_game)
        ]
        self.settings_buttons = [
            Button("Volume", 170, 100, 300, 50, self.settings_volume),
            Button("Back to menu", 170, 200, 300, 50, self.exit_settings),
        ]
        self.game_buttons = [
            Button("Menu", 1000, 50, 250, 50, self.open_game_settings),
        ]
        self.game_settings_buttons = [
            Button("Back to game", 170, 100, 300, 50, self.exit_settings),
            Button("Restart", 170, 200, 300, 50, self.restart_game),
            Button("Volume", 170, 300, 300, 50, self.settings_volume),
            Button("Exit", 170, 400, 300, 50, self.exit_game)
        ]
        self.volume_settings_buttons = [
            Button("Disable music", 170, 100, 300, 50, self.disable_music),
            Button("Enable music", 170, 200, 300, 50, self.enable_music),
            Button("Back", 170, 400, 300, 50, self.exit_volume),
        ]
        self.game_over_buttons = [
            Button("Restart", 170, 100, 300, 50, self.restart_game),
            Button("Exit", 170, 200, 300, 50, self.exit_game)
        ]

        self.volume_slider = Slider(170, 300, 300, 20, 0.0, 1.0, pygame.mixer.music.get_volume(), "Music volume")

    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('', 'graphics', 'level', 'flag'),
            'floor_spike': import_folder('', 'graphics', 'enemies', 'floor_spikes'),
            'palms' : import_sub_folders('', 'graphics', 'level', 'palms'),
            'player': import_sub_folders('', 'graphics', 'player'), 
            'helicopter': import_folder('', 'graphics', 'level', 'helicopter'),
            'tooth': import_folder('', 'graphics', 'enemies', 'tooth', 'run'),
            'items': import_sub_folders('', 'graphics', 'items'),
            'particle': import_folder('', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('', 'graphics', 'level', 'clouds', 'large_cloud'),
            'crowd': import_folder('', 'graphics', 'enemies', 'crowd'),
            'chandelier': import_sub_folders('', 'graphics', 'enemies', 'chandelier'),
            'fail': import_image('', 'graphics', 'fail', '0'), 
            'win': import_image('', 'graphics', 'win', 'win'), 
        }

        self.font = pygame.font.Font(join('','graphics','ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart' : import_folder('', 'graphics', 'ui', 'heart'),
            'coin': import_image('', 'graphics', 'ui', 'coin'),
            'jacket': import_image('', 'graphics', 'ui', 'jacket'),
            'backpack': import_image('', 'graphics', 'ui', 'backpack'),
        }
        
        self.audio_files = {
            'coin': pygame.mixer.Sound(join('', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('', 'audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('', 'audio', 'damage.wav')),
        }
        
    def run(self):
        while True:
            while self.in_menu:
                while self.in_settings:
                    if not self.in_volume:
                        # settings
                        dt = self.clock.tick() / 1000
                        self.display_surface.fill('#ddc6a1')

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    self.exit_settings()
                            for button in self.settings_buttons:
                                button.handle_event(event)

                        for button in self.settings_buttons:
                            button.draw(self.display_surface)
                    
                    # volume settings
                    else:
                        dt = self.clock.tick() / 1000
                        self.display_surface.fill('#ddc6a1')

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    self.exit_settings()
                            for button in self.volume_settings_buttons:
                                button.handle_event(event)
                            
                            self.volume_slider.handle_event(event)

                        for button in self.volume_settings_buttons:
                            button.draw(self.display_surface)
                        self.volume_slider.draw(self.display_surface)
                        
                    pygame.display.update()

                # menu
                dt = self.clock.tick() / 1000
                self.display_surface.fill('#ddc6a1')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.exit_game()
                    for button in self.buttons:
                        button.handle_event(event)

                for button in self.buttons:
                    button.draw(self.display_surface)
                pygame.display.update()

            # game
            if not self.in_pause:
                dt = self.clock.tick() / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.in_pause = not self.in_pause
                        if event.key == pygame.K_p:
                            self.exit_game()
                    for button in self.game_buttons:
                        button.handle_event(event)
                
                self.current_stage.run(dt)
                self.ui.update(dt)
                if not self.in_game_settings:
                    pygame.mixer.unpause()
                for button in self.game_buttons:
                    button.draw(self.display_surface)
                
                # game over
                if self.data.health <= 0:
                    pygame.mixer.stop()
                    self.display_surface.blit(self.fail_surf, self.fail_surf.get_frect())
                    dt = self.clock.tick() / 1000
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.exit_game()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.exit_game()
                        for button in self.game_over_buttons:
                            button.handle_event(event)
                    for button in self.game_over_buttons:
                        button.draw(self.display_surface)
                if self.data.win:
                    pygame.mixer.stop()
                    self.display_surface.blit(self.win_surf, self.win_surf.get_frect())
                    dt = self.clock.tick() / 1000
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.exit_game()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.exit_game()
                        for button in self.game_over_buttons:
                            button.handle_event(event)
                    for button in self.game_over_buttons:
                        button.draw(self.display_surface)

                # in-game settings
                if self.in_game_settings:
                    dt = self.clock.tick() / 1000
                    self.display_surface.fill('#ddc6a1')

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.exit_settings()
                        for button in self.game_settings_buttons:
                            button.handle_event(event)
                    pygame.mixer.pause()
                    for button in self.game_settings_buttons:
                        button.draw(self.display_surface)
                pygame.display.update()

            else:
                # pause
                pygame.mixer.pause()
                self.display_surface.blit(self.pause_text_surf, self.pause_text_rect)
                dt = self.clock.tick() / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.in_pause = not self.in_pause
                        if event.key == pygame.K_p:
                            self.exit_game()
                    for button in self.game_buttons:
                        button.handle_event(event)
                    for button in self.game_settings_buttons:
                        button.handle_event(event)
                # in-game settings
                if self.in_game_settings:
                    dt = self.clock.tick() / 1000
                    self.display_surface.fill('#ddc6a1')

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.exit_settings()
                        for button in self.game_settings_buttons:
                            button.handle_event(event)

                    for button in self.game_settings_buttons:
                        button.draw(self.display_surface)
            pygame.display.update()          
        
    def start_game(self):
        self.in_menu = False
    
    def open_settings(self):
        self.in_settings = True
    
    def open_game_settings(self):
        if self.in_pause:
            # self.in_pause = False
            self.in_game_settings = True
        else:
            self.in_game_settings = True

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def exit_settings(self):
        if self.in_pause == True:
            self.in_menu, self.in_game_settings, self.in_pause, self.in_volume = False, False, False, False
        if self.in_settings == True:
            self.in_settings = False
        if self.in_game_settings:
            self.in_game_settings = False
            self.in_menu = False
    
    def restart_game(self):
        self.current_stage.reset()
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        self.in_menu, self.in_game_settings, self.in_pause = False, False, False
        pygame.mixer.stop()
        bg_music.play(-1)
        siren.play(-1)
        if self.data.win:
            self.current_stage.reset()
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
            self.in_menu, self.in_game_settings, self.in_pause = False, False, False
            pygame.mixer.stop()
            bg_music.play(-1)
            siren.play(-1)
            self.data.win = False
        
    def disable_music(self):
        pygame.mixer.stop()

    def enable_music(self):
        bg_music.play(-1)
        siren.play(-1)
        pygame.mixer.pause()

    def settings_volume(self):
        if self.in_game_settings:
            self.in_menu = True
            self.in_settings = True
            self.in_volume = True
        else:
            self.in_volume = True

    def exit_volume(self):
        self.in_volume = False

if __name__ == '__main__':
    game = Game()
    game.run()