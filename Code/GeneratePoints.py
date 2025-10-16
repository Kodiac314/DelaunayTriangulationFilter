from random import sample, shuffle, randrange
from math import sqrt

global_pts = []

def generate_pts(BG, mode, num_pts, buffer):
    
    W, H = BG.get_size()
    
    match (mode.lower()):
        
        case 'grid':
            step_x = round(sqrt(num_pts * W / H))
            step_y = round(num_pts / step_x)
            res = [(x, y)
                    for x in range(0, W, W // step_x)
                    for y in range(0, H, H // step_y)]
            shuffle(res)
            return res
        
        
        case 'uniform':
            pts_x = round(sqrt(num_pts * W / H))
            step_x = W // pts_x
            step_y = H // round(num_pts / pts_x)
            
            res = [(x + randrange(step_x), y + randrange(step_y))
                    for x in range(0, W, step_x)
                    for y in range(0, H, step_y)]
            shuffle(res)
            return res
        
        
        case 'dynamic':
            if not global_pts:
                
                def c_dist(color1, color2):
                    return sum(abs(a - b) for a, b in zip(color1, color2))
                
                THRESHOLD = 30
                
                for y in range(0, H):
                    prev = BG.get_at((0, 0))
                    for x in range(1, W):
                        col = BG.get_at((x, y))
                        if c_dist(prev, col) >= THRESHOLD:
                            global_pts.append((x, y))
                            prev = col
            
            res = sample(global_pts, num_pts)
            for i in range(-buffer, W + buffer + 1, W // buffer):
                res.append((i, 0))
                res.append((i, H))
            for i in range(0, H + 1, H // buffer):
                res.append((0, i))
                res.append((W, i))
            return res
        
        
        case _: # fully random
            return [(randrange(-buffer, W + buffer), randrange(-buffer, H + buffer))
                    for _ in range(num_pts)]


