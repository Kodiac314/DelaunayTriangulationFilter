from random import choices, shuffle, randrange
from math import sqrt

W = H = 0

def sort(arr: list[int]) -> None:
    shuffle(arr)
#     arr.sort(key = lambda item :
#         sqrt((item[0] - W//2)**2 + (item[1] - H//2)**2) // 50,
#              reverse=True)

dynamic_pts = []
dynamic_weights = []

def generate_pts(BG, mode, num_pts, buffer):
    global W, H
    W, H = BG.get_size()
    
    match (mode.lower()):
        
        case 'grid':
            pts_x = round(sqrt(num_pts * W / H))
            step_x = W // pts_x
            step_y = H // round(num_pts / pts_x)
            
            res = [(x, y)
                    for x in range(0, W, step_x)
                    for y in range(0, H, step_y)]
            sort(res)
            return res
        
        
        case 'uniform':
            pts_x = round(sqrt(num_pts * W / H))
            step_x = W // pts_x
            step_y = H // round(num_pts / pts_x)
            
            res = [(x + randrange(step_x), y + randrange(step_y))
                    for x in range(-step_x, W+step_x, step_x)
                    for y in range(-step_y, H+step_y, step_y)]
            sort(res)
            return res
        
        
        case 'dynamic':
            if not dynamic_pts:
                
                def c_dist(color1, color2):
                    return sum(abs(a - b) for a, b in zip(color1, color2))
                
                upval = [BG.get_at((x, 0)) for x in range(W)]
                
                for y in range(1, H):
                    prev = BG.get_at((0, y))
                    for x in range(1, W):
                        col = BG.get_at((x, y))
                        
                        lf = c_dist(prev, col)
                        up = c_dist(upval[x], col)
                        
                        dynamic_pts.append((x, y))
                        dynamic_weights.append(lf + up)
                        
                        prev = upval[x] = col
            
            res = []
            
            pts_x = round(sqrt(num_pts * W / H))
            step_x = W // pts_x * 4
            step_y = H // round(num_pts / pts_x) * 4
            
            for x in range(-step_x, W+step_x, step_x):
                res.append((x, -step_y))
                res.append((x, H+step_y))
            for y in range(0, H, step_y):
                res.append((-step_x, y))
                res.append((W+step_x, y))
            
            res += choices(dynamic_pts, weights=dynamic_weights, k=num_pts)
            return res
        
        
        case _: # fully random
            return [(randrange(-buffer, W + buffer), randrange(-buffer, H + buffer))
                    for _ in range(num_pts)]


