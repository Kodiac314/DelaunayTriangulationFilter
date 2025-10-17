from math import acos, sin, sqrt
Point = tuple[int, int]


''' ----- Triangulation Helpers ----- '''
def dist(pt_1: Point, pt_2: Point) -> float:
    return sqrt((pt_1[0] - pt_2[0])**2 + (pt_1[1] - pt_2[1])**2)

def dist2(pt_1: Point, pt_2: Point) -> float:
    return (pt_1[0] - pt_2[0])**2 + (pt_1[1] - pt_2[1])**2

class Triangle:
    __slots__ = ('valid', 'points', 'edges', 'center', 'radius2')
    
    def __init__(self, pt_1: Point, pt_2: Point, pt_3: Point):
        pt_1, pt_2, pt_3 = sorted([pt_1, pt_2, pt_3])
        
        self.valid = True
        self.points = [pt_1, pt_2, pt_3]
        self.edges = [(pt_1, pt_2), (pt_1, pt_3), (pt_2, pt_3)]
        
        # Side lengths
        a = dist(pt_1, pt_2); b = dist(pt_2, pt_3); c = dist(pt_3, pt_1)
        
        LIM = 1e-2
        if a < LIM or b < LIM or c < LIM:# or 2*max(a,b,c) < a+b+c:
            self.valid = False
            return
        
        # Angles (law of cosine)
        try:
            angle1 = acos((a**2 + c**2 - b**2) / (2 * a * c))
            angle2 = acos((a**2 + b**2 - c**2) / (2 * a * b))
            angle3 = acos((b**2 + c**2 - a**2) / (2 * b * c))
        except:
            self.valid = False
            return
        
        # Circumcircle center point and radius
        den = sin(2*angle1) + sin(2*angle2) + sin(2*angle3)
        self.center = (
            (pt_1[0]*sin(2*angle1) + pt_2[0]*sin(2*angle2) + pt_3[0]*sin(2*angle3)) / den,
            (pt_1[1]*sin(2*angle1) + pt_2[1]*sin(2*angle2) + pt_3[1]*sin(2*angle3)) / den
            )
        self.radius2 = dist2(self.center, pt_1)

    def contains(self, pt_d: Point) -> bool:
        if not self.valid: raise RuntimeError(f'{self.points} {self.edges}')
        return dist2(self.center, pt_d) <= self.radius2


''' ----- Triangulation Algorithm ----- '''
def bowyer_watson(arr: list[list[int]], dims: list[int]) -> list:
    WIDTH, HEIGHT, BUFFER = dims

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


def bowyer_watson_slowmo(arr: list[list[int]], dims: list[int]) -> list:
    WIDTH, HEIGHT, BUFFER = dims

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
        
        new_triangles = []
        for edge in polygon: # replace removed triangles
            new_triangle = Triangle(edge[0], edge[1], pt)
            if new_triangle.valid: # ignore point and line 'triangles'
                new_triangles.append(new_triangle)
                triangulation.add(new_triangle)
        yield new_triangles
    
    outer = []
    for triangle in triangulation:
        if any(pt in SUPER_TRIANGLE for pt in triangle.points):
            outer.append(triangle)
    
    for triangle in outer:
        triangulation.remove(triangle)
    
    return triangulation
