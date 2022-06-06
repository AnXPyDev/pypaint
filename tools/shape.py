from util import Vector
from tools.tool import Tool

class Shape(Tool):
  def __init__(self, editor, shape_fn):
    super().__init__(editor)
    self.current_anchor = None
    self.current_shape = None
    self.deselect()
    self.shape_fn = shape_fn

  def handle_lbdown(self, position):
    self.current_anchor = position
    self.current_shape = self.shape_fn()
    self.editor.new_action()
    self.editor.add_to_action(self.current_shape)

  def handle_lbmotion(self, position):
    self.editor.canvas.coords(self.current_shape, self.current_anchor.x, self.current_anchor.y, position.x, position.y)
