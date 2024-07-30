import random
import sys
from time import sleep
from pyvidplayer2 import Video
import pygame
from pygame.locals import *

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.FPS = 32
        self.SCREENWIDTH = pygame.display.Info().current_w
        self.SCREENHEIGHT = pygame.display.Info().current_h
        self.GROUNDY = self.SCREENHEIGHT * 0.7
        self.SCREEN = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT), pygame.FULLSCREEN)
        self.GAME_SPRITES = {}
        self.GAME_SOUNDS = {}
        self.PLAYER = 'gallery/sprites/bird.png'
        self.BACKGROUND = 'gallery/sprites/background.png'
        self.PIPE = 'gallery/sprites/pipe.png'
        self.FPSCLOCK = None
        self.BACKGROUNDS = [
            'gallery/sprites/background_day.png',
            'gallery/sprites/background_night.png',
            'gallery/sprites/background_desert.png'
        ]
        self.selected_background = self.BACKGROUNDS[0]
        self.VIDEO_PATH = 'gallery/video/intro.avi'


    def load_assets(self):
        # Loading the images
        score_width = self.SCREENWIDTH * 0.07
        score_height = self.SCREENHEIGHT * 0.21
        self.GAME_SPRITES['numbers'] = (
            pygame.transform.scale(pygame.image.load('gallery/sprites/0.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/1.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/2.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/3.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/4.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/5.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/6.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/7.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/8.png').convert_alpha(), (score_width, score_height)),
            pygame.transform.scale(pygame.image.load('gallery/sprites/9.png').convert_alpha(), (score_width, score_height)),
        )
        self.GAME_SPRITES['background'] = pygame.image.load(self.selected_background).convert_alpha()
        self.GAME_SPRITES['player'] = pygame.image.load(self.PLAYER).convert_alpha()
        self.GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
        pipe_width = self.SCREENWIDTH * 0.04
        pipe_height = self.SCREENHEIGHT * 0.46
        self.GAME_SPRITES['pipe'] = (
            pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.PIPE).convert_alpha(), (pipe_width, pipe_height)), 180),
            pygame.transform.scale(pygame.image.load(self.PIPE).convert_alpha(), (pipe_width, pipe_height))
        )

        # Scaling the loaded images
        self.GAME_SPRITES['background'] = pygame.transform.scale(self.GAME_SPRITES['background'], (self.SCREENWIDTH, self.SCREENHEIGHT))
        self.GAME_SPRITES['player'] = pygame.transform.scale(self.GAME_SPRITES['player'], (self.SCREENWIDTH * 0.05, self.SCREENHEIGHT * 0.07))
        self.GAME_SPRITES['base'] = pygame.transform.scale(self.GAME_SPRITES['base'], (self.SCREENWIDTH, self.SCREENHEIGHT * 0.3))

        # Game Sounds
        self.GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        self.GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        self.GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
        self.GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        self.GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
        self.GAME_SOUNDS['option-switch'] = pygame.mixer.Sound('gallery/audio/option-switch.wav')
        self.GAME_SOUNDS['option-selected'] = pygame.mixer.Sound('gallery/audio/option-selected.wav')

    def  render_text(self, text, font, color, position):
        """
        Renders text onto the screen.
        """
        text_surface = font.render(text, True, color)
        self.SCREEN.blit(text_surface, position)

    def choose_background_screen(self):
        """
        Shows the background selection screen
        """
        self.SCREEN.fill((0, 0, 0))

        background_rects = []
        padding = 20
        box_width = (self.SCREENWIDTH - (len(self.BACKGROUNDS) + 1) * padding) / len(self.BACKGROUNDS)
        box_height = self.SCREENHEIGHT * 0.4
        y_position = (self.SCREENHEIGHT - (box_height/1.5)) / 2

        # Render the title
        title_text = "Choose Background"
        title_color = (255, 255, 255)  # White color
        title_font = pygame.font.Font(None, 100)
        title_position = (self.SCREENWIDTH // 2 - title_font.size(title_text)[0] // 2, (y_position // 2) - 30)
        self.render_text(title_text, title_font, title_color, title_position)

        subtitle_text = "Press Esc to exit"
        subtitle_color = (235, 235, 23)
        subtitle_font = pygame.font.Font(None, 50)
        subtitle_position = (self.SCREENWIDTH // 2 - subtitle_font.size(subtitle_text)[0] // 2, (y_position // 2) + 50)
        self.render_text(subtitle_text, subtitle_font, subtitle_color, subtitle_position)

        for i, bg in enumerate(self.BACKGROUNDS):
            x_position = padding + (box_width + padding) * i
            bg_image = pygame.image.load(bg).convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (box_width, box_height))
            background_rects.append((bg_image, pygame.Rect(x_position, y_position, box_width, box_height)))

        selected_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_LEFT):
                    self.GAME_SOUNDS['option-switch'].play()
                    selected_index = (selected_index - 1) % len(self.BACKGROUNDS)
                elif event.type == KEYDOWN and (event.key == K_RIGHT):
                    self.GAME_SOUNDS['option-switch'].play()
                    selected_index = (selected_index + 1) % len(self.BACKGROUNDS)
                elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
                    self.GAME_SOUNDS['option-selected'].play()
                    self.selected_background = self.BACKGROUNDS[selected_index]
                    self.load_assets()
                    return

            for i, (image, rect) in enumerate(background_rects):
                self.SCREEN.blit(image, rect.topleft)
                if i == selected_index:
                    pygame.draw.rect(self.SCREEN, (255, 0, 0), rect, 5)

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)


    def welcome_screen(self):
        '''
        Shows welcome images on the screen
        '''
        playerx = int(self.SCREENWIDTH / 5)
        playery = int(self.SCREENHEIGHT - self.GAME_SPRITES['player'].get_height()) / 2
        basex = 0
        # background_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                
                self.SCREEN.blit(self.GAME_SPRITES['background'], (0, 0))
                self.SCREEN.blit(self.GAME_SPRITES['player'], (playerx, playery))
                self.SCREEN.blit(self.GAME_SPRITES['base'], (basex, self.GROUNDY))
                pygame.display.update()
                self.FPSCLOCK.tick(self.FPS)

    def play_intro_video(self):
        vid = Video(self.VIDEO_PATH)

        while vid.active:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    vid.close()
            if vid.draw(self.SCREEN, (-200, -80), force_draw=False):
                pygame.display.update()
        vid.close()

    def main_game(self):
        score = 0
        playerx = int(self.SCREENWIDTH / 5)
        playery = int(self.SCREENHEIGHT / 2)
        basex = 0

        # Create two pipes for blitting on screen
        newPipe1 = self.get_random_pipe()
        newPipe2 = self.get_random_pipe()
        newPipe3 = self.get_random_pipe()

        # my list of upper pipes
        upperPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        # my list of lower pipes
        lowerPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4
        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8  # Velocity while flapping
        playerFlapped = False  # It is only true when the bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        self.GAME_SOUNDS['wing'].play()

            crashTest = self.is_collide(playerx, playery, upperPipes, lowerPipes)  # This function will return true if player crashed
            if crashTest:
                return

            # Check for score
            playerMidPos = playerx + (self.GAME_SPRITES['player'].get_width() / 2)
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + (self.GAME_SPRITES['pipe'][0].get_width() / 2)
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f"Your Score is {score}")
                    self.GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = self.GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, self.GROUNDY - playery - playerHeight)

            # Move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = self.get_random_pipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # If the pipe is out of screen then remove it
            if upperPipes[0]['x'] < -self.GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # Let's blit our sprites now
            self.SCREEN.blit(self.GAME_SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(self.GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                self.SCREEN.blit(self.GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            self.SCREEN.blit(self.GAME_SPRITES['base'], (basex, self.GROUNDY))
            self.SCREEN.blit(self.GAME_SPRITES['player'], (playerx, playery))

            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += self.GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (self.SCREENWIDTH - width) / 2

            for digit in myDigits:
                self.SCREEN.blit(self.GAME_SPRITES['numbers'][digit], (Xoffset, self.SCREENHEIGHT * 0.12))
                Xoffset += self.GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    def is_collide(self, playerx, playery, upperPipes, lowerPipes):
        if playery > self.GROUNDY - (self.GAME_SPRITES['player'].get_height() + 1) or playery < 0:
            self.GAME_SOUNDS['hit'].play()
            return True

        for pipe in upperPipes:
            pipeHeight = self.GAME_SPRITES['pipe'][0].get_height()
            if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width():
                self.GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + self.GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width():
                self.GAME_SOUNDS['hit'].play()
                return True

        return False

    def get_random_pipe(self):
        """
        Generate positions of two pipes(one bottom straight and one top rotated) for blitting on the screen
        """
        pipeHeight = self.GAME_SPRITES['pipe'][0].get_height()
        offset = self.SCREENHEIGHT / 3
        y2 = offset + random.randrange(0, int(self.SCREENHEIGHT - self.GAME_SPRITES['base'].get_height() - 1.2 * offset))
        pipeX = self.SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1},  # upper Pipe
            {'x': pipeX, 'y': y2}  # lower Pipe
        ]
        return pipe

    def run(self):
        pygame.init()  # Initialize all pygame's modules
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('Flappy Bird by CoderBairagi')
        pygame.display.toggle_fullscreen()
        pygame.display.toggle_fullscreen()
        self.load_assets()
        self.play_intro_video()

        while True:
            self.choose_background_screen() # Choose background before starting the game
            self.welcome_screen()  # Shows welcome screen to the user until he presses a button
            self.main_game()  # This is the main game function


if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
