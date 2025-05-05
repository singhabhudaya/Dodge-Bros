import pygame  
import random

pygame.init()
WIDTH, HEIGHT = 1152, 648
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Bros")

# Music and sound setup
pygame.mixer.music.load("Assets/Theme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

orb_sound = pygame.mixer.Sound("Assets/Black_Orb.wav")
orb_sound.set_volume(0.7)

# Load assets
bg = pygame.transform.scale(pygame.image.load("Assets/Background.png"), (WIDTH, HEIGHT))
p1_img = pygame.transform.scale(pygame.image.load("Assets/Player1.png"), (60, 80))
p2_img = pygame.transform.scale(pygame.image.load("Assets/Player2.png"), (60, 80))
fireball_img = pygame.transform.scale(pygame.image.load("Assets/fireball.png"), (32, 32))
dragon_img = pygame.transform.scale(pygame.image.load("Assets/Enemy.png"), (100, 100))
heart_img = pygame.transform.scale(pygame.image.load("Assets/heart.png"), (32, 32))
black_orb_img = pygame.transform.scale(pygame.image.load("Assets/Black_orb.png"), (32, 32))

font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

def reset_game():
    return {
        'p1': pygame.Rect(100, HEIGHT - 135, 60, 80),
        'p2': pygame.Rect(WIDTH - 160, HEIGHT - 135, 60, 80),
        'p1_vel': 0,
        'p2_vel': 0,
        'p1_lives': 3,
        'p2_lives': 3,
        'dragon_x': WIDTH // 2 - 50,
        'dragon_y': 20,
        'dragon_speed': 3,
        'dragon_dir': 1,
        'fireballs': [],
        'black_orbs': [],
        'orb_count': 0,
        'massive_orb': None,
        'game_over': False,
        'victory': False,
        'miss_timer': -9999,
    }

game = reset_game()
GROUND_Y = HEIGHT - 135
orb_target = 30

def draw_button(text):
    button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50)
    pygame.draw.rect(win, (30, 30, 30), button, border_radius=8)
    pygame.draw.rect(win, (255, 255, 255), button, 2, border_radius=8)
    label = font.render(text, True, (255, 255, 255))
    label_pos = label.get_rect(center=button.center)
    win.blit(label, label_pos)
    return button

running = True
while running:
    clock.tick(60)
    win.blit(bg, (0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game['game_over'] or game['victory']):
                game = reset_game()
            if event.key == pygame.K_g and game['orb_count'] >= orb_target and not game['massive_orb']:
                game['massive_orb'] = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 100, 60, 60)
                orb_sound.play()

        # Mouse replay button
        if (game['game_over'] or game['victory']) and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_button("Replay").collidepoint(event.pos):
                game = reset_game()

    keys = pygame.key.get_pressed()

    if not game['game_over'] and not game['victory']:
        # Player controls
        if keys[pygame.K_a] and game['p1'].left > 0 and game['p1_lives'] > 0:
            game['p1'].x -= 6
        if keys[pygame.K_d] and game['p1'].right < WIDTH and game['p1_lives'] > 0:
            game['p1'].x += 6
        if keys[pygame.K_w] and game['p1'].bottom >= GROUND_Y + 80 and game['p1_lives'] > 0:
            game['p1_vel'] = -18

        if keys[pygame.K_LEFT] and game['p2'].left > 0 and game['p2_lives'] > 0:
            game['p2'].x -= 6
        if keys[pygame.K_RIGHT] and game['p2'].right < WIDTH and game['p2_lives'] > 0:
            game['p2'].x += 6
        if keys[pygame.K_UP] and game['p2'].bottom >= GROUND_Y + 80 and game['p2_lives'] > 0:
            game['p2_vel'] = -18

        # Gravity
        if game['p1_lives'] > 0:
            game['p1_vel'] += 1.2
            game['p1'].y += game['p1_vel']
            if game['p1'].bottom >= GROUND_Y + 80:
                game['p1'].bottom = GROUND_Y + 80
                game['p1_vel'] = 0

        if game['p2_lives'] > 0:
            game['p2_vel'] += 1.2
            game['p2'].y += game['p2_vel']
            if game['p2'].bottom >= GROUND_Y + 80:
                game['p2'].bottom = GROUND_Y + 80
                game['p2_vel'] = 0

        # Dragon movement
        game['dragon_x'] += game['dragon_speed'] * game['dragon_dir']
        if game['dragon_x'] <= 0 or game['dragon_x'] >= WIDTH - 100:
            game['dragon_dir'] *= -1

        # Fireballs
        if random.randint(1, 18) == 1:
            game['fireballs'].append(pygame.Rect(game['dragon_x'] + 40, game['dragon_y'] + 60, 32, 32))

        for fb in game['fireballs'][:]:
            fb.y += 7
            if fb.colliderect(game['p1']) and game['p1_lives'] > 0:
                game['p1_lives'] -= 1
                game['fireballs'].remove(fb)
            elif fb.colliderect(game['p2']) and game['p2_lives'] > 0:
                game['p2_lives'] -= 1
                game['fireballs'].remove(fb)
            elif fb.y > HEIGHT:
                game['fireballs'].remove(fb)

        # Black orbs
        if random.randint(1, 70) == 1 and len(game['black_orbs']) < orb_target:
            x = random.randint(50, WIDTH - 82)
            y = random.choice([GROUND_Y + 40, GROUND_Y - 60])
            game['black_orbs'].append(pygame.Rect(x, y, 32, 32))

        for orb in game['black_orbs'][:]:
            if (orb.colliderect(game['p1']) and game['p1_lives'] > 0) or (orb.colliderect(game['p2']) and game['p2_lives'] > 0):
                if game['orb_count'] < orb_target:
                    game['orb_count'] += 1
                game['black_orbs'].remove(orb)

        # Massive orb update
        if game['massive_orb']:
            game['massive_orb'].y -= 10
            dragon_rect = pygame.Rect(game['dragon_x'], game['dragon_y'], 100, 100)
            if game['massive_orb'].colliderect(dragon_rect):
                game['victory'] = True
                game['massive_orb'] = None
            elif game['massive_orb'].bottom < 0:
                game['massive_orb'] = None
                game['orb_count'] = 0
                game['miss_timer'] = current_time

        # Game over if both players dead
        if game['p1_lives'] <= 0 and game['p2_lives'] <= 0:
            game['game_over'] = True

    # Drawing
    win.blit(dragon_img, (game['dragon_x'], game['dragon_y']))
    win.blit(p1_img, game['p1'])
    win.blit(p2_img, game['p2'])

    for fb in game['fireballs']:
        win.blit(fireball_img, fb)
    for orb in game['black_orbs']:
        win.blit(black_orb_img, orb)

    if game['massive_orb']:
        pygame.draw.circle(win, (80, 0, 200), game['massive_orb'].center, 30)
        glow_radius = 35 + random.randint(0, 3)
        pygame.draw.circle(win, (160, 100, 255, 100), game['massive_orb'].center, glow_radius)

    for i in range(game['p1_lives']):
        win.blit(heart_img, (10 + i * 34, 10))
    for i in range(game['p2_lives']):
        win.blit(heart_img, (WIDTH - (i + 1) * 34 - 10, 10))

    orb_text = font.render(f"Orbs: {game['orb_count']}/{orb_target}", True, (255, 255, 255))
    win.blit(orb_text, (WIDTH//2 - orb_text.get_width()//2, 10))

    if game['orb_count'] >= orb_target and not game['massive_orb']:
        g_text = font.render("Press G to slay the Dragon!", True, (255, 215, 0))
        win.blit(g_text, (WIDTH // 2 - g_text.get_width() // 2, HEIGHT // 2 - 40))

    if 0 < current_time - game['miss_timer'] < 2000:
        miss_text = font.render("You Missed!", True, (255, 0, 0))
        win.blit(miss_text, (WIDTH // 2 - miss_text.get_width() // 2, HEIGHT // 2 - 80))

    if game['game_over']:
        text = font.render("Game Over", True, (255, 0, 0))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        draw_button("Replay")
        hint = font.render("Press R to Replay", True, (180, 180, 180))
        win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 70))

    if game['victory']:
        text = font.render("Dragon Defeated! You Win!", True, (0, 255, 0))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        draw_button("Replay")
        hint = font.render("Press R to Replay", True, (180, 180, 180))
        win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 70))

    pygame.display.update()

pygame.quit()
