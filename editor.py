from util import Vector
import tools

class Editor:
  def __init__(self):
    self.window = None
    self.canvas_size = Vector(480, 480)
    self.actual_canvas_size = self.canvas_size.copy()
    self.canvas = None
    self.primary_color = "#000000"
    self.secondary_color = "#FFFFFF"
    self.action_history = []
    self.undo_history = []

  def init(self, window):
    self.window = window
    self.canvas = window.canvas
    self.tools = {
      "pen" : tools.Pen(self),
      "brush" : tools.Brush(self),
      "line" : tools.Line(self),
      "rectangle" : tools.Shape(self, lambda : self.canvas.create_rectangle(0,0,0,0, fill = self.primary_color, width = 0)),
      "ellipse" : tools.Shape(self, lambda : self.canvas.create_oval(0,0,0,0, fill = self.primary_color, width = 0)),
      "recolor" : tools.Recolor(self),
      "eraser" : tools.Eraser(self)
    }
    self.last_tool_name = None
    self.current_tool_name = "eraser"
    self.select_tool("pen")

  def handle_lbdown(self, position):
    self.current_tool.handle_lbdown(position)

  def handle_lbup(self, position):
    self.current_tool.handle_lbup(position)
    
  def handle_lbmotion(self, position):
    self.current_tool.handle_lbmotion(position)

  def handle_motion(self, position):
    self.current_tool.handle_motion(position)

  def handle_rbdown(self, position):
    pass

  def select_tool(self, tool):
    tools = self.tools.keys()
    if not tool in tools: return
    for x in tools:
      if x != tool:
        self.tools[x].deselect()
    self.current_tool = self.tools[tool]
    self.current_tool.select()
    self.last_tool_name = self.current_tool_name
    self.current_tool_name = tool

  def select_last_tool(self):
    self.select_tool(self.last_tool_name)

  def undo_action(self, action):
    if action[1] == "creation":
      self.canvas.itemconfig(action[0], state = "hidden")
      return [action[0], "deletion"]
    elif action[1] == "deletion":
      self.canvas.itemconfig(action[0], state = "normal")
      return [action[0], "creation"]
    elif action[1] == "recolor":
      current_color = self.canvas.itemcget(action[0], "fill")
      self.canvas.itemconfig(action[0], fill = action[2])
      return [action[0], "recolor", current_color]
    
  def undo(self):
    if len(self.action_history) == 0: return
    reverse_actions = []
    for action in self.action_history[-1]:
      reverse_actions.append(self.undo_action(action))
    
    self.undo_history.append(reverse_actions)
    self.action_history.pop()

  def redo(self):
    if len(self.undo_history) == 0: return
    reverse_actions = []
    for action in self.undo_history[-1]:
      reverse_actions.append(self.undo_action(action))
    
    self.action_history.append(reverse_actions)
    self.undo_history.pop()

  def add_to_action(self, id, action_name = "creation", data = None):
    if len(self.action_history) == 0: self.new_action()
    self.action_history[-1].append([id, action_name, data])

  def new_action(self):
    self.action_history.append([])
    self.erase_undo_history()

  def set_primary_color(self, color):
    self.primary_color = color
    for tool in self.tools.values():
      tool.update()

  def set_current_tool_size(self, size):
    try:
      int(size)
      self.current_tool.set_size(size)
    except:
      pass

  def remake_cursors(self):
    for tool in self.tools.values():
      tool.make_cursor()

  def erase_undo_history(self):
    for action in self.undo_history:
      for i in action:
        if action[1] == "deletion":
          self.canvas.delete(action[0])
    self.undo_history = []


  def on_clear_canvas(self):
    self.action_history = []
    self.undo_history = []
    self.remake_cursors()

  def inc_size(self):
    self.current_tool.set_size(self.current_tool.size + 1)

  def dec_size(self):
    self.current_tool.set_size(self.current_tool.size - 1)
