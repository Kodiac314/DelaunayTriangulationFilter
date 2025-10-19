# Interactive Delaunay Triangulation

from GenerateMesh import bowyer_watson_slowmo
from pyautogui import size as pyautogui_size
import pygame
from random import randrange
Point = tuple[int, int]
pygame.init()


''' ----- SETTINGS ----- '''
# Upload an image to serve as a background
SOURCE_IMG  = 'doggo.jpg'


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
BUFFER = 1

# Update image and display to scaled dimensions
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delaunay Triangulation Interactive Filter")

# Init NUM_PTS and pts
pts = [(WIDTH//2, HEIGHT//2)]
mesh_iter = bowyer_watson_slowmo(pts, [WIDTH, HEIGHT, 0])


''' ----- Render ----- '''
def color(midpoint: Point):
    x = max(0, min(round(midpoint[0]) - BUFFER, WIDTH-1))
    y = max(0, min(round(midpoint[1]) - BUFFER, HEIGHT-1))
    return BG.get_at((x, y))

def render(x, y):
    pts.append((x, y))
    mesh = next(mesh_iter)
    updateRect = [0, 0, WIDTH, HEIGHT]
    for triangle in mesh:
        X, Y = zip(*triangle.points)
        midpt = (sum(X) / 3, sum(Y) / 3)
        pygame.draw.polygon(dis, color(midpt), triangle.points)
        
        updateRect[0] = min(updateRect[0], min(X))
        updateRect[1] = min(updateRect[1], min(Y))
        updateRect[2] = max(updateRect[2], max(X))
        updateRect[3] = max(updateRect[3], max(Y))
    pygame.display.update(updateRect[0], updateRect[1], updateRect[2]-updateRect[0], updateRect[3]-updateRect[1])
for (x, y) in ((0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)):
    render(x, y)


''' Game Loop '''
clock = pygame.time.Clock()
run = True
frame = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_s:
                name, extension = SOURCE_IMG.split('.')
                pygame.image.save(dis, f"Stylized/{name}_{MODE}_{QUALITY}.{extension}")
            if event.key == pygame.K_f:
                print(f"clicks = {frame}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            render(x, y)
            frame += 1

exit()


