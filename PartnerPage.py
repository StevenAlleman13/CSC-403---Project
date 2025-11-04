import pygame
import sys

# initialize pygame if it hasn’t been already
pygame.init()

# screen setup (make sure this matches your main screen size)
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Partner Page")

# fonts and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 80)

def partner_page():
    """Simple placeholder screen for Partner Page."""
    running = True
    while running:
        SCREEN.fill(BLACK)

        # draw text centered
        text = FONT.render("Partner Page", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(text, text_rect)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    partner_page()
