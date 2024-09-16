import pygame
import sys
import random
import math

# Inicializamos pygame
pygame.init()

# Configuramos los colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Configuramos la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataforma 2D")

# Reloj para controlar el framerate
clock = pygame.time.Clock()
FPS = 60

# Configuración del jugador
PLAYER_SIZE = 15
PLAYER_SPEED = 5

# Configuración de los enemigos
ENEMY_SIZE = 25
ENEMY_SPAWN_MARGIN = 50
ENEMY_VERTICAL_RANGE = (HEIGHT - 200, HEIGHT - 150)

# Configuración de las monedas
COIN_SIZE = 18
COIN_SPAWN_RANGE = 50

# Configuración del juego
POINTS_TO_NEXT_LEVEL = 10
MAX_LEVEL = 10

# Cargamos la imagen de fondo
background = pygame.image.load(r'D:\USUARIO\Desktop\Python\Ejercicios_GPT\paisaje_montanas.jpg').convert()

# Clase Jugador
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, 50, PLAYER_SIZE, PLAYER_SIZE)
        self.velocity_y = 0
        self.jumping = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Limitar movimiento dentro de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Clase Enemigo
class Enemy:
    def __init__(self, x, y, speed, movement_type):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.direction = 1
        self.speed = speed
        self.angle = 0
        self.movement_type = movement_type
        self.center_x, self.center_y = WIDTH // 2, HEIGHT // 2
        self.radius = 100

    def move(self):
        if self.movement_type == "horizontal":
            self.rect.x += self.direction * self.speed
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction *= -1
        elif self.movement_type == "vertical":
            self.rect.y += self.direction * self.speed
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.direction *= -1
        elif self.movement_type == "circular":
            self.angle += 0.05
            self.rect.centerx = self.center_x + int(self.radius * math.cos(self.angle))
            self.rect.centery = self.center_y + int(self.radius * math.sin(self.angle))

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Clase Moneda
class Coin:
    def __init__(self, enemy_rect):
        self.rect = pygame.Rect(0, 0, COIN_SIZE, COIN_SIZE)
        self.respawn(enemy_rect)

    def respawn(self, enemy_rect):
        while True:
            x = random.randint(enemy_rect.left - COIN_SPAWN_RANGE, enemy_rect.right + COIN_SPAWN_RANGE)
            y = random.randint(enemy_rect.top - COIN_SPAWN_RANGE, enemy_rect.bottom + COIN_SPAWN_RANGE)
            self.rect.topleft = (x, y)
            if self.rect.left > 0 and self.rect.right < WIDTH and self.rect.top > 0 and self.rect.bottom < HEIGHT:
                break

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

# Función para mostrar el menú principal
def show_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 55)
        text = font.render("Presiona ESPACIO para empezar", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        pygame.display.flip()
        clock.tick(FPS)

# Función para definir el número de enemigos por nivel
def get_num_enemies(level):
    if 1 <= level <= 4:
        return 4
    elif 5 <= level <= MAX_LEVEL:
        return 5
    else:
        return 5

# Función para mostrar el marcador de puntaje y nivel
def show_hud(score, level):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    level_text = font.render(f"Nivel: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

# Función principal del juego
def game():
    player = Player()
    level = 1
    score = 0
    num_enemies = get_num_enemies(level)
    enemy_types = ["horizontal", "vertical", "circular"]

    enemies = []
    for _ in range(num_enemies):
        while True:
            x = random.randint(ENEMY_SPAWN_MARGIN, WIDTH - ENEMY_SPAWN_MARGIN - ENEMY_SIZE)
            y = random.randint(*ENEMY_VERTICAL_RANGE)
            enemy = Enemy(x, y, random.randint(level * 2, level * 3), random.choice(enemy_types))
            if all(not enemy.rect.colliderect(e.rect) for e in enemies):
                enemies.append(enemy)
                break

    coin = Coin(random.choice(enemies).rect)

    running = True
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        player.move(keys)

        for enemy in enemies:
            enemy.move()

        player.draw()
        for enemy in enemies:
            enemy.draw()
        coin.draw()

        show_hud(score, level)

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                return "derrota"

        if player.rect.colliderect(coin.rect):
            score += 1
            coin.respawn(random.choice(enemies).rect)

        if score >= POINTS_TO_NEXT_LEVEL:
            level += 1
            if level > MAX_LEVEL:
                return "victoria"
            num_enemies = get_num_enemies(level)
            score = 0
            enemies = []
            for _ in range(num_enemies):
                while True:
                    x = random.randint(ENEMY_SPAWN_MARGIN, WIDTH - ENEMY_SPAWN_MARGIN - ENEMY_SIZE)
                    y = random.randint(*ENEMY_VERTICAL_RANGE)
                    enemy = Enemy(x, y, random.randint(level * 2, level * 3), random.choice(enemy_types))
                    if all(not enemy.rect.colliderect(e.rect) for e in enemies):
                        enemies.append(enemy)
                        break
            coin = Coin(random.choice(enemies).rect)

        pygame.display.flip()
        clock.tick(FPS)

# Función para mostrar la pantalla final
def end_screen(result):
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 55)
        if result == "derrota":
            text = font.render("¡Has perdido! Presiona R para reiniciar", True, WHITE)
        elif result == "victoria":
            text = font.render("¡Has ganado! Presiona R para reiniciar", True, WHITE)
        else:
            text = font.render("Gracias por jugar. Presiona R para reiniciar", True, WHITE)

        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return "restart"

        pygame.display.flip()
        clock.tick(FPS)

# Loop principal
def main():
    while True:
        show_menu()
        result = game()
        if result == "quit":
            break
        action = end_screen(result)
        if action == "quit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()