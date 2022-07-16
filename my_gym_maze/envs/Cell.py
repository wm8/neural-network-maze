class Cell:
    def __init__(self, right, down):
        self.right = right
        self.down = down
        self.up = False
        self.left = False
        self.id = 0
        self.visited = False

