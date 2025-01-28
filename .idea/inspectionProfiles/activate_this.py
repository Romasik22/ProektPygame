import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Launcher")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Шрифты
font = pygame.font.SysFont(None, 40)

# Кнопки
buttons = [
    {"text": "Arkanoid", "rect": pygame.Rect(250, 100, 300, 50)},
    {"text": "Flappy Bird", "rect": pygame.Rect(250, 200, 300, 50)},
    {"text": "Snake", "rect": pygame.Rect(250, 300, 300, 50)},
    {"text": "Space Invaders", "rect": pygame.Rect(250, 400, 300, 50)}
]

# Функция для отрисовки кнопок
def draw_buttons():
    for button in buttons:
        pygame.draw.rect(screen, GREEN, button["rect"])
        text = font.render(button["text"], True, BLACK)
        screen.blit(text, (button["rect"].x + 50, button["rect"].y + 10))

# Функция для запуска игры
def run_game(game_name):
    if game_name == "Arkanoid":
        arkanoid()
    elif game_name == "Flappy Bird":
        flappy_bird()
    elif game_name == "Snake":
        snake_game()
    elif game_name == "Space Invaders":
        space_invaders()

# --- Игры ---

# Арканоид
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
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-paddle.speed)
        if keys[pygame.K_RIGHT]:
            paddle.move(paddle.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over!")

# Flappy Bird
def flappy_bird():
    bird_width = 50
    bird_height = 50
    gravity = 1
    jump_strength = -7
    pipe_width = 60
    pipe_gap = 200
    pipe_speed = 4

    class Bird:
        def __init__(self):
            self.rect = pygame.Rect(100, HEIGHT // 2, bird_width, bird_height)
            self.velocity = 0

        def move(self):
            self.velocity += gravity
            self.rect.y += self.velocity

        def jump(self):
            self.velocity = jump_strength

    class Pipe:
        def __init__(self):
            self.x = WIDTH
            self.height = random.randint(100, HEIGHT - pipe_gap - 100)
            self.top = pygame.Rect(self.x, 0, pipe_width, self.height)
            self.bottom = pygame.Rect(self.x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)

        def move(self):
            self.x -= pipe_speed
            self.top.x = self.x
            self.bottom.x = self.x

        def reset(self):
            self.x = WIDTH
            self.height = random.randint(100, HEIGHT - pipe_gap - 100)
            self.top = pygame.Rect(self.x, 0, pipe_width, self.height)
            self.bottom = pygame.Rect(self.x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)

    bird = Bird()
    pipes = [Pipe()]
    running = True

    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, bird.rect)

        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe.top)
            pygame.draw.rect(screen, GREEN, pipe.bottom)

        bird.move()

        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            running = False

        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe_width < 0:
                pipes.remove(pipe)
                pipes.append(Pipe())

            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(90  )

    pygame.quit()
    print("Game Over!")

def snake_game():
    snake_size = 20
    snake_speed = 15
    food_size = 20

    class Snake:
        def __init__(self):
            self.body = [(100, 100), (80, 100), (60, 100)]
            self.direction = (snake_size, 0)

        def move(self):
            head_x, head_y = self.body[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            self.body = [new_head] + self.body[:-1]

        def grow(self):
            tail_x, tail_y = self.body[-1]
            self.body.append((tail_x, tail_y))

        def collides_with_boundaries(self):
            head_x, head_y = self.body[0]
            return head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT

        def collides_with_self(self):
            return len(self.body) != len(set(self.body))

    snake = Snake()
    food = (random.randint(0, (WIDTH - food_size) // food_size) * food_size,
            random.randint(0, (HEIGHT - food_size) // food_size) * food_size)
    running = True

    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], snake_size, snake_size))

        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], food_size, food_size))

        snake.move()

        if snake.collides_with_boundaries() or snake.collides_with_self():
            running = False  # Проигрыш, если змейка столкнулась с границами или собой

        if (snake.body[0][0], snake.body[0][1]) == food:
            snake.grow()
            food = (random.randint(0, (WIDTH - food_size) // food_size) * food_size,
                    random.randint(0, (HEIGHT - food_size) // food_size) * food_size)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.direction != (snake_size, 0):
            snake.direction = (-snake_size, 0)
        if keys[pygame.K_RIGHT] and snake.direction != (-snake_size, 0):
            snake.direction = (snake_size, 0)
        if keys[pygame.K_UP] and snake.direction != (0, snake_size):
            snake.direction = (0, -snake_size)
        if keys[pygame.K_DOWN] and snake.direction != (0, -snake_size):
            snake.direction = (0, snake_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(snake_speed)

    pygame.quit()
    print("Game Over!")

# Space Invaders
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

        # Перемещение пули
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # Столкновения с пришельцами
        for alien in aliens[:]:
            for bullet in bullets[:]:
                if alien.rect.colliderect(bullet.rect):
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    break

        # Столкновения с игроком
        for alien in aliens:
            if alien.rect.colliderect(player.rect):
                running = False  # Проигрыш, если пришелец столкнулся с игроком

        # Движение пришельцев
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over!")

# Главное меню
def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button["rect"].collidepoint(pos):
                        run_game(button["text"])

        pygame.display.flip()

    pygame.quit()

# Запуск главного меню
main_menu()
