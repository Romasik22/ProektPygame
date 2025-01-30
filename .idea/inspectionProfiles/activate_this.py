import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Launcher")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

flappy_bird_img = pygame.image.load("610-6106806_flappy-bird-png-flappy-bird-pixelart-transparent-png.png")
flappy_bird_img = pygame.transform.scale(flappy_bird_img, (50, 50))
snake_food_img = pygame.image.load("i.webp")
snake_food_img = pygame.transform.scale(snake_food_img, (30, 30))
game_over_img = pygame.image.load("maxresdefault.jpg")
game_over_img = pygame.transform.scale(game_over_img, (400, 300))

menu_background = pygame.image.load("background.jpg")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))


def game_over_screen(game_func, main_menu_func):
    while True:
        screen.fill(BLACK)
        screen.blit(game_over_img, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
        font = pygame.font.SysFont(None, 40)
        restart_text = font.render("Restart", True, BLACK)
        menu_text = font.render("Menu", True, BLACK)
        restart_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 180, 140, 40)
        menu_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 230, 140, 40)
        pygame.draw.rect(screen, GREEN, restart_rect)
        pygame.draw.rect(screen, RED, menu_rect)
        screen.blit(restart_text, (WIDTH // 2 - 35, HEIGHT // 2 + 190))
        screen.blit(menu_text, (WIDTH // 2 - 25, HEIGHT // 2 + 240))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    game_func()
                elif menu_rect.collidepoint(event.pos):
                    main_menu_func()

def pause_screen(game_func, main_menu_func):
    paused = True
    while paused:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 40)
        resume_text = font.render("Resume", True, BLACK)
        restart_text = font.render("Restart", True, BLACK)
        menu_text = font.render("Menu", True, BLACK)
        resume_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 - 50, 140, 40)
        restart_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2, 140, 40)
        menu_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 50, 140, 40)
        pygame.draw.rect(screen, GREEN, resume_rect)
        pygame.draw.rect(screen, BLUE, restart_rect)
        pygame.draw.rect(screen, RED, menu_rect)
        screen.blit(resume_text, (WIDTH // 2 - 35, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - 35, HEIGHT // 2 + 10))
        screen.blit(menu_text, (WIDTH // 2 - 25, HEIGHT // 2 + 60))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    paused = False
                elif restart_rect.collidepoint(event.pos):
                    game_func()
                elif menu_rect.collidepoint(event.pos):
                    main_menu_func()


def flappy_bird():
    bird_x = 50
    bird_y = HEIGHT // 2
    bird_velocity = 0
    gravity = 0.7
    jump_strength = -6
    pipe_width = 70
    pipe_gap = 200
    pipe_velocity = 5
    pipes = []
    score = 0
    clock = pygame.time.Clock()

    def draw_bird():
        screen.blit(flappy_bird_img, (bird_x, bird_y))

    def draw_pipes():
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe)

    def check_collision():
        bird_rect = pygame.Rect(bird_x, bird_y, 50, 50)
        for pipe in pipes:
            pipe_rect = pygame.Rect(pipe[0], pipe[1], pipe[2], pipe[3])
            if bird_rect.colliderect(pipe_rect):
                return True
        if bird_y + 50 > HEIGHT or bird_y < 0:
            return True
        return False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                if event.key == pygame.K_ESCAPE:
                    pause_screen(flappy_bird, main_menu)

        bird_velocity += gravity
        bird_y += bird_velocity

        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
            pipes.append([WIDTH, 0, pipe_width, pipe_height])
            pipes.append([WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap])

        for pipe in pipes:
            pipe[0] -= pipe_velocity

        if pipes[0][0] + pipe_width < 0:
            pipes.pop(0)
            pipes.pop(0)
            score += 1

        if check_collision():
            game_over_screen(flappy_bird, main_menu)
            return

        screen.fill(WHITE)
        draw_bird()
        draw_pipes()
        font = pygame.font.SysFont(None, 40)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(30)


def snake_game():
    snake_size = 20
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    food = [random.randint(0, (WIDTH - snake_size) // snake_size) * snake_size,
            random.randint(0, (HEIGHT - snake_size) // snake_size) * snake_size]
    clock = pygame.time.Clock()
    snake_speed = 10

    def draw_snake():
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, snake_size, snake_size))

    def draw_food():
        screen.blit(snake_food_img, (food[0], food[1]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    pause_screen(snake_game, main_menu)

        if direction == "UP":
            new_head = [snake[0][0], snake[0][1] - snake_size]
        elif direction == "DOWN":
            new_head = [snake[0][0], snake[0][1] + snake_size]
        elif direction == "LEFT":
            new_head = [snake[0][0] - snake_size, snake[0][1]]
        elif direction == "RIGHT":
            new_head = [snake[0][0] + snake_size, snake[0][1]]

        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in snake:
            game_over_screen(snake_game, main_menu)
            return

        snake.insert(0, new_head)
        if new_head[0] == food[0] and new_head[1] == food[1]:
            food = [random.randint(0, (WIDTH - snake_size) // snake_size) * snake_size,
                    random.randint(0, (HEIGHT - snake_size) // snake_size) * snake_size]
        else:
            snake.pop()

        screen.fill(WHITE)
        draw_snake()
        draw_food()
        pygame.display.flip()
        clock.tick(snake_speed)


def arkanoid():
    paddle_width = 100
    paddle_height = 20
    ball_radius = 10
    ball_speed = 5
    paddle_speed = 10

    class Paddle:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)
            self.speed = paddle_speed

        def move(self, x):
            self.rect.x += x
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

    class Ball:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
            self.speed_x = ball_speed * random.choice([-1, 1])
            self.speed_y = -ball_speed

        def move(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        def bounce(self):
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speed_x = -self.speed_x
            if self.rect.top <= 0:
                self.speed_y = -self.speed_y

    paddle = Paddle()
    ball = Ball()
    running = True

    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, paddle.rect)
        pygame.draw.circle(screen, RED, ball.rect.center, ball_radius)

        ball.move()
        ball.bounce()

        if ball.rect.colliderect(paddle.rect):
            ball.speed_y = -ball.speed_y

        if ball.rect.bottom >= HEIGHT:
            game_over_screen(arkanoid, main_menu)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-paddle.speed)
        if keys[pygame.K_RIGHT]:
            paddle.move(paddle.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(arkanoid, main_menu)

        pygame.display.flip()
        clock.tick(60)


def space_invaders():
    player_width = 50
    player_height = 20
    bullet_width = 5
    bullet_height = 10
    alien_width = 40
    alien_height = 40
    alien_speed = 2
    bullet_speed = 7
    max_bullets = 5

    class Player:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 50, player_width, player_height)
            self.speed = 5

        def move(self, dx):
            self.rect.x += dx
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

    class Bullet:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, bullet_width, bullet_height)

        def move(self):
            self.rect.y -= bullet_speed

    class Alien:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, alien_width, alien_height)
            self.direction = 1

        def move(self):
            self.rect.x += alien_speed * self.direction

        def change_direction(self):
            self.direction = -self.direction

    player = Player()
    bullets = []
    aliens = [Alien(x * (alien_width + 10), y * (alien_height + 10)) for x in range(8) for y in range(3)]
    running = True

    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, player.rect)

        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet.rect)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien.rect)

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for alien in aliens[:]:
            for bullet in bullets[:]:
                if alien.rect.colliderect(bullet.rect):
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    break

        for alien in aliens:
            if alien.rect.colliderect(player.rect):
                game_over_screen(space_invaders, main_menu)
                return

        for alien in aliens:
            alien.move()
            if alien.rect.left <= 0 or alien.rect.right >= WIDTH:
                for alien in aliens:
                    alien.change_direction()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)
        if keys[pygame.K_SPACE] and len(bullets) < max_bullets:
            bullets.append(Bullet(player.rect.centerx - bullet_width // 2, player.rect.top))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(space_invaders, main_menu)  # Передали main_menu

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    running = True
    while running:
        screen.blit(menu_background, (0, 0))

        font = pygame.font.SysFont(None, 40)
        title_text = font.render("Game Launcher", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - 100, 50))

        buttons = [
            ("Flappy Bird", 150, flappy_bird),
            ("Snake", 250, snake_game),
            ("Arkanoid", 350, arkanoid),
            ("Space Invaders", 450, space_invaders)
        ]

        for text, y, game_func in buttons:
            pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, y, 200, 50))
            label = font.render(text, True, BLACK)
            screen.blit(label, (WIDTH // 2 - 80, y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for text, btn_y, game_func in buttons:
                    if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and btn_y <= y <= btn_y + 50:
                        game_func()

main_menu()
