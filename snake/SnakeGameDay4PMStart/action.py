class Action():
    left = (-1, 0)
    up = (0, -1)
    right = (1, 0)
    down = (0, 1)
    
    @staticmethod
    def all():
        return [Action.left, Action.up, Action.right, Action.down]