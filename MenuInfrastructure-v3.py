import pygame, sys, time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AD Tinder")

# Image imports
IMAGE_FILES = [
    "phone1.jpg",
    "phone2.jpg",
    "phone3.jpg",
    "phone4.jpg",
    "phone5.jpg",
    "watch1.jpg",
    "watch2.jpg",
    "watch3.jpg",
    "watch4.jpg",
    "shirt1.jpg",
    "shirt2.jpg",
    "shirt3.jpg",
    "shirt4.jpg",
    "shoe1.jpg",
    "shoe2.jpg",
    "shoe3.jpg",
    "shoe4.jpg",
    "shoe5.jpg",
    "tv1.jpg",
    "tv2.jpg",
    "tv3.jpg",
    "tv4.jpg",
    "tv5.jpg",
]

def load_scaled(path):
    return pygame.transform.scale(pygame.image.load(path), (540, 640))

IMAGES = [load_scaled(p) for p in IMAGE_FILES]

# --- Money counter ---                                                                  Added Money Counter
MONEY_CENTS = 0                                 # SA

def format_money(cents: int) -> str:
    dollars = cents // 100
    c = cents % 100
    return f"${dollars:,}.{c:02d}"


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
GOLD = (182, 143, 64)
LIGHT_BLUE = (173, 216, 230)
CREAM = (255, 235, 205, 255)
DARKGREY = (51, 51, 51, 255)
ROYALBLUE = (72, 118, 255, 255)

# Font
def get_font(size):
    return pygame.font.SysFont("arial", size, bold=True)

# add gradient to background
def draw_gradient_background(surface, top_color, bottom_color):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

# ----- TextBox Class -----
class TextBox:
    def __init__(self, rect, font, text_color=BLACK, bg_color=WHITE, border_color=BLACK, border_color_active=GREEN,
                 placeholder="", is_password=False, max_len=64, border_width=3, radius=12):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_color_active = border_color_active
        self.placeholder = placeholder
        self.is_password = is_password
        self.max_len = max_len
        self.border_width = border_width
        self.radius = radius

        self.text = ""
        self.active = False
        self.cursor_visible = True
        self._last_blink = time.time()
        self._blink_interval = 0.5  # seconds

        self._rendered = None
        self._update_render()

    @property
    def value(self):
        return self.text

    def set_text(self, s):
        self.text = s[: self.max_len]
        self._update_render()

    def _display_text(self):
        if self.text:
            return ("*" * len(self.text)) if self.is_password else self.text
        return ""  # placeholder handled separately

    def _update_render(self):
        shown = self._display_text()
        # Show placeholder if not active and empty
        if not shown and not self.active and self.placeholder:
            self._rendered = self.font.render(self.placeholder, True, (130, 130, 130))
        else:
            self._rendered = self.font.render(shown, True, self.text_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self._update_render()
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Optional: deactivate on enter
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            else:
                # Accept printable characters
                if event.unicode and len(self.text) < self.max_len:
                    # Filter out control chars
                    if 32 <= ord(event.unicode) <= 126:
                        self.text += event.unicode
            self._update_render()

    def update(self):
        # Blink cursor
        if time.time() - self._last_blink >= self._blink_interval:
            self.cursor_visible = not self.cursor_visible
            self._last_blink = time.time()

    def draw(self, surface):
        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.radius)
        # Border
        border_col = self.border_color_active if self.active else self.border_color
        pygame.draw.rect(surface, border_col, self.rect, self.border_width, border_radius=self.radius)
        # Text
        text_surf = self._rendered
        text_rect = text_surf.get_rect()
        padding_x, padding_y = 12, 6
        text_rect.topleft = (self.rect.x + padding_x, self.rect.y + padding_y)
        surface.blit(text_surf, text_rect)
        # Cursor
        if self.active and self.cursor_visible:
            # Place cursor at end of text (or placeholder start)
            cursor_x = text_rect.right if self.text else (self.rect.x + padding_x)
            top = self.rect.y + padding_y
            bottom = top + self.font.get_height()
            pygame.draw.line(surface, border_col, (cursor_x + 1, top), (cursor_x + 1, bottom), 2)

# ----- Button Class -----
class Button:
    def __init__(self, text, pos, font, base_color, hovering_color, callback):
        self.text = text
        self.pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.callback = callback
        self.rendered = self.font.render(self.text, True, self.base_color)
        self.rect = self.rendered.get_rect(center=self.pos)

    def update(self, surface):
        surface.blit(self.rendered, self.rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.check_for_input(position):
            self.rendered = self.font.render(self.text, True, self.hovering_color)
        else:
            self.rendered = self.font.render(self.text, True, self.base_color)

# ----- Screens -----
# Terms of Service screen and its button functions
def tos():
    while True:
        draw_gradient_background(SCREEN, DARKGREY, DARKGREY)
        mouse_pos = pygame.mouse.get_pos()

        # Text
        text = get_font(45).render("Terms of Service", True, WHITE)
        text_rect = text.get_rect(center=(640, 260))
        SCREEN.blit(text, text_rect)

        # accept button
        accept_button = Button("ACCEPT", (640, 460), get_font(75), BLACK, DARKGREY, adscreen)
        accept_button.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE, accept_button.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, accept_button.rect, 4, border_radius=15)
        accept_button.update(SCREEN)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if accept_button.check_for_input(mouse_pos):
                    accept_button.callback()

        pygame.display.update()

# adscreen screen and its button functions
def adscreen():
   
    global MONEY_CENTS
   
    idx = 0                                     # SA
    current_img = IMAGES[idx]

    while True:
        draw_gradient_background(SCREEN, DARKGREY, DARKGREY)
        mouse_pos = pygame.mouse.get_pos()

        # text
        text = get_font(45).render("TWO Images Displayed Here", True, WHITE)
        text_rect = text.get_rect(center=(640, 260))
        SCREEN.blit(text, text_rect)

        # no button
        no_button = Button("NO", (285, 360), get_font(75), BLACK, DARKGREY, adscreen)
        no_button.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE, no_button.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, no_button.rect, 2, border_radius=15)
        no_button.update(SCREEN)

        # yes button
        yes_button = Button("YES", (1015, 360), get_font(75), BLACK, DARKGREY, adscreen)
        yes_button.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE, yes_button.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, yes_button.rect, 2, border_radius=15)
        yes_button.update(SCREEN)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if no_button.check_for_input(mouse_pos) or yes_button.check_for_input(mouse_pos):            # SA
                    MONEY_CENTS += 5                                                                                         #   Adds 5 cents each click
                    idx += 1
                    if idx >= len(IMAGES):
                        idx = 0
                        main_menu()
                    current_img = IMAGES[idx]

        SCREEN.blit(current_img, current_img.get_rect(center=SCREEN.get_rect().center))

        money_surf = get_font(36).render(format_money(MONEY_CENTS), True, WHITE)
        SCREEN.blit(money_surf, (20, 20))
        
        pygame.display.flip()
        pygame.display.update()

# Login screen and its button functions
def login():
    # Create controls one time
    title = get_font(72).render("Sign In", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 120))

    label_user = get_font(36).render("Username", True, WHITE)
    label_pass = get_font(36).render("Password", True, WHITE)
    label_ssn = get_font(36).render("SSN", True, WHITE)

    #Username text box
    user_box = TextBox(
        rect=(WIDTH // 2 - 250, 220, 500, 60),
        font=get_font(36),
        placeholder="Enter username",
        bg_color=WHITE,
        border_color=BLACK,
        border_color_active=ROYALBLUE,
        radius=15
    )
    # Password text box
    pass_box = TextBox(
        rect=(WIDTH // 2 - 250, 320, 500, 60),
        font=get_font(36),
        placeholder="Enter password",
        bg_color=WHITE,
        border_color=BLACK,
        border_color_active=ROYALBLUE,
        is_password=True,
        radius=15
    )
    # Social Security Number text box
    ssn_box = TextBox(
        rect=(WIDTH // 2 - 250, 420, 500, 60),
        font=get_font(36),
        placeholder="Enter SSN",
        bg_color=WHITE,
        border_color=BLACK,
        border_color_active=ROYALBLUE,
        is_password=True,
        radius=15
    )

    login_button = Button("LOGIN", (WIDTH // 2, 550), get_font(60), BLACK, WHITE, tos)

    while True:
        draw_gradient_background(SCREEN, (255, 69, 0, 255), (220, 20, 60, 255))
        mouse_pos = pygame.mouse.get_pos()

        # Labels & title
        SCREEN.blit(title, title_rect)
        SCREEN.blit(label_user, (user_box.rect.x, user_box.rect.y - 40))
        SCREEN.blit(label_pass, (pass_box.rect.x, pass_box.rect.y - 40))
        SCREEN.blit(label_ssn, (ssn_box.rect.x, ssn_box.rect.y - 40))

        # Update controls
        user_box.update()
        pass_box.update()
        ssn_box.update()
        user_box.draw(SCREEN)
        pass_box.draw(SCREEN)
        ssn_box.draw(SCREEN)

        # Continue button (All fields must be filled)
        enabled = bool(user_box.value.strip() and pass_box.value.strip() and ssn_box.value.strip())
        login_button.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE if enabled else (200, 200, 200),
                         login_button.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, login_button.rect, 4, border_radius=15)
        login_button.update(SCREEN)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            user_box.handle_event(event)
            pass_box.handle_event(event)
            ssn_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and enabled:
                if login_button.check_for_input(mouse_pos):
                    # You can grab credentials here if needed:
                    # print("Username:", user_box.value, "Password:", pass_box.value)
                    login_button.callback()

        pygame.display.update()

# Main Menu screen and its button functions
def main_menu():
    while True:
        draw_gradient_background(SCREEN, (255, 69, 0, 255), (220, 20, 60, 255))
        mouse_pos = pygame.mouse.get_pos()

        # Menu title
        title_text = get_font(100).render("AD TINDER", True, WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        SCREEN.blit(title_text, title_rect)

        # Buttons
        start_button = Button("START", (640, 325), get_font(75), BLACK, BLACK, login)
        quit_button = Button("QUIT", (640, 475), get_font(75), BLACK, BLACK, sys.exit)

        for button in [start_button, quit_button]:
            button.change_color(mouse_pos)
            pygame.draw.rect(SCREEN, WHITE, button.rect, border_radius=15)
            pygame.draw.rect(SCREEN, BLACK, button.rect, 4, border_radius=15)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(mouse_pos):
                    start_button.callback()
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit(); sys.exit()

        pygame.display.update()

# Run Program

main_menu()
