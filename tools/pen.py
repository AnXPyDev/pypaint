from util import Vector
from math import sqrt
from tools.tool import Tool
from tools.line import set_polygon_line_coords

class Pen(Tool):
  def __init__(self, editor):
    super().__init__(editor)
    self.size = 5
    self.last_pos = Vector(0)
    self.make_cursor()
    self.deselect()

  def make_cursor(self):
    self.cursor = self.editor.canvas.create_oval(-100, -100, self.size - 100, self.size - 100, fill = self.editor.primary_color)

  def get_scaled_size(self):
    return self.size * self.editor.window.canvas_scale
    
  def set_size(self, size):
    self.size = size

  def update(self):
    self.editor.canvas.tag_raise(self.cursor)
    self.editor.canvas.itemconfig(self.cursor, fill = self.editor.primary_color)

  def select(self):
    self.update()
    self.editor.canvas.itemconfig(self.cursor, state = "normal")
    self.editor.canvas.update()

  def deselect(self):
    self.editor.canvas.itemconfig(self.cursor, state = "hidden")
    self.editor.canvas.update()

  def handle_motion(self, position):
    self.editor.canvas.coords(self.cursor, position.x - self.get_scaled_size() / 2, position.y - self.get_scaled_size() / 2, position.x + self.get_scaled_size() / 2, position.y + self.get_scaled_size() / 2)
    
  def draw(self, position):
    vn = self.last_pos - position
    distance = sqrt(vn.x ** 2 + vn.y ** 2)
    if distance < self.get_scaled_size() * 4: return
    id = self.editor.canvas.create_polygon(0, 0, 0, 0, fill = self.editor.primary_color)
    set_polygon_line_coords(self.editor.canvas, id, self.last_pos, position, self.get_scaled_size())
    self.editor.add_to_action(id)
    self.last_pos = position

  def handle_lbdown(self, position):
    self.editor.new_action()
    self.last_pos = position
    self.draw(position)

  def handle_lbmotion(self, position):
    self.handle_motion(position)
    self.draw(position)
