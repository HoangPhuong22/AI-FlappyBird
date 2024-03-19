from queue import Queue

def gen_path(bird, pipe, velocity):
    start = (bird.rect.x, bird.rect.y, pipe.rect.x, pipe.rect.bottomleft[1], velocity)
    print(bird.rect.x, bird.rect.y, pipe.rect.x, pipe.rect.bottomleft[1], velocity)
    q = Queue()
    q.put(start)
    parent = {start: None}

    while not q.empty():
        current = q.get()
        bx, by, px, py, velocity = current
        if bx >( px + pipe.rect.width):
            return build_path(parent, current)

        for ns in next_states(bx, by, px, py, velocity, bird, pipe):
            if ns not in parent:
                parent[ns] = current
                q.put(ns)

    return []

def next_states(bx, by, px, py, velocity, bird, pipe):
    if velocity > 8:
        velocity = 8
    states = []
    px -= 5
    jump = by - 6
    no_jump = by + velocity
    if bx + bird.rect.width >= px:
        if py < by and (by + bird.rect.height ) < (py + 120):
            states.append((bx, jump, px, py, -6))  # Bird nhảy
            states.append((bx, no_jump, px, py, velocity + 0.3))  # Bird không nhảy
    else:
        if (100 <= no_jump <= 540) and (by < py):
            states.append((bx, no_jump, px, py, velocity + 0.3))  # Bird không nhảy
        elif (100 <= jump <= 540) and (by + bird.rect.height) > (py + 120):
            states.append((bx, jump, px, py, -6))  # Bird nhảy
        elif 100 <= no_jump <= 540: 
            states.append((bx, no_jump, px, py, velocity + 0.3))  # Bird không nhảy
        
    return states

def build_path(parent, end):
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    return path[::-1]
