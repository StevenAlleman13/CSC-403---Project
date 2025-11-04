import pygame
class BackgroundButton:
    """
    An invisible background button for the main page that only triggers when
    the white space outside of the buttons positioned inside of the background
    is clicked.
    """
    def __init__(self, rect, on_click, exclude_rects=None):
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.exclude_rects = exclude_rects or []

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if not self.rect.collidepoint(e.pos):
                return
            # if the click is inside any excluded rect like the right/left or
            # donate button then the background button ignores the click.
            for r in self.exclude_rects:
                if r.collidepoint(e.pos):
                    return
            self.on_click()

    # makes background button invisible
    def draw_button(self): 
        pass
