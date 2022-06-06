from util import Vector
from tools.tool import Tool

class Brush(Tool):
  def __init__(self, editor):
    super().__init__(editor)
    self.size = 5
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
    id = self.editor.canvas.create_oval(position.x - self.get_scaled_size() / 2, position.y - self.get_scaled_size() / 2, position.x + self.get_scaled_size() / 2, position.y + self.get_scaled_size() / 2, fill = self.editor.primary_color, width = 0)
    self.editor.add_to_action(id)

  def handle_lbdown(self, position):
    self.editor.new_action()
    self.draw(position)

  def handle_lbmotion(self, position):
    self.handle_motion(position)
    self.draw(position)
