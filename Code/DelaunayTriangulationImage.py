
from GeneratePoints import generate_pts
from GenerateMesh import bowyer_watson, bowyer_watson_slowmo
from pyautogui import size as pyautogui_size
import pygame
from random import randrange
Point = tuple[int, int]
pygame.init()


''' ----- SETTINGS ----- '''
SOURCE_IMG  = 'moose3.jpg' # Upload an image to serve as a background, or leave empty for a color wheel
QUALITY     = 'SD'            # LD (1/2) | SD (1) | HD (2) | UHD (4)

# Advanced settings
MODE        = 'dynamic'  # Grid | Uniform | Dynamic
BUFFER      = 1          # extra space on border of image
SHOW_STEPS  = True       # Final result is faster if off, fun to watch if True


''' ----- INIT ----- '''
# Get device screen dimensions and init display
MAX_WIDTH, MAX_HEIGHT = pyautogui_size()
MAX_WIDTH, MAX_HEIGHT = round(MAX_WIDTH * 0.8), round(MAX_HEIGHT * 0.8)
dis = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

# Load image, calculate scale to screen dimensions
BG = pygame.image.load(SOURCE_IMG).convert_alpha()
WIDTH, HEIGHT = BG.get_size()
WIDTH, HEIGHT = round(WIDTH * MAX_HEIGHT / HEIGHT), MAX_HEIGHT
while 2*WIDTH <= MAX_WIDTH: WIDTH *= 2

# Update image and display to scaled dimensions
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delaunay Triangulation Filter")

# Init NUM_PTS and pts
PT_DENSITY = {'LD' : 0.5, 'SD' : 1, 'HD' : 2, 'UHD' : 3}
NUM_PTS = int((WIDTH // 10) * (HEIGHT // 10) * PT_DENSITY[QUALITY])
pts = generate_pts(BG, MODE, NUM_PTS, BUFFER)


''' ----- Render ----- '''
def color(midpoint: Point):
    x = max(0, min(round(midpoint[0]) - BUFFER, WIDTH-1))
    y = max(0, min(round(midpoint[1]) - BUFFER, HEIGHT-1))
    return BG.get_at((x, y))
    

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
                name, extension = SOURCE_IMG.split('.')
                pygame.image.save(dis, f"Stylized/{name}_{MODE}_{QUALITY}.{extension}")
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


