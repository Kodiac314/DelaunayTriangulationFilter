
from GeneratePoints import generate_pts
from GenerateMesh import bowyer_watson, bowyer_watson_slowmo
from pyautogui import size as pyautogui_size
import pygame
from random import randrange, random
Point = tuple[int, int]
pygame.init()


''' ----- SETTINGS ----- '''
# Pick two images to be merged
IMG1     = 'lake.jpg'
IMG2     = 'wolf2.jpg'
QUALITY  = 'HD'          # LD | SD | HD | UHD

# Advanced settings
MIX         = 'blend'    # Blend | Chop
MODE        = 'uniform'  # Grid | Uniform | Dynamic
BUFFER      = 1          # extra space on border of image
SHOW_STEPS  = True       # Final result is faster if off, fun to watch if True


''' ----- INIT ----- '''
# Get device screen dimensions and init display
MAX_WIDTH, MAX_HEIGHT = pyautogui_size()
MAX_WIDTH, MAX_HEIGHT = round(MAX_WIDTH * 0.8), round(MAX_HEIGHT * 0.8)
dis = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

# Load image, calculate scale to screen dimensions
BG1 = pygame.image.load(IMG1).convert_alpha()
W1, H1 = BG1.get_size()
W1 = round(W1 * MAX_HEIGHT / H1)
while 2*W1 <= MAX_WIDTH: W1 *= 2

BG2 = pygame.image.load(IMG2).convert_alpha()
W2, H2 = BG2.get_size()
W2 = round(W2 * MAX_HEIGHT / H2)
while 2*W2 <= MAX_WIDTH: W2 *= 2

WIDTH, HEIGHT = (W1 + W2) // 2, MAX_HEIGHT

# Update image and display to scaled dimensions
BG1 = pygame.transform.scale(BG1, (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(BG2, (WIDTH, HEIGHT))
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delaunay Triangulation Mixer")

# Init NUM_PTS and pts
PT_DENSITY = {'LD' : 0.5, 'SD' : 1, 'HD' : 2, 'UHD' : 3}
NUM_PTS = int((WIDTH // 10) * (HEIGHT // 10) * PT_DENSITY[QUALITY])
pts = generate_pts(BG1, MODE, NUM_PTS, BUFFER)


''' ----- Render ----- '''
def color(midpoint: Point):
    x = max(0, min(round(midpoint[0]) - BUFFER, WIDTH-1))
    y = max(0, min(round(midpoint[1]) - BUFFER, HEIGHT-1))
    
    match MIX:
        case 'chop':
            return BG1.get_at((x, y)) if random() < 0.5 else BG2.get_at((x, y))
        case 'blend':
            r1, g1, b1, a1 = BG1.get_at((x, y))
            r2, g2, b2, a2 = BG2.get_at((x, y))
            return (r1+r2) // 2, (g1+g2) // 2, (b1+b2) // 2, (a1+a2) // 2
    

''' Game Loop '''
clock = pygame.time.Clock()

if SHOW_STEPS: mesh_iter = bowyer_watson_slowmo(pts, [WIDTH, HEIGHT, BUFFER])

run = True
pause = False
frame = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pts = generate_pts(BG, MODE, NUM_PTS, BUFFER)
                render()
            if event.key == pygame.K_s:
                name1, extension = IMG1.split('.')
                name2, _         = IMG2.split('.')
                pygame.image.save(dis, f"Stylized/Mixer_{name1}_{name2}_{QUALITY}.{extension}")
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_f:
                print(f"{frame}/{NUM_PTS} ({frame/NUM_PTS*100:.2f}%)")

    if pause: continue
    
    if SHOW_STEPS:
        try:
            mesh = next(mesh_iter)
        except:
            pause = True
            continue
        frame += 1
        updateRect = [0, 0, WIDTH, HEIGHT]
        for triangle in mesh:
            x, y = zip(*triangle.points)
            midpt = (sum(x) / 3, sum(y) / 3)
            pygame.draw.polygon(dis, color(midpt), triangle.points)
            
            updateRect[0] = min(updateRect[0], min(x))
            updateRect[1] = min(updateRect[1], min(y))
            updateRect[2] = max(updateRect[2], max(x))
            updateRect[3] = max(updateRect[3], max(y))
        pygame.display.update(updateRect[0], updateRect[1], updateRect[2]-updateRect[0], updateRect[3]-updateRect[1])
    else:
        mesh = bowyer_watson(pts, [WIDTH, HEIGHT, BUFFER])
        for triangle in mesh:
            x, y = zip(*triangle.points)
            midpt = (sum(x) / 3, sum(y) / 3)
            pygame.draw.polygon(dis, color(midpt), triangle.points)
        pygame.display.update()
        pause = True

exit()


