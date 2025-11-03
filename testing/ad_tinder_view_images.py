# Steven Alleman
# Displays Ads and you can click through them and it shows the reslut of all YES clicks

import sys, pygame

EXT = ".jpg"
WIDTH, HEIGHT = 960, 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 28)

# List of dictionaries, each dic holds source file path and category 
AD_ITEMS = [
    {"src": "images/phone1"  + EXT, "category": "Phone"},
    {"src": "images/shirt1"  + EXT, "category": "Shirt"},
    {"src": "images/shirt2"  + EXT, "category": "Shirt"},
    {"src": "images/shirt3"  + EXT, "category": "Shirt"},
    {"src": "images/shirt4"  + EXT, "category": "Shirt"},
    {"src": "images/shoe1"   + EXT, "category": "Shoe"},
    {"src": "images/shoe2"   + EXT, "category": "Shoe"},
    {"src": "images/shoe3"   + EXT, "category": "Shoe"},
    {"src": "images/shoe4"   + EXT, "category": "Shoe"},
    {"src": "images/shoe5"   + EXT, "category": "Shoe"},
    {"src": "images/shoe6"   + EXT, "category": "Shoe"},
    {"src": "images/tv1"     + EXT, "category": "TV"},
    {"src": "images/tv2"     + EXT, "category": "TV"},
    {"src": "images/tv3"     + EXT, "category": "TV"},
    {"src": "images/tv4"     + EXT, "category": "TV"},
    {"src": "images/tv5"     + EXT, "category": "TV"},
    {"src": "images/watch1"  + EXT, "category": "Watch"},
    {"src": "images/watch2"  + EXT, "category": "Watch"},
    {"src": "images/watch3"  + EXT, "category": "Watch"},
    {"src": "images/watch4"  + EXT, "category": "Watch"},
]

# simple layout
LEFT_BTN  = pygame.Rect(60, HEIGHT-80, 160, 50)
RIGHT_BTN = pygame.Rect(WIDTH-220, HEIGHT-80, 160, 50)
VIEW = pygame.Rect(40, 40, WIDTH-80, HEIGHT-120)

def draw_button(rect, label):
    pygame.draw.rect(screen, (225,225,225), rect, border_radius=10)
    txt = font.render(label, True, (0,0,0))
    screen.blit(txt, txt.get_rect(center=rect.center))

def load_scaled(path):
    img = pygame.image.load(path).convert()
    w, h = img.get_size()
    s = min(VIEW.width / w, VIEW.height / h)
    return pygame.transform.smoothscale(img, (int(w*s), int(h*s)))

# state
idx = 0
yes = {"TV":0, "Shoe":0, "Shirt":0, "Watch":0, "Phone":0}
done = False
current_img = load_scaled(AD_ITEMS[0]["src"])

# main loop
while True:
    for e in pygame.event.get():  # new events/mouse click
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if not done and e.type == pygame.MOUSEBUTTONDOWN:
            if LEFT_BTN.collidepoint(e.pos):            # NO
                idx += 1
            elif RIGHT_BTN.collidepoint(e.pos):         # YES
                yes[AD_ITEMS[idx]["category"]] += 1
                idx += 1
            if idx >= len(AD_ITEMS):
                done = True
            else:
                current_img = load_scaled(AD_ITEMS[idx]["src"])

    screen.fill((245,246,248))

    if not done:
        # image + buttons + caption
        screen.blit(current_img, current_img.get_rect(center=VIEW.center))
        draw_button(LEFT_BTN,  "Left (No)")
        draw_button(RIGHT_BTN, "Right (Yes)")
        cap = font.render(f"{idx+1}/{len(AD_ITEMS)} – {AD_ITEMS[idx]['category']}", True, (60,60,70))
        screen.blit(cap, (16, 8))
    else:
        # results
        y = 160
        title = font.render("Results", True, (0,0,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        for cat in ("TV","Shoe","Shirt","Watch","Phone"):
            line = font.render(f"{cat}: {yes[cat]}", True, (0,0,0))
            screen.blit(line, (WIDTH//2 - 60, y)); y += 36
        hint = font.render("Exit with X", True, (90,90,90))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-50))

    pygame.display.flip()
