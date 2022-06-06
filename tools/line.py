from util import Vector
from math import atan2, sqrt, sin, cos
from tools.tool import Tool

def vector_angle(vector, origin = Vector(0)):
  vn = vector - origin
  return atan2(vn.y, vn.x)

def rotate_vector(vector, origin = Vector(0), angle = 0):
  vn = vector - origin
  distance = sqrt(vn.x ** 2 + vn.y ** 2)
  new_angle = vector_angle(vn) + angle
  return Vector(cos(new_angle) * distance, sin(new_angle) * distance) + origin
  
def set_polygon_line_coords(canvas, id, v0, v1, width):
  origin = (v0 + v1) / Vector(2)
  vn = v1 - v0
  distance = sqrt(vn.x ** 2 + vn.y ** 2) + width
  angle = vector_angle(v0, v1)
  c = [
    rotate_vector(Vector(distance / 2, width / 2), angle = angle) + origin,
    rotate_vector(Vector(distance / 2, -width / 2), angle = angle) + origin,
    rotate_vector(Vector(-distance / 2, -width / 2), angle = angle) + origin,
    rotate_vector(Vector(-distance / 2, width / 2), angle = angle) + origin
  ]
  canvas.coords(id, c[0].x, c[0].y, c[1].x, c[1].y, c[2].x, c[2].y, c[3].x, c[3].y)
  
class Line(Tool):
  def __init__(self, editor):
    super().__init__(editor)
    self.size = 5
    self.make_cursor()
    self.current_line = None
    self.current_anchor = None
    self.deselect()

  def make_cursor(self):
    self.cursor = self.editor.canvas.create_oval(-100, -100, self.size - 100, self.size - 100, fill = self.editor.primary_color)
    
  def update(self):
    self.editor.canvas.tag_raise(self.cursor)
    self.editor.canvas.itemconfig(self.cursor, fill = self.editor.primary_color)

  def set_size(self, size):
    self.size = size

  def get_scaled_size(self):
    return self.size * self.editor.window.canvas_scale
    
  def select(self):
    self.update()
    self.editor.canvas.itemconfig(self.cursor, state = "normal")
    self.editor.canvas.update()

  def deselect(self):
    self.editor.canvas.itemconfig(self.cursor, state = "hidden")
    self.editor.canvas.update()

  def handle_motion(self, position):
    self.editor.canvas.coords(self.cursor, position.x - self.get_scaled_size() / 2, position.y - self.get_scaled_size() / 2, position.x + self.get_scaled_size() / 2, position.y + self.get_scaled_size() / 2)
    
  def handle_lbdown(self, position):
    self.current_anchor = position
    self.current_line = self.editor.canvas.create_polygon(0, 0, 0, 0, fill = self.editor.primary_color)
    set_polygon_line_coords(self.editor.canvas, self.current_line, self.current_anchor, self.current_anchor, self.get_scaled_size())
    self.editor.new_action()
    self.editor.add_to_action(self.current_line)

  def handle_lbmotion(self, position):
    self.handle_motion(position)
    set_polygon_line_coords(self.editor.canvas, self.current_line, self.current_anchor, position, self.get_scaled_size())
