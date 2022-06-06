from util import Vector
from tools.tool import Tool

class Eraser(Tool):
  def __init__(self, editor):
    super().__init__(editor)
    self.size = 5
    self.make_cursor()
    self.deselect()

  def make_cursor(self):
    self.cursor = self.editor.canvas.create_rectangle(0, 0, 0, 0, fill = "#000000")
    
  def get_scaled_size(self):
    return self.size * self.editor.window.canvas_scale

  def set_size(self, size):
    self.size = size

  def update(self):
    self.editor.canvas.tag_raise(self.cursor)

  def select(self):
    self.update()
    self.editor.canvas.itemconfig(self.cursor, state = "normal")
    self.editor.canvas.update()

  def deselect(self):
    self.editor.canvas.itemconfig(self.cursor, state = "hidden")
    self.editor.canvas.update()

  def handle_motion(self, position):
    self.editor.canvas.coords(self.cursor, position.x - self.get_scaled_size() / 2, position.y - self.get_scaled_size() / 2, position.x + self.get_scaled_size() / 2, position.y + self.get_scaled_size() / 2)
    
  def erase(self, position):
    for object in self.editor.canvas.find_overlapping(position.x - self.size / 2, position.y - self.size / 2, position.x + self.size / 2, position.y + self.size / 2):
      if object == self.cursor:
        continue
      self.editor.add_to_action(object, "deletion")
      self.editor.canvas.itemconfig(object, state = "hidden")

  def handle_lbdown(self, position):
    self.editor.new_action()
    self.erase(position)

  def handle_lbmotion(self, position):
    self.handle_motion(position)
    self.erase(position)
