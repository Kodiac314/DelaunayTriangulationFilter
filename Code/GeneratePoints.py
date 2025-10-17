from random import sample, shuffle, randrange
from math import sqrt

W = H = 0

def sort(arr: list[int]) -> None:
    shuffle(arr)
#     arr.sort(key = lambda item :
#         sqrt((item[0] - W//2)**2 + (item[1] - H//2)**2) // 50,
#              reverse=True)

global_pts = []

def generate_pts(BG, mode, num_pts, buffer):
    global W, H
    W, H = BG.get_size()
    
    match (mode.lower()):
        
        case 'grid':
            step_x = round(sqrt(num_pts * W / H))
            step_y = round(num_pts / step_x)
            res = [(x, y)
                    for x in range(0, W, W // step_x)
                    for y in range(0, H, H // step_y)]
            sort(res)
            return res
        
        
        case 'uniform':
            pts_x = round(sqrt(num_pts * W / H))
            step_x = W // pts_x
            step_y = H // round(num_pts / pts_x)
            
            res = [(x + randrange(step_x), y + randrange(step_y))
                    for x in range(0, W, step_x)
                    for y in range(0, H, step_y)]
            sort(res)
            return res
        
        
        case 'dynamic':
            if not global_pts:
                
                def c_dist(color1, color2):
                    return sum(abs(a - b) for a, b in zip(color1, color2))
                
                THRESHOLD = 30
                
                upval = [BG.get_at((x, 0)) for x in range(W)]
                
                for y in range(1, H):
                    prev = BG.get_at((0, y))
                    for x in range(1, W):
                        col = BG.get_at((x, y))
                        
                        lf = c_dist(prev, col)
                        up = c_dist(upval[x], col)
                        
                        if lf >= THRESHOLD:
                            global_pts.append((x, y))
                            prev = col
                        if up >= THRESHOLD:
                            global_pts.append((x, y))
                            upval[x] = col
            
            res = []
            for i in range(-buffer, W + buffer + 1, W // buffer):
                res.append((i, -buffer))
                res.append((i, H+buffer))
            for i in range(0, H + 1, H // buffer):
                res.append((-buffer, i))
                res.append((W+buffer, i))
            res += sample(global_pts, num_pts)
            return res
        
        
        case _: # fully random
            return [(randrange(-buffer, W + buffer), randrange(-buffer, H + buffer))
                    for _ in range(num_pts)]


