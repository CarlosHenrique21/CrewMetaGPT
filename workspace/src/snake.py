"""
Snake entity module.
Manages snake position, movement, growth, and collision detection.
"""

class Snake:
    def __init__(self, initial_positions):
        """
        Initialize the snake with a list of positions.
        Each position is a tuple (x, y) on the grid.
        The first element is the head.
        """
        self.positions = initial_positions  # list of tuples
        self.direction = (1, 0)  # Initially moving right
        self.grow_on_next_move = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        """
        Change the direction of the snake.
        Prevent reversing direction directly.
        """
        current_dx, current_dy = self.direction
        new_dx, new_dy = direction
        # Disallow reversing
        if (current_dx * -1, current_dy * -1) == (new_dx, new_dy):
            return  # Ignore the reverse direction command
        self.direction = direction

    def move(self):
        """
        Move the snake one step in the current direction.
        If grow flag is set, do not remove tail.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Insert new head
        self.positions.insert(0, new_head)

        if self.grow_on_next_move:
            self.grow_on_next_move = False
        else:
            # Remove tail
            self.positions.pop()

    def grow(self):
        """
        Set flag to grow automatically on next move.
        """
        self.grow_on_next_move = True

    def check_self_collision(self):
        """
        Check if the snake's head collides with its body.
        """
        head = self.get_head_position()
        return head in self.positions[1:]  # collision if head in body
