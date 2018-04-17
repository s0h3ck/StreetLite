from enum import Enum

class CustomEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
    
    @classmethod
    def from_value(cls, value):
        found_element = None

        if cls.has_value(value):
            found_element = cls(value)

        return found_element

class Direction(CustomEnum):
    EAST = 0x1
    SOUTH = 0x2
    WEST = 0x3
    NORTH = 0x4

class Action(CustomEnum):
    FLASH_RED = 0x32
    GREEN = 0x33
    FLASH_GREEN = 0x34
    PEDESTRIAN = 0x35
    EMERGENCY = 0x37

class Intersection(CustomEnum):
    A = 0x62
    B = 0x61
    BOTH = 0x63

class Mode(CustomEnum):
    LIVE = 0
    SIMULATION = 1