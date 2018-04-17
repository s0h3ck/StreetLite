from kivy.graphics import Color

class Lamp():
    def __init__(self, intersection, direction, lat, lon):
        self.intersection = intersection
        self.direction = direction
        self.status = "transparent"
        self.lat = lat
        self.lon = lon
        self.color = Color(1,0,0,1)

    def change_status(self, status):
        if status not in ["green", "red", "yellow", "white"]:
            self.status = "transparent"
            self.color = Color(0,0,0,0.0)
        else:
            if status == "green":
                self.color = Color(0,1,0,0.75)
            elif status == "yellow":
                self.color = Color(1,1,0,0.75)
            elif status == "red":
                self.color = Color(1,0,0,0.75)
            elif status == "white":
                self.color = Color(1,1,1,1)
            self.status = status