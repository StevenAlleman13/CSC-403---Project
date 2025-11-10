import pygame, sys, time, random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AD Tinder")

# if true, certain relevant values will be printed to stdout
DEBUG = False

# Categorized image imports
IMAGE_PHONE = [
    "phone1.jpg",
    "phone2.jpg",
    "phone3.jpg",
    "phone4.jpg",
    "phone5.jpg",
    "phone6.jpg",
    "phone7.jpg"
]

IMAGE_WATCH = [
    "watch1.jpg",
    "watch2.jpg",
    "watch3.jpg",
    "watch4.jpg",
    "watch5.jpg",
    "watch6.jpg",
    "watch7.jpg",
    "watch8.jpg"
]

IMAGE_SHIRT = [
    "shirt1.jpg",
    "shirt2.jpg",
    "shirt3.jpg",
    "shirt4.jpg",
    "shirt5.jpg",
    "shirt6.jpg",
    "shirt7.jpg"
]

IMAGE_SHOE = [
    "shoe1.jpg",
    "shoe2.jpg",
    "shoe3.jpg",
    "shoe4.jpg",
    "shoe5.jpg",
    "shoe6.jpg",
    "shoe7.jpg"
]

IMAGE_TV = [
    "tv1.jpg",
    "tv2.jpg",
    "tv3.jpg",
    "tv4.jpg",
    "tv5.jpg",
    "tv6.jpg",
    "tv7.jpg"
]


# final ads list. these will display upon completion based on product with highest weight value.
# will not be included in overall image files list.
FINAL_ADS = [
        "phoneperfect.jpg",
        "watchperfect.jpg",
        "shirtperfect.jpg",
        "shoeperfect.jpg",
        "tvperfect.jpg"
]

# Full image imports list for certain usecases
IMAGE_FILES = IMAGE_PHONE + IMAGE_WATCH + IMAGE_SHIRT + IMAGE_SHOE + IMAGE_TV


# Products list
# Format: <String> Product name, <Float> Weight, <String List> Filenames, <Integer> index within products list
#
# Weight value will be amended when program is running, so not a constant
products = [
    ["Phone", 0.0, IMAGE_PHONE, 0],
    ["Watch", 0.0, IMAGE_WATCH, 1],
    ["Shirt", 0.0, IMAGE_SHIRT, 2],
    ["Shoe", 0.0, IMAGE_SHOE, 3],
    ["TV", 0.0, IMAGE_TV, 4],
]

# take in products list (but not as a parameter so as to edit it)
# returns one product within the products list
# is passed to a different function to find a random ad in that category
def get_ad():
    # values that alter algorithm
    BASE = 1.0  # base value (added to weight)
    EXP = 2.0   # exponent   (applied to compound value)
    MIN = 0.1   # minimum allowed compound value
    
    # ranges list: determines highest range of an index in products list being chosen.
    ranges = []
    # value: tracks the value of all previous compound values added together, or the previous value in the ranges list. will be equal to the final value in ranges list which is important for scaling a 0.0-1.0 range random var
    value = 0

    # fill out ranges list
    for product in products:
        # compound weight value
        compound = ((product[1] + BASE) ** EXP)
        # edge case for minimum value
        if compound < 0.1:
            compound = 0.1
        
        value += compound
        ranges.append(value)
        

    # find random value
    chosen = (random.random() * value)
    
    # debug
    if DEBUG:
        print(ranges)
    
    
    # iterate over ranges list and find chosen product using relative indexing
    for i in range(len(products)):
        # condition where i == 0
        if (i == 0):
            # succeed if chosen is lower than value at ranges[i] 
            if (chosen < ranges[i]):
                # debug
                if DEBUG:
                    print("return value: " + products[i][0])
                return products[i]
        # condition where i > 0
        else:
            # succeed if chosen is greater than or equal to ranges[i - 1] and lower than ranges[i]
            if ((chosen >= ranges[i - 1]) and (chosen < ranges[i])):
                # debug
                if DEBUG:
                    print("return value: " + products[i][0])
                return products[i]
            

# parameters: specific product list(an entry in products list)
#
# return value: a specific randomized entry from the
# built in list of advertisement images in the product list
def get_random_ad(product):
    index = random.randint(0, (len(product[2]) - 1))
    # debug
    if DEBUG:
        print(index)
    return product[2][index]

# parameters: none
# resets weight values of all products to 1.0
# primary use is for when game restarts
def reset_weights():
    for product in products:
        product[1] = 1.0

# parameters: relative file pathway to images (stored in images folder)
#
# returns image for use in pygame
def load_scaled(path):
    return pygame.transform.scale(pygame.image.load('images\\' + path), (540, 640))

IMAGES = [load_scaled(p) for p in IMAGE_FILES]

# --- Money counter ---                                                                  Added Money Counter
MONEY_CENTS = 0                                 # SA

def format_money(cents: int) -> str:
    dollars = cents // 100
    c = cents % 100
    return f"${dollars:,}.{c:02d}"

scaled_image1 = pygame.transform.scale(pygame.image.load('images\phone1.jpg'), (540, 640))

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

# Add gradient to background
def draw_gradient_background(surface, top_color, bottom_color):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

# Renders imported text to fit within a certain width
def wrapped_text(surface, text, font, color, rect, line_spacing=6):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= rect.width:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)

    y = rect.y
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break  # stop when we run out of space
        surf = font.render(line, True, color)
        surface.blit(surf, (rect.x, y))
        y += font.get_height() + line_spacing

# Returns wrapped lines that fit a given width
def wrap_lines(text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

# TextBox
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

# Buttons
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

# Terms of Service screen
def tos():
    # Load TOS text
    try:
        with open("TOS.txt", "r", encoding="utf-8") as f:
            tos_text = f.read()
    except Exception:
        tos_text = "Terms of Service file (TOS.txt) not found."

    # Define a fixed box for the TOS text
    box_rect = pygame.Rect(0, 0, 800, 400)
    box_rect.center = (WIDTH // 2, HEIGHT // 2)


    scroll = 0  # top line index

    while True:
        draw_gradient_background(SCREEN, DARKGREY, DARKGREY)
        mouse_pos = pygame.mouse.get_pos()

        # Title
        title = get_font(65).render("Terms of Service", True, WHITE)
        title_rect = title.get_rect(center=(640, 115))
        SCREEN.blit(title, title_rect)

        # Draw the TOS text box
        # Fill
        pygame.draw.rect(SCREEN, WHITE, box_rect, border_radius=12)
        # Border
        pygame.draw.rect(SCREEN, BLACK, box_rect, 3, border_radius=12)

        # Sets up the scrollable text box
        content_font = get_font(20)
        pad_rect = box_rect.inflate(-20, -16)  # Padding
        # Wrap once per frame
        lines = wrap_lines(tos_text, content_font, pad_rect.width)

        # Defines space inbetween lines, vertical height of one line, and lines seen the size of the box
        line_spacing = 6
        line_h = content_font.get_height() + line_spacing
        visible_lines = max(1, pad_rect.height // line_h)

        # Calculates how far down a user can scroll
        max_scroll = max(0, len(lines) - visible_lines)
        if scroll < 0: scroll = 0
        if scroll > max_scroll: scroll = max_scroll

        # As scroll increases, start shifts down in the lines list so you are able to
        # see a different part of the text
        y = pad_rect.y
        start = scroll
        end = min(start + visible_lines, len(lines))
        for i in range(start, end):
            surf = content_font.render(lines[i], True, BLACK)
            SCREEN.blit(surf, (pad_rect.x, y))
            y += line_h

        # Creates a vertical scrollbar to track progress
        track = pygame.Rect(pad_rect.right - 10, pad_rect.y, 8, pad_rect.height)
        pygame.draw.rect(SCREEN, (220, 220, 220), track, border_radius=4)

        if len(lines) > visible_lines:
            thumb_h = max(30, int(track.height * (visible_lines / len(lines))))
            # Position scrollbar based on scroll fraction
            travel = track.height - thumb_h
            frac = 0 if max_scroll == 0 else (scroll / max_scroll)
            thumb_y = track.y + int(travel * frac)
            thumb = pygame.Rect(track.x, thumb_y, track.width, thumb_h)
            pygame.draw.rect(SCREEN, (120, 120, 120), thumb, border_radius=4)

        # Accept button
        accept_button = Button("ACCEPT", (640, 625), get_font(75), BLACK, DARKGREY, adscreen)
        accept_button.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE, accept_button.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, accept_button.rect, 4, border_radius=15)
        accept_button.update(SCREEN)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if accept_button.check_for_input(mouse_pos):
                    accept_button.callback()
            # --- SCROLL INPUT ---
            if event.type == pygame.MOUSEWHEEL:
                # pygame: event.y is +1 on wheel up, -1 on wheel down
                scroll -= event.y * 3  # tweak step size to taste

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll += 1
                elif event.key == pygame.K_UP:
                    scroll -= 1
                elif event.key == pygame.K_PAGEDOWN:
                    scroll += visible_lines
                elif event.key == pygame.K_PAGEUP:
                    scroll -= visible_lines

        pygame.display.update()

def adscreen():
    global MONEY_CENTS

    idx = 0
    current_product = products[idx]
    current_img = load_scaled(get_random_ad(current_product))
    # constant representing the total amount of ads that will run before final scene transition
    ADS_CAP = 31
    # constants determining weight value shift
    POSITIVE = 0.2       # added to weight if yes
    NEGATIVE = 0.1       # subtracted from weight if no
    # constant defining minimum possible weight value
    MINIMUM_WEIGHT = 0.1

    while True:
        draw_gradient_background(SCREEN, DARKGREY, DARKGREY)
        mouse_pos = pygame.mouse.get_pos()

        # YES / NO buttons
        no_button  = Button("NO",  (285, 360), get_font(75), BLACK, DARKGREY, None)
        yes_button = Button("YES", (1015, 360), get_font(75), BLACK, DARKGREY, None)
        for btn in (no_button, yes_button):
            btn.change_color(mouse_pos)
            pygame.draw.rect(SCREEN, WHITE, btn.rect, border_radius=15)
            pygame.draw.rect(SCREEN, BLACK, btn.rect, 2, border_radius=15)
            btn.update(SCREEN)

        # DONATE button (bottom-left)
        donate_btn = Button("DONATE", (0, 0), get_font(50), BLACK, DARKGREY, None)
        donate_btn.rect.bottomleft = (30, HEIGHT - 30)
        donate_btn.change_color(mouse_pos)
        pygame.draw.rect(SCREEN, WHITE, donate_btn.rect, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, donate_btn.rect, 2, border_radius=15)
        donate_btn.update(SCREEN)

        # events
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # only relevant user input event (mouse button down)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # prioritize button hits first
                if donate_btn.check_for_input(event.pos):
                    MONEY_CENTS += 500 * 100  # +$500.00
                # event for user pressing no button
                elif no_button.check_for_input(event.pos):
                    MONEY_CENTS += 5          # +$0.05
                    
                    # shift weight value of current product (subtract)
                    weight = current_product[1] - NEGATIVE
                    # edge case so that weight never goes below a minimum value
                    if weight < MINIMUM_WEIGHT:
                        weight = 0.1
                    
                    products[current_product[3]][1] = weight
                    
                    # check idx counter, if higher than the amount of products in product list then
                    # default to algorithmic image fetching. otherwise, iterate through one cycle of
                    # ads such that each product is represented once.
                    if idx < (len(products) - 1):
                        # increment counter and set new values
                        idx += 1
                        current_product = products[idx]
                        current_img = load_scaled(get_random_ad(current_product))
                    # case where counter is higher than the length of products list
                    # this will happen after the intended 'loop' at the beginning of the ad cycle
                    # after the initial loop, all ads will be determined using the get_ad method
                    else:
                        # increment such that the ads cap is eventually reached
                        idx += 1
                        current_product = get_ad()
                        # debug
                        if DEBUG:
                            print(current_product[0])
                        current_img = load_scaled(get_random_ad(current_product))
                    
                    # go to final screen if ad cap is reached (maximum amount of intended ads has run)
                    if idx >= ADS_CAP:
                        final_screen()
                        return
                    
                    # old code
                    # current_img = IMAGES[idx]
                # event for user pressing yes button
                elif yes_button.check_for_input(event.pos):
                    MONEY_CENTS += 5          # +$0.05
                    
                    # shift weight value of current product (add)
                    weight = current_product[1] + POSITIVE       
                    products[current_product[3]][1] = weight
                    
                    # check idx counter, if higher than the amount of products in product list then
                    # default to algorithmic image fetching. otherwise, iterate through one cycle of
                    # ads such that each product is represented once.
                    if idx < (len(products) - 1):
                        # increment counter and set new values
                        idx += 1
                        current_product = products[idx]
                        current_img = load_scaled(get_random_ad(current_product))
                    # case where counter is higher than the length of products list
                    # this will happen after the intended 'loop' at the beginning of the ad cycle
                    # after the initial loop, all ads will be determined using the get_ad method
                    else:
                        # increment such that the ads cap is eventually reached
                        idx += 1
                        current_product = get_ad()
                        if DEBUG:
                            print(current_product[0])
                        current_img = load_scaled(get_random_ad(current_product))
                    
                    # go to final screen if ad cap is reached (maximum amount of intended ads has run)
                    if idx >= ADS_CAP:
                        final_ad_page(5)
                        final_screen()
                        return
                    
                    # old code
                    # current_img = IMAGES[idx]    
                
                else:
                    # anywhere else -> partner page for 5s, then return here
                    show_partner_page(5)

        # draw current image + money
        SCREEN.blit(current_img, current_img.get_rect(center=SCREEN.get_rect().center))
        money_surf = get_font(36).render(format_money(MONEY_CENTS), True, WHITE)
        SCREEN.blit(money_surf, (20, 20))

        pygame.display.update()






def show_partner_page(seconds: int = 5):
    """Show a Partner Page with 6 main partners arranged nicely for `seconds`, then return."""
    end_time = pygame.time.get_ticks() + seconds * 1000
    title_surf = get_font(64).render("Partner Page", True, WHITE)
    title_rect = title_surf.get_rect(midtop=(WIDTH // 2, 40))

    partners = [
        ("Google",      (66, 133, 244)),   # Blue
        ("Meta",        (59, 89, 152)),    # Facebook Blue
        ("Amazon",      (255, 153, 0)),    # Orange
        ("Apple",       (153, 153, 153)),  # Grey
        ("TikTok",      (255, 59, 92)),    # Pinkish Red
        ("Twitter",     (29, 161, 242))    # Light Blue
    ]

    partner_surfs = []
    y_positions = [400, 400, 400, 700, 700, 700]
    x_positions = [WIDTH // 4, WIDTH // 2, (WIDTH * 3) // 4,
                   WIDTH // 4, WIDTH // 2, (WIDTH * 3) // 4]

    # render names
    for i, (name, color) in enumerate(partners):
        surf = get_font(48).render(name, True, color)
        rect = surf.get_rect(center=(x_positions[i], y_positions[i] - 120))
        partner_surfs.append((surf, rect))

    # main display loop
    while pygame.time.get_ticks() < end_time:
        SCREEN.fill(BLACK)
        SCREEN.blit(title_surf, title_rect)
        for surf, rect in partner_surfs:
            SCREEN.blit(surf, rect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.update()
        pygame.time.delay(16) 


def final_ad_page(seconds: int = 5):
    """Show an Ad Page before the final page for `seconds`, then return."""
    end_time = pygame.time.get_ticks() + seconds * 1000

    # get final image 
    weights = []
    
    # create list of all weights with indices correlating to products list
    for product in products:
        weights.append(product[1])
    
    # track index value of chosen product type
    index = 0
    # find highest weight value
    for i in range(len(weights)):
        if products[i][1] > products[index][1]:
            index = i
        # case for identical values. choose one at random
        elif products[i][1] == products[index][1]:
            if random.randint(1, 2) == 1:
                index = i
                
    # get final ad
    final_ad = load_scaled(FINAL_ADS[index])
    
    # main display loop
    while pygame.time.get_ticks() < end_time:
        SCREEN.fill(DARKGREY)
        SCREEN.blit(final_ad, final_ad.get_rect(center=SCREEN.get_rect().center))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.update()
        pygame.time.delay(16) 




# Login screen
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
        placeholder="*****",
        bg_color=WHITE,
        border_color=BLACK,
        border_color_active=ROYALBLUE,
        is_password=True,
        radius=15,
        max_len=5     # limit to 5 characters
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











def final_screen():
    global MONEY_CENTS

    # Final Screen
    line1 = get_font(48).render("Thanks we sold your data to", True, WHITE)
    line2 = get_font(48).render("Google, Meta, and 45 other companies!", True, WHITE)

    while True:
        draw_gradient_background(SCREEN, DARKGREY, DARKGREY)

        # Center message
        SCREEN.blit(line1, line1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        SCREEN.blit(line2, line2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        # Money Counter 
        money_text = get_font(40).render(f"Total: {format_money(MONEY_CENTS)}", True, WHITE)
        money_rect = money_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
        SCREEN.blit(money_text, money_rect)

        # restart button
        restart_btn = Button("RESTART", (0, 0), get_font(50), BLACK, DARKGREY, adscreen)
        restart_btn.rect.midbottom = (
            money_rect.right + 100 + restart_btn.rect.width // 2,
            money_rect.bottom
        )

        # exit button
        exit_btn = Button("EXIT", (0, 0), get_font(50), BLACK, DARKGREY, main_menu)
        exit_btn.rect.midbottom = (
            money_rect.left - 100 - exit_btn.rect.width // 2,  # mirror spacing
            money_rect.bottom
        )

        # draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in (exit_btn, restart_btn):
            btn.change_color(mouse_pos)
            pygame.draw.rect(SCREEN, WHITE, btn.rect, border_radius=15)
            pygame.draw.rect(SCREEN, BLACK, btn.rect, 2, border_radius=15)
            btn.update(SCREEN)

        # reset product weight values for next cycle
        reset_weights()

        # restart / exit Button events
        # resart = back to adscreen
        # exit = back to menu page
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.check_for_input(mouse_pos):
                    restart_btn.callback()
                    return
                if exit_btn.check_for_input(mouse_pos):
                    exit_btn.callback()
                    return

        pygame.display.update()








# Main Menu screen
def main_menu():
    while True:
        draw_gradient_background(SCREEN, (255, 69, 0, 255), (220, 20, 60, 255))
        mouse_pos = pygame.mouse.get_pos()

        # menu title
        title_text = get_font(100).render("AD TINDER", True, WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        SCREEN.blit(title_text, title_rect)

        # start / exit buttons
        start_button = Button("START", (640, 325), get_font(75), BLACK, BLACK, login)
        quit_button = Button("QUIT", (640, 475), get_font(75), BLACK, BLACK, sys.exit)

        for button in [start_button, quit_button]:
            button.change_color(mouse_pos)
            pygame.draw.rect(SCREEN, WHITE, button.rect, border_radius=15)
            pygame.draw.rect(SCREEN, BLACK, button.rect, 4, border_radius=15)
            button.update(SCREEN)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(mouse_pos):
                    start_button.callback()
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit(); sys.exit()

        pygame.display.update()

main_menu()
