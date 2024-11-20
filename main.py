import pygame
import random
import time

# Inicialización de pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Obtener el primer joystick
    joystick.init()  # Inicializar el joystick
else:
    print("No se encontró ningún joystick.")
    pygame.quit()
    exit()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego del Autobús")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Parámetros del juego
FPS = 60
bus_speed = 7
scroll_speed = 5
score = 0
WIN_SCORE = 300
lives = 2  # Número de vidas
invulnerable = False  # Estado de invulnerabilidad
invulnerability_timer = 0  # Temporizador de invulnerabilidad

# Fuentes
font = pygame.font.Font(None, 36)
end_font = pygame.font.Font(None, 72)

# Cargar imágenes
bus_img = pygame.image.load("assets/img/bus.png")
bus_img = pygame.transform.scale(bus_img, (80, 160))
obstacle_img = pygame.image.load("assets/img/cone.png")
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
item_img = pygame.image.load("assets/img/coin.png")
item_img = pygame.transform.scale(item_img, (30, 30))
road_img = pygame.image.load("assets/img/road.jpg")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Rectángulo del autobús
bus_rect = bus_img.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Listas para obstáculos y objetos coleccionables
obstacles = []
items = []

# Variables para el fondo de pista
road_y = 0

# Lista de puntuaciones
high_scores = []  # Para guardar el nombre y la puntuación de los mejores jugadores


# Función para generar obstáculos
def generate_obstacle():
    x = random.randint(100, WIDTH - 100)
    y = random.randint(-600, -50)
    obstacle_rect = obstacle_img.get_rect(center=(x, y))
    obstacles.append(obstacle_rect)


# Función para generar objetos coleccionables
def generate_item():
    x = random.randint(100, WIDTH - 100)
    y = random.randint(-600, -50)
    item_rect = item_img.get_rect(center=(x, y))
    items.append(item_rect)


# Función para mover el autobús
def move_bus(keys):
    joystick_x = joystick.get_axis(0)
    joystick_y = joystick.get_axis(2)
    if (
        keys[pygame.K_LEFT] or joystick_x < -0.1 or joystick_y < -0.1
    ) and bus_rect.left > 100:
        bus_rect.x -= bus_speed
    if (
        keys[pygame.K_RIGHT] or joystick_x > 0.1 or joystick_y > 0.1
    ) and bus_rect.right < WIDTH - 100:
        bus_rect.x += bus_speed


# Función para actualizar obstáculos y objetos coleccionables
def update_objects():
    global score
    for obstacle in obstacles[:]:
        obstacle.y += scroll_speed
        if obstacle.top > HEIGHT:
            obstacles.remove(obstacle)

    for item in items[:]:
        item.y += scroll_speed
        if item.top > HEIGHT:
            items.remove(item)
        if bus_rect.colliderect(item):
            score += 10
            items.remove(item)


# Función para simular el movimiento de la pista
def update_road():
    global road_y
    road_y += scroll_speed
    if road_y >= HEIGHT:
        road_y = 0


# Función para mostrar la puntuación
def show_score():
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Función para mostrar las vidas restantes
def show_lives():
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))


# Función para mostrar el menú de fin de juego (Continuar o Cancelar)
def show_game_over_menu():
    global lives
    screen.fill(BLACK)
    continue_text = end_font.render("Continuar", True, WHITE)
    cancel_text = end_font.render("Cancelar", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    cancel_rect = cancel_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(continue_text, continue_rect)
    screen.blit(cancel_text, cancel_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Salir del juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Salir del juego
                elif event.key == pygame.K_UP:
                    lives = 1  # Dar una vida extra
                    return True  # Continuar el juego
                elif event.key == pygame.K_DOWN:
                    return False  # Cancelar el juego


# Función para mostrar la pantalla final
def show_end_screen(message):
    text = end_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Animación simple de parpadeo
    alpha = 0
    direction = 5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return

        screen.fill(BLACK)
        text.set_alpha(alpha)
        screen.blit(text, text_rect)

        # Actualizar el alfa para la animación
        alpha += direction
        if alpha >= 255 or alpha <= 0:
            direction *= -1

        pygame.display.flip()
        pygame.time.delay(30)


# Función para mostrar la lista de puntuaciones
def show_high_scores():
    screen.fill(BLACK)
    title_text = end_font.render("Puntuaciones Altas", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    # Mostrar las puntuaciones
    high_scores_sorted = sorted(high_scores, key=lambda x: x[1], reverse=True)[
        :5
    ]  # Mostrar top 5
    for i, (name, score) in enumerate(high_scores_sorted):
        score_text = font.render(f"{i + 1}. {name}: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 150 + i * 40))
        screen.blit(score_text, score_rect)

    pygame.display.flip()
    time.sleep(3)  # Mostrar la lista durante 3 segundos


# Función principal del juego
def main():
    global lives, score, invulnerable, invulnerability_timer
    # Pedir nombre del jugador al inicio
    player_name = ""
    input_active = True
    while input_active:
        screen.fill(BLACK)
        name_text = font.render(f"Ingrese su nombre: {player_name}", True, WHITE)
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter para empezar
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Eliminar último carácter
                else:
                    player_name += event.unicode  # Añadir carácter

    # Agregar el jugador a la lista de puntuaciones
    global high_scores
    high_scores.append((player_name, 0))

    clock = pygame.time.Clock()
    running = True
    game_active = True

    # Generar obstáculos y objetos iniciales
    for _ in range(3):
        generate_obstacle()
        generate_item()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if game_active:
            move_bus(keys)

            # Generar nuevos obstáculos y objetos coleccionables
            if random.randint(0, 40) == 0:
                generate_obstacle()
            if random.randint(0, 50) == 0:
                generate_item()

            update_objects()
            update_road()

            # Dibujar elementos en pantalla
            screen.blit(road_img, (0, road_y - HEIGHT))
            screen.blit(road_img, (0, road_y))
            if not invulnerable or int(pygame.time.get_ticks() / 500) % 2 == 0:
                screen.blit(bus_img, bus_rect)
            for obstacle in obstacles:
                screen.blit(obstacle_img, obstacle)
            for item in items:
                screen.blit(item_img, item)

            show_score()
            show_lives()

            if score >= WIN_SCORE:
                show_end_screen("¡Felicidades, has alcanzado la meta!")
                high_scores[-1] = (player_name, score)
                show_high_scores()
                break

            # Verificar si se chocó
            for obstacle in obstacles:
                if bus_rect.colliderect(obstacle):
                    if not invulnerable:
                        lives -= 1
                        invulnerable = True
                        invulnerability_timer = pygame.time.get_ticks()
                        if lives <= 0:
                            game_active = False
                            show_end_screen("Perdiste")
                            high_scores[-1] = (player_name, score)
                            show_high_scores()
                            break

            if invulnerable and pygame.time.get_ticks() - invulnerability_timer > 2000:
                invulnerable = (
                    False  # Desactivar invulnerabilidad después de 2 segundos
                )

        else:
            if not show_game_over_menu():
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
