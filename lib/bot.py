from pygame import Vector2

# global variables
NUM_DIRE = 4

EMPTY = 0
SNAKE = 1
APPLE = 2
BLOCK = 3

DIRE_LOOKUP = {
    0: (0, -1),  # UP
    1: (-1, 0),  # LEFT
    2: (0, 1),  # DOWN
    3: (1, 0),  # RIGHT
}

VECTOR_LOOKUP = {
    (0, -1): 0,  # UP
    (-1, 0): 1,  # LEFT
    (0, 1): 2,  # DOWN
    (1, 0): 3,  # RIGHT
}


class Bot:
    def __init__(self, map_size) -> None:
        self.map_size = map_size
        self.map = [[[EMPTY] * NUM_DIRE] *
                    self.map_size for _ in range(self.map_size)]

    def reset_graph(self):
        self.map = [[[EMPTY] * NUM_DIRE] *
                    self.map_size for _ in range(self.map_size)]

    def _vector2_to_pair(self, vector):
        return (int(vector.x), int(vector.y))

    def update_graph(self, snake_pos, apple_pos, blocks):
        self.map[int(apple_pos.x)][int(apple_pos.y)] = [APPLE] * NUM_DIRE
        for snk in snake_pos:
            self.map[int(snk.x)][int(snk.y)] = [SNAKE] * NUM_DIRE
        for blk in blocks:
            self.map[int(blk.pos.x)][int(blk.pos.y)] = [BLOCK] * NUM_DIRE

    def get_move(self, snake_pos, snake_dir, tail_last_block_pos, apple_pos, blocks):
        if len(snake_pos) <= 0:
            return None
        self.reset_graph()
        self.update_graph(snake_pos, apple_pos, blocks)
        pos, path_history = self.bfs(snake_pos[0], snake_dir, apple_pos)
        if pos == snake_pos[0]:
            pos, path_history = self.bfs(
                snake_pos[0], snake_dir, tail_last_block_pos)
            if pos == snake_pos[0]:
                pos, path_history = self.dfs(snake_pos[0], snake_dir)
        return self.backtrack(pos, path_history, snake_pos[0])

    def bfs(self, loc, dir, goal):
        queue = []
        prev = {}
        visited = set()

        for k, v in VECTOR_LOOKUP.items():
            if k == (self._vector2_to_pair(-dir)):
                continue
            queue.append((int(loc.x), int(loc.y), v))
            prev[(int(loc.x), int(loc.y), v)] = (-1, -1, -1)

        while len(queue):
            curr_pos = queue.pop(0)
            if curr_pos in visited:
                continue
            x, y, d = curr_pos
            visited.add(curr_pos)

            if Vector2(x, y) == goal:
                return curr_pos, prev

            dir = DIRE_LOOKUP[d]
            next_x = x + dir[0]
            next_y = y + dir[1]

            if next_x < 0 or next_x >= self.map_size or next_y < 0 or next_y >= self.map_size:
                continue

            for i in range(4):
                next_coord = (next_x, next_y, i)
                if next_coord not in visited and (self.map[next_x][next_y][i] == EMPTY or self.map[next_x][next_y][i] == APPLE):
                    prev[next_coord] = (x, y, d)
                    queue.append(next_coord)

        return loc, prev

    def dfs(self, loc, dir):
        queue = []
        history = {}
        visited = set()
        last_pos = (int(loc.x), int(loc.y),
                    VECTOR_LOOKUP[(int(dir.x), int(dir.y))])

        for k, v in VECTOR_LOOKUP.items():
            if k == (self._vector2_to_pair(-dir)):
                continue
            curr_pos = (int(loc.x), int(loc.y), v)
            queue.append(curr_pos)
            history[curr_pos] = (-1, -1, -1)

        while len(queue):
            curr_pos = queue.pop()
            if curr_pos in visited:
                continue
            x, y, d = curr_pos
            visited.add(curr_pos)

            dir = DIRE_LOOKUP[d]
            next_x = x + dir[0]
            next_y = y + dir[1]

            if next_x < 0 or next_x >= self.map_size or next_y < 0 or next_y >= self.map_size:
                continue

            for i in range(4):
                next_coord = (next_x, next_y, i)
                if next_coord not in visited and self.map[next_x][next_y][i] == EMPTY:
                    history[next_coord] = (x, y, d)
                    queue.append(next_coord)
                    last_pos = next_coord

        return last_pos, history

    def backtrack(self, pos, path_history, snake_head):
        while True:
            if pos == (-1, -1, -1):
                return -1
            if path_history[pos][0] == int(snake_head.x) and path_history[pos][1] == int(snake_head.y):
                return path_history[pos][2]
            pos = path_history[pos]

    # def greedy(self, loc, dir):
    #     for k, v in VECTOR_LOOKUP.items():
    #         if k == (self._vector2_to_pair(-dir)):
    #             continue
    #         next_x = int(loc.x + k[0])
    #         next_y = int(loc.y + k[1])
    #         if next_x < 0 or next_x >= self.map_size or next_y < 0 or next_y >= self.map_size:
    #             continue
    #         if (self.map[next_x][next_y][0] == EMPTY or self.map[next_x][next_y][0] == APPLE):
    #             return v

    #     return None
