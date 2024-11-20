import pygame
import time


# Función para mostrar pantalla con texto y animación
def show_screen_with_text(text, background_image):
    screen.fill(BLACK)  # Limpiar la pantalla

    # Cargar y mostrar el fondo
    background = pygame.image.load(background_image)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    # Crear el texto con una animación simple
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Animación de aparición de texto (desvanecimiento)
    alpha = 0
    direction = 5  # Velocidad de la animación de desvanecimiento
    while alpha <= 255:  # Hasta que el texto sea completamente visible
        screen.fill(BLACK)
        screen.blit(background, (0, 0))  # Mostrar el fondo
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        alpha += direction
        if alpha >= 255:
            direction *= -1  # Invertir la dirección para hacer parpadear el texto

        pygame.time.delay(30)  # Delay para controlar la velocidad del parpadeo

    # Esperar a que el jugador haga clic en la pantalla para continuar
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                waiting_for_input = False  # Salir del bucle cuando se hace clic


# Inicialización de Pygame y configuración de pantalla
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pantalla con Texto y Animación")

# Fuentes
font = pygame.font.Font(None, 36)

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Ejemplo de cómo usar la función
def main():
    # Mostrar pantalla inicial con fondo y texto animado
    show_screen_with_text("Bienvenido al Juego", "fondo.jpg")

    # Continuar con el resto del juego o la siguiente pantalla
    print("El juego continúa...")


# Llamar a la función principal
if __name__ == "__main__":
    main()
    pygame.quit()
