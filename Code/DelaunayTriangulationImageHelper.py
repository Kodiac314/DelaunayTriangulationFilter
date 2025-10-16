# DelaunayTriangulationImage::helper

from random import sample, randrange

global_pts = []

def generate_pts(BG, mode, num_pts, buffer):
    
    W, H = BG.get_size()
    
    match (mode.lower()):
        
        case 'grid':
            return [(x, y)
                for x in range(0, W + 1, buffer)
                for y in range(0, H + 1, buffer)]
        
        
        case 'uniform':
            return [(x + randrange(buffer), y + randrange(buffer))
                    for x in range(0, W, buffer)
                    for y in range(0, H, buffer)]
        
        
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
            for i in range(-buffer, W + buffer + 1, buffer):
                res.append((i, 0))
            for i in range(0, H + 1, buffer):
                res.append((0, i))
            return res
        
        
        case _: # fully random
            return [(randrange(W), randrange(H))
                    for x in range(0, W + gap-1, gap)
                    for y in range(0, H + gap-1, gap)]
