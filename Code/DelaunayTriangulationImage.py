import pygame
from random import randrange
from GeneratePoints import generate_pts
from GenerateMesh import bowyer_watson, bowyer_watson_slowmo
Point = tuple[int, int]


''' ----- SETTINGS ----- '''
SOURCE_IMG    = 'lake.jpg' # Upload an image to serve as a background, or leave empty for a color wheel
WIDTH, HEIGHT = 1100, 600  # Dimensions of screen, in pixels
MODE          = 'uniform'  # Grid - perfect grid, Uniform - roughly grid, Dynamic - based on gradient density
NUM_PTS       = 7000       # Number of points used
BUFFER        = 1         # extra space on border of image
SHOW_STEPS    = True


''' ----- INIT PYGAME ----- '''
pygame.init()
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delaunay Triangulation Filter")


''' ----- Background color ----- '''
BG = pygame.image.load(SOURCE_IMG).convert_alpha()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

def color(midpoint: Point):
    x = max(0, min(round(midpoint[0]) - BUFFER, WIDTH-1))
    y = max(0, min(round(midpoint[1]) - BUFFER, HEIGHT-1))
    return BG.get_at((x, y))

pts = generate_pts(BG, MODE, NUM_PTS, BUFFER)


''' ----- Render ----- '''
def render():
    dis.blit(BG, (0, 0))
    pygame.display.update()
    
    if SHOW_STEPS:
        for mesh in bowyer_watson_slowmo(pts, [WIDTH, HEIGHT, BUFFER]):
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


''' Game Loop '''
clock = pygame.time.Clock()
run = True

render()

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
                pygame.image.save(dis, f"{MODE}_{SOURCE_IMG}")

exit()


