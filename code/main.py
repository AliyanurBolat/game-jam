from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data

from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('', 'data', 'levels', 'kbtu_omni.tmx'))
            }

        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)

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
            dt = self.clock.tick() / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.current_stage.run(dt)
            self.ui.update(dt)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()