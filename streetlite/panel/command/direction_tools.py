from streetlite.common.constants import Direction

class DirectionTools(object):

    @staticmethod
    def get_facing_direction(direction):
        facing_direction = Direction.SOUTH

        if direction == Direction.EAST:
            facing_direction = Direction.WEST
        elif direction == Direction.SOUTH:
            facing_direction = Direction.NORTH
        elif direction == Direction.WEST:
            facing_direction = Direction.EAST

        return facing_direction

    @staticmethod
    def get_next_direction(direction):
        next_direction = Direction.EAST

        if direction == Direction.EAST:
            next_direction = Direction.SOUTH
        elif direction == Direction.SOUTH:
            next_direction = Direction.WEST
        elif direction == Direction.WEST:
            next_direction = Direction.NORTH

        return next_direction
