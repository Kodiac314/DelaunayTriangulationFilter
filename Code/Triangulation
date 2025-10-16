from math import acos, pi, sin, sqrt
import pygame
# import cv2
from random import sample, randrange
from DelaunayTriangulationImageHelper import generate_pts
Point = tuple[int, int]


''' ----- GLOBALS ----- '''
SOURCE_IMG = 'wolf.jpg'  # Upload an image to serve as a background, or leave empty for a color wheel
# sunset.jpg | lake.jpg | wolf.jpg

WIDTH, HEIGHT = 1100, 600  # Dimensions of screen, in pixels
MODE          = 'uniform'  # Grid - perfect grid, Uniform - roughly grid, Dynamic - based on gradient density
NUM_PTS       = 1500       # Number of points used
BUFFER        = 20         # extra space on border of image


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


''' ----- Triangulation Helpers ----- '''
def dist(pt_1: Point, pt_2: Point) -> float:
    return sqrt((pt_1[0] - pt_2[0])**2 + (pt_1[1] - pt_2[1])**2)

class Triangle:
    __slots__ = ('valid', 'points', 'edges', 'center', 'radius')
    
    def __init__(self, pt_a: Point, pt_b: Point, pt_c: Point):
        pt_a, pt_b, pt_c = sorted([pt_a, pt_b, pt_c])
        self.valid = True
        self.points = [pt_a, pt_b, pt_c]
        self.edges = [(pt_a, pt_b), (pt_a, pt_c), (pt_b, pt_c)]
        
        # Side lengths
        a = dist(pt_a, pt_b); b = dist(pt_b, pt_c); c = dist(pt_c, pt_a)
        
        LIM = 1e-8
        if a < LIM or b < LIM or c < LIM:
            self.valid = False
            return
        
        # Angles
        C = acos((b**2 + c**2 - a**2) / (2 * b * c))
        A = acos((a**2 + c**2 - b**2) / (2 * a * c))
        B = acos((a**2 + b**2 - c**2) / (2 * a * b))
        
        # Circumcircle center point and radius
        den = sin(2*A) + sin(2*B) + sin(2*C)
        self.center = (
            (pt_a[0]*sin(2*A) + pt_b[0]*sin(2*B) + pt_c[0]*sin(2*C)) / den,
            (pt_a[1]*sin(2*A) + pt_b[1]*sin(2*B) + pt_c[1]*sin(2*C)) / den
            )
        self.radius = dist(self.center, pt_a)

    def contains(self, pt_d: Point) -> bool:
        return dist(self.center, pt_d) <= self.radius


''' ----- Triangulation Algorithm ----- '''
def bowyer_watson(arr: list[list[int]]) -> list:
    SUPER_TRIANGLE = [(-BUFFER-1, -BUFFER-1), (2 * (WIDTH + BUFFER + 1), -BUFFER-1), (-BUFFER-1, 2 * (HEIGHT + BUFFER + 1))]
    triangulation = set()
    triangulation.add(Triangle(*SUPER_TRIANGLE))
    
    for pt in arr: # add all the points one at a time to the triangulation
        bad_triangles = []
        bad_edge_ct = {}
        for triangle in triangulation: # first find all the triangles that are no longer valid due to the insertion
            if triangle.contains(pt):
                bad_triangles.append(triangle)
                for edge in triangle.edges:
                    bad_edge_ct[edge] = bad_edge_ct.get(edge, 0) + 1
        
        polygon = [edge for (edge, ct) in bad_edge_ct.items() if ct == 1]
        
        for triangle in bad_triangles:
            triangulation.remove(triangle)
        
        for edge in polygon: # replace removed triangles
            new_triangle = Triangle(edge[0], edge[1], pt)
            if new_triangle.valid: # ignore point and line 'triangles'
                triangulation.add(new_triangle)
    outer = []
    for triangle in triangulation:
        if any(pt in SUPER_TRIANGLE for pt in triangle.points):
            outer.append(triangle)
    
    for triangle in outer:
        triangulation.remove(triangle)
    
    return triangulation


''' ----- Render ----- '''
def render():
    dis.blit(BG, (0, 0))
        
    mesh = bowyer_watson(pts)
    # shift = lambda item : (item[0] - BUFFER, item[1] - BUFFER)
    for triangle in mesh:
        midpt = ((triangle.points[0][0] + triangle.points[1][0] + triangle.points[2][0]) / 3,
                 (triangle.points[0][1] + triangle.points[1][1] + triangle.points[2][1]) / 3)
        pygame.draw.polygon(dis, color(midpt), triangle.points)

    pygame.display.update()


''' ----- Game Loop ----- '''
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
