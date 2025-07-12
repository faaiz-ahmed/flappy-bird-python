import random
import sys
import pygame
from pygame.locals import *
import os

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'assets/sprites/bird.png'
BACKGROUND = 'assets/sprites/background.png'
PIPE = 'assets/sprites/pipe.png'
HIGH_SCORE_FILE = 'highscore.txt'

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def load_font(font_name, size):
    """Load font with fallback to system font if custom font fails"""
    try:
        return pygame.font.Font(resource_path(f'assets/fonts/{font_name}'), size)
    except:
        return pygame.font.SysFont('Arial', size)

def load_high_score():
    """Load high score from a file."""
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    """Save high score to a file."""
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

def draw_button(text, x, y, size=24, color=(255, 255, 255), shadow_color=(0, 0, 0)):
    """Draw a button with shadow effect and specified text properties."""
    font = load_font('Raleway-SemiBold.ttf', size)
    button_surface = font.render(text, True, shadow_color)
    button_rect = button_surface.get_rect(center=(x + 2, y + 2))
    SCREEN.blit(button_surface, button_rect)

    button_surface = font.render(text, True, color)
    button_rect = button_surface.get_rect(center=(x, y))
    SCREEN.blit(button_surface, button_rect)
    return button_rect

def main_menu():
    """Display the main menu."""
    while True:
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (SCREENWIDTH / 5, (SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2))
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))

        draw_button("Flappy Bird", SCREENWIDTH / 2, SCREENHEIGHT / 3, size=36, color=(255, 215, 0))
        play_button = draw_button("Play", SCREENWIDTH / 2, SCREENHEIGHT / 2 - 30, size=30, color=(0, 255, 0))
        exit_button = draw_button("Exit", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 30, size=30, color=(0, 255, 0))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_button.collidepoint(mouse_x, mouse_y):
                    difficulty_selection()
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def difficulty_selection():
    """Display the difficulty selection menu."""
    selected_difficulty = "easy"
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if easy_button.collidepoint(mouse_x, mouse_y):
                    selected_difficulty = "easy"
                    welcomeScreen()
                    main_game(selected_difficulty)
                    return
                elif medium_button.collidepoint(mouse_x, mouse_y):
                    selected_difficulty = "medium"
                    welcomeScreen()
                    main_game(selected_difficulty)
                    return
                elif hard_button.collidepoint(mouse_x, mouse_y):
                    selected_difficulty = "hard"
                    welcomeScreen()
                    main_game(selected_difficulty)
                    return
                elif back_button.collidepoint(mouse_x, mouse_y):
                    return  
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        draw_button("Select Difficulty", SCREENWIDTH / 2, SCREENHEIGHT / 2 - 50, size=30, color=(0, 255, 0))
        easy_button = draw_button("Easy", SCREENWIDTH / 2, SCREENHEIGHT / 2, size=28, color=(0, 255, 0))
        medium_button = draw_button("Medium", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 40, size=28, color=(0, 255, 0))
        hard_button = draw_button("Hard", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 80, size=28, color=(0, 255, 0))
        back_button = draw_button("Back", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 130, size=28, color=(0, 255, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def display_high_score(high_score):
    """Display high score on the screen."""
    my_high_digits = [int(x) for x in list(str(high_score))]
    high_width = sum(GAME_SPRITES['numbers'][digit].get_width() for digit in my_high_digits)
    high_Xoffset = (SCREENWIDTH - high_width) - 10

    hs_text = load_font('Raleway-SemiBold.ttf', 24).render('HS:', True, (255, 255, 255))
    SCREEN.blit(hs_text, (high_Xoffset - hs_text.get_width() - 5, SCREENHEIGHT * 0.02))

    for digit in my_high_digits:
        high_score_surface = pygame.transform.scale(GAME_SPRITES['numbers'][digit], (20, 30))
        SCREEN.blit(high_score_surface, (high_Xoffset, SCREENHEIGHT * 0.02))
        high_Xoffset += high_score_surface.get_width()

def welcomeScreen():
    """Display the welcome screen before the game starts."""
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    tip = draw_button("Press SPACE/tap/upkey to start/flap", SCREENWIDTH / 2, SCREENHEIGHT - 50, size=16, color=(255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or (event.type == MOUSEBUTTONDOWN):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        draw_button("Press SPACE/tap/upkey to start/flap", SCREENWIDTH / 2, SCREENHEIGHT - 50, size=16, color=(255, 255, 255))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def get_random_pipe(difficulty):
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3 if difficulty == "easy" else (SCREENHEIGHT / 5 if difficulty == "medium" else SCREENHEIGHT / 7)
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH + 10
    y1 = pipe_height - y2 + offset
    return [{'x': pipe_x, 'y': -y1}, {'x': pipe_x, 'y': y2}]

def main_game(difficulty):
    score = 0
    high_score = load_high_score()
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0
    upperpipes = []
    lowerpipes = []
    new_pipe1 = get_random_pipe(difficulty)
    new_pipe2 = get_random_pipe(difficulty)

    upperpipes.extend([{'x': SCREENWIDTH + 200, 'y': new_pipe1[0]['y']},
                       {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe2[0]['y']}])
    lowerpipes.extend([{'x': SCREENWIDTH + 200, 'y': new_pipe1[1]['y']},
                       {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe2[1]['y']}])

    if difficulty == "easy":
        pipe_vel_x = -4
    elif difficulty == "medium":
        pipe_vel_x = -5
    else:
        pipe_vel_x = -6
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1
    player_flap_acc = -8
    player_flapped = False
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    paused = not paused
                    if paused:
                        GAME_SOUNDS['swoosh'].play()
                elif (event.key == K_SPACE or event.key == K_UP) and not paused:
                    if playery > 0:
                        player_vel_y = player_flap_acc
                        player_flapped = True
                        GAME_SOUNDS['wing'].play()
            elif event.type == MOUSEBUTTONDOWN and not paused:
                if playery > 0:
                    player_vel_y = player_flap_acc
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()
        if paused:
            draw_button("PAUSED", SCREENWIDTH / 2, SCREENHEIGHT / 2, size=36, color=(255, 255, 255))
            draw_button("Press P to resume", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 40, size=20, color=(255, 255, 255))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue
        if is_collide(playerx, playery, upperpipes, lowerpipes):
            save_high_score(max(score, high_score))
            game_over_menu(score, high_score,difficulty)
            return 

        playermidpoint = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperpipes:
            pipemidpoint = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipemidpoint <= playermidpoint <= pipemidpoint + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        playery = playery + min(player_vel_y, GROUNDY - playery - player_height)

        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipe_vel_x
            lowerpipe['x'] += pipe_vel_x

        if 0 < upperpipes[0]['x'] < 5:
            new_pipe = get_random_pipe(difficulty)
            upperpipes.append(new_pipe[0])
            lowerpipes.append(new_pipe[1])

        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        my_digits = [int(x) for x in list(str(score))]
        width = sum(GAME_SPRITES['numbers'][digit].get_width() for digit in my_digits)
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in my_digits:
            score_surface = pygame.transform.scale(GAME_SPRITES['numbers'][digit], (20, 30))
            SCREEN.blit(score_surface, (Xoffset, SCREENHEIGHT * 0.02))
            Xoffset += score_surface.get_width()

        my_high_digits = [int(x) for x in list(str(high_score))]
        high_width = sum(GAME_SPRITES['numbers'][digit].get_width() for digit in my_high_digits)
        high_Xoffset = (SCREENWIDTH - high_width) - 10

        hs_text = pygame.font.SysFont('Arial', 24).render('HS:', True, (255, 255, 255))
        SCREEN.blit(hs_text, (high_Xoffset - hs_text.get_width() - 5, SCREENHEIGHT * 0.02))

        for digit in my_high_digits:
            high_score_surface = pygame.transform.scale(GAME_SPRITES['numbers'][digit], (20, 30))
            SCREEN.blit(high_score_surface, (high_Xoffset, SCREENHEIGHT * 0.02))
            high_Xoffset += high_score_surface.get_width()
        hint_font = load_font('Raleway-SemiBold.ttf', 14)
        hint_text = hint_font.render("P to pause", True, (255, 255, 255))
        SCREEN.blit(hint_text, (5, 5))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def game_over_menu(score, high_score, difficulty):
    """Display the game over menu with an option to restart or exit."""
    new_high_score = score > high_score
    if new_high_score:
        high_score = score
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    main_game(difficulty)
                    return
                elif menu_button.collidepoint(mouse_x, mouse_y):
                    return
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        
        draw_button("Game Over", SCREENWIDTH / 2, SCREENHEIGHT / 2 - 70, size=30, color=(255, 0, 0))
        draw_button(f"Score: {score}", SCREENWIDTH / 2, SCREENHEIGHT / 2 - 30, size=24, color=(255, 255, 255))
        
        if new_high_score:
            draw_button("New High Score!", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 0, size=24, color=(255, 215, 0))
        
        restart_button = draw_button("Restart", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 40, size=24, color=(0, 255, 0))
        menu_button = draw_button("Main Menu", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 80, size=24, color=(0, 200, 255))
        exit_button = draw_button("Exit", SCREENWIDTH / 2, SCREENHEIGHT / 2 + 120, size=24, color=(255, 50, 50))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def is_collide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipe_height = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipe_height + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers'] = tuple(
        pygame.image.load(f'assets/sprites/{i}.png').convert_alpha() for i in range(10)
    )
    GAME_SPRITES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()

    main_menu()