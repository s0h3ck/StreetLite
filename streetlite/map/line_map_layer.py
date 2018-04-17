from kivy.garden.mapview import MapLayer
from kivy.graphics import Color, Ellipse
from kivy.graphics.context_instructions import Translate, Scale

class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 0
        self.lamps = []

    def update(self):
        self.draw_line()

    def clear(self):
        self.lamps = []
        with self.canvas:
            self.canvas.clear()

    def draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom

        scatter = mapview._scatter
        map_source = mapview.map_source
        sx, sy, ss = scatter.x, scatter.y, scatter.scale

        with self.canvas:
            self.canvas.clear()

            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            for lamp in self.lamps:
                screen_lamp = mapview.get_window_xy_from(lamp.lat, lamp.lon, mapview.zoom)
             
                # self.color = lamp.color <--- Why it doesn't work? I'm curious to know :p
                Color(lamp.color.r, lamp.color.g, lamp.color.b, lamp.color.a)
                self.circle = Ellipse(size = (25,25), pos = (screen_lamp))

    def add_circle(self, lamp):
        if lamp in self.lamps:
            for l in self.lamps:
                if l == lamp:
                    self.lamps.remove(lamp)
                    self.lamps.append(l)
                    break
        else:
            self.lamps.append(lamp)
        

#    def reposition(self):
#        mapview = self.parent
#        
#
#        if (self.zoom != mapview.zoom):
#            self.update()
