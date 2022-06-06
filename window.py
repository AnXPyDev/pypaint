from util import Vector
import tkinter
from tkinter import simpledialog
from tkinter import colorchooser

class Window:
  def __init__(self, editor):
    self.editor = editor
    self.toolbar_frame_width = 60
    self.canvas_size = Vector(480)
    self.canvas_position = Vector(0)
    self.last_canvas_scale = 1
    self.canvas_scale = 1
    self.last_canvas_anchor = Vector(0,0)
    # Initialize tkinter elements

    self.root = tkinter.Tk()

    # Initialize menubar
    self.menubar = tkinter.Menu(self.root)

    self.imagemenu = tkinter.Menu(self.menubar, tearoff = 0)
    self.imagemenu.add_command(label = "Resize canvas (Ctrl-S)", command = lambda : self.ask_resize_canvas())
    self.imagemenu.add_command(label = "Resize and rescale contents (Alt-S)", command = lambda : self.ask_resize_and_rescale_canvas())
    self.imagemenu.add_command(label = "Recenter canvas (Ctrl-R)", command = lambda : self.recenter_canvas())
    self.imagemenu.add_command(label = "Fit canvas to frame (Ctrl-F)", command = lambda : self.fit_canvas())
    self.imagemenu.add_command(label = "Zoom in (Ctrl-I)", command = lambda : self.handle_canvas_zoom(120))
    self.imagemenu.add_command(label = "Zoom out (Ctrl-O)", command = lambda : self.handle_canvas_zoom(-120))
    self.imagemenu.add_command(label = "Move canvas left (Ctrl-LeftArrow)", command = lambda : self.handle_move_canvas(self.last_canvas_anchor + Vector(-20, 0)))
    self.imagemenu.add_command(label = "Move canvas right (Ctrl-RightArrow)", command = lambda : self.handle_move_canvas(self.last_canvas_anchor + Vector(20, 0)))
    self.imagemenu.add_command(label = "Move canvas up (Ctrl-UpArrow)", command = lambda : self.handle_move_canvas(self.last_canvas_anchor + Vector(0, -20)))
    self.imagemenu.add_command(label = "Move canvas down (Ctrl-DownArrow)", command = lambda : self.handle_move_canvas(self.last_canvas_anchor + Vector(0, 20)))
    self.imagemenu.add_command(label = "Clear canvas (Ctrl-C)", command = lambda : self.clear_canvas())
    self.menubar.add_cascade(label = "Canvas", menu = self.imagemenu)

    self.toolmenu = tkinter.Menu(self.menubar, tearoff = 0)
    self.toolmenu.add_command(label = "Pen", command = lambda : self.editor.select_tool("pen"))
    self.toolmenu.add_command(label = "Brush", command = lambda : self.editor.select_tool("brush"))
    self.toolmenu.add_command(label = "Line", command = lambda : self.editor.select_tool("line"))
    self.toolmenu.add_command(label = "Rectangle", command = lambda : self.editor.select_tool("rectangle"))
    self.toolmenu.add_command(label = "Ellipse", command = lambda : self.editor.select_tool("ellipse"))
    self.toolmenu.add_command(label = "Recolor", command = lambda : self.editor.select_tool("recolor"))
    self.toolmenu.add_command(label = "Eraser", command = lambda : self.editor.select_tool("eraser"))
    self.toolmenu.add_command(label = "Last tool (Ctrl-Q)", command = lambda : self.editor.select_last_tool())
    self.menubar.add_cascade(label = "Tools", menu = self.toolmenu)

    self.editmenu = tkinter.Menu(self.menubar, tearoff = 0)
    self.editmenu.add_command(label = "Undo (Ctrl-Z)", command = lambda : self.editor.undo())
    self.editmenu.add_command(label = "Redo (Ctrl-Y)", command = lambda : self.editor.redo())
    self.menubar.add_cascade(label = "Edit", menu = self.editmenu)
    
    self.optionsmenu = tkinter.Menu(self.menubar, tearoff = 0)
    self.optionsmenu.add_command(label = "Set primary color", command = lambda : self.set_fg_color())
    self.optionsmenu.add_command(label = "Set background color", command = lambda : self.set_bg_color())
    self.optionsmenu.add_command(label = "Set tool size (Ctrl-T)", command = lambda : self.ask_tool_size())
    self.menubar.add_cascade(label = "Options", menu = self.optionsmenu)

    self.root.config(menu = self.menubar)

    self.toolbar_frame = tkinter.Frame(self.root)
    self.toolbar_frame.pack(side = tkinter.TOP, fill = tkinter.X)
    
    undo_icon = tkinter.PhotoImage(file = "icons/undo.png")
    tkinter.Button(self.toolbar_frame, image = undo_icon, command = lambda : self.editor.undo()).pack(side = tkinter.LEFT)
    redo_icon = tkinter.PhotoImage(file = "icons/redo.png")
    tkinter.Button(self.toolbar_frame, image = redo_icon, command = lambda : self.editor.redo()).pack(side = tkinter.LEFT)

    self.primary_color_button = tkinter.Button(self.toolbar_frame, width = 2, bg = "#000000", command = lambda : self.set_fg_color())
    self.primary_color_button.pack(side = tkinter.LEFT)
    self.background_color_button = tkinter.Button(self.toolbar_frame, width = 2, bg = "#FFFFFF", command = lambda : self.set_bg_color())
    self.background_color_button.pack(side = tkinter.LEFT)

    pen_icon = tkinter.PhotoImage(file = "icons/pen.png")
    tkinter.Button(self.toolbar_frame, image = pen_icon, command = lambda : self.editor.select_tool("pen")).pack(side = tkinter.LEFT)
    brush_icon = tkinter.PhotoImage(file = "icons/brush.png")
    tkinter.Button(self.toolbar_frame, image = brush_icon, command = lambda : self.editor.select_tool("brush")).pack(side = tkinter.LEFT)
    line_icon = tkinter.PhotoImage(file = "icons/line.png")
    tkinter.Button(self.toolbar_frame, image = line_icon, command = lambda : self.editor.select_tool("line")).pack(side = tkinter.LEFT)
    rectangle_icon = tkinter.PhotoImage(file = "icons/rectangle.png")
    tkinter.Button(self.toolbar_frame, image = rectangle_icon, command = lambda : self.editor.select_tool("rectangle")).pack(side = tkinter.LEFT)
    ellipse_icon = tkinter.PhotoImage(file = "icons/ellipse.png")
    tkinter.Button(self.toolbar_frame, image = ellipse_icon, command = lambda : self.editor.select_tool("ellipse")).pack(side = tkinter.LEFT)
    recolor_icon = tkinter.PhotoImage(file = "icons/recolor.png")
    tkinter.Button(self.toolbar_frame, image = recolor_icon, command = lambda : self.editor.select_tool("recolor")).pack(side = tkinter.LEFT)
    eraser_icon = tkinter.PhotoImage(file = "icons/eraser.png")
    tkinter.Button(self.toolbar_frame, image = eraser_icon, command = lambda : self.editor.select_tool("eraser")).pack(side = tkinter.LEFT)
    minus_icon = tkinter.PhotoImage(file = "icons/minus.png")
    tkinter.Button(self.toolbar_frame, image = minus_icon, command = lambda : self.editor.dec_size()).pack(side = tkinter.RIGHT)
    plus_icon = tkinter.PhotoImage(file = "icons/plus.png")
    tkinter.Button(self.toolbar_frame, image = plus_icon, command = lambda : self.editor.inc_size()).pack(side = tkinter.RIGHT)

    self.canvas_frame = tkinter.Frame(self.root, bg = "#202020", width = 640, height = 640)
    self.canvas_frame.pack_propagate(0)
    self.canvas_frame.pack(fill = tkinter.BOTH, expand = 1)
    
    self.canvas = tkinter.Canvas(self.canvas_frame, height = self.canvas_size.x, width = self.canvas_size.y, bg = "#FFFFFF")


    self.canvas.bind("<Motion>", lambda event : self.editor.handle_motion(Vector(event.x, event.y)))
    self.canvas.bind("<ButtonPress-1>", lambda event : self.editor.handle_lbdown(Vector(event.x, event.y)))
    self.canvas.bind("<ButtonRelease-1>", lambda event : self.editor.handle_lbup(Vector(event.x, event.y)))
    self.canvas.bind("<Button-3>", lambda event : self.editor.handle_rbdown(Vector(event.x, event.y)))
    self.canvas.bind("<B1-Motion>", lambda event : self.editor.handle_lbmotion(Vector(event.x, event.y)))
    self.canvas_frame.bind("<ButtonPress-2>", lambda event : self.set_last_canvas_anchor(Vector(event.x, event.y)))
    self.canvas_frame.bind("<ButtonRelease-2>", lambda event : self.handle_move_canvas(Vector(event.x, event.y)))
    self.canvas.bind("<ButtonPress-2>", lambda event : self.set_last_canvas_anchor_c(Vector(event.x, event.y)))
    self.canvas.bind("<ButtonRelease-2>", lambda event : self.handle_move_canvas_c(Vector(event.x, event.y)))

    self.canvas_frame.bind("<MouseWheel>", lambda event : self.handle_canvas_zoom(event.delta))
    self.canvas.bind("<MouseWheel>", lambda event : self.handle_canvas_zoom(event.delta))

    self.root.bind("<Control-z>", lambda event : self.editor.undo())
    self.root.bind("<Control-y>", lambda event : self.editor.redo())
    self.root.bind("<Control-i>", lambda event : self.handle_canvas_zoom(120))
    self.root.bind("<Control-o>", lambda event : self.handle_canvas_zoom(-120))
    self.root.bind("<Up>", lambda event : self.handle_move_canvas(self.last_canvas_anchor + Vector(0, -20)))
    self.root.bind("<Down>", lambda event : self.handle_move_canvas(self.last_canvas_anchor + Vector(0, 20)))
    self.root.bind("<Left>", lambda event : self.handle_move_canvas(self.last_canvas_anchor + Vector(-20, 0)))
    self.root.bind("<Right>", lambda event : self.handle_move_canvas(self.last_canvas_anchor + Vector(20, 0)))

    self.root.bind("<Control-r>", lambda event : self.recenter_canvas())
    self.root.bind("<Control-f>", lambda event : self.fit_canvas())
    self.root.bind("<Control-c>", lambda event : self.clear_canvas())
    self.root.bind("<Control-s>", lambda event : self.ask_resize_canvas())
    self.root.bind("<Alt-s>", lambda event : self.ask_resize_and_rescale_canvas())

    self.root.bind("<Control-q>", lambda event : self.editor.select_last_tool())
    self.root.bind("<Control-t>", lambda event : self.ask_tool_size())

    self.canvas_position = Vector(320)
    self.move_canvas()

    self.editor.init(self)
    self.root.mainloop()

  def set_last_canvas_anchor(self, anchor):
    self.last_canvas_anchor = anchor
    
  def set_last_canvas_anchor_c(self, anchor):
    self.set_last_canvas_anchor(anchor + (self.canvas_position - self.canvas_size / Vector(2)))

  def move_canvas(self):
    self.canvas.place_forget()
    self.canvas.place(x = self.canvas_position.x - (self.canvas_size.x * self.canvas_scale) / 2, y = self.canvas_position.y - (self.canvas_size.y * self.canvas_scale) / 2, width = self.canvas_size.x * self.canvas_scale, height = self.canvas_size.y * self.canvas_scale)

  def handle_move_canvas(self, position):
    self.canvas_position += position - self.last_canvas_anchor
    self.last_canvas_anchor = position
    self.move_canvas()

  def handle_move_canvas_c(self, position):
    self.handle_move_canvas(position + (self.canvas_position - self.canvas_size / Vector(2)))

  def rescale_canvas(self):
    scale_factor = self.canvas_scale / self.last_canvas_scale
    self.canvas.scale("all", 0, 0, scale_factor, scale_factor)
    self.last_canvas_scale = self.canvas_scale
    
  def handle_canvas_zoom(self, delta):
    self.canvas_scale += delta / 1000
    self.move_canvas()
    self.rescale_canvas()
    
  def ask_for_color(self):
    return colorchooser.askcolor()[1]

  def ask_resize_canvas(self, msg = "Resize"):
    try:
      new_size = simpledialog.askstring(msg, "Enter new canvas size, e.g. 1280x720").split("x")
      self.canvas_size = Vector(int(new_size[0]), int(new_size[1]))
      self.move_canvas()
    except:
      pass

  def ask_resize_and_rescale_canvas(self):
    old_size = self.canvas_size
    self.ask_resize_canvas("Resize and rescale contents")
    self.canvas.scale("all", 0, 0, self.canvas_size.x / old_size.x, self.canvas_size.y / old_size.y)

  def clear_canvas(self):
    self.canvas.delete("all")
    self.editor.on_clear_canvas()

  def get_canvas_frame_size(self):
    return Vector(self.canvas_frame.winfo_width(), self.canvas_frame.winfo_height())

  def recenter_canvas(self):
    self.canvas_position = self.get_canvas_frame_size() / Vector(2)
    self.move_canvas()

  def fit_canvas(self):
    frame_size = self.get_canvas_frame_size()
    self.canvas_scale = min(frame_size.x / self.canvas_size.x, frame_size.y / self.canvas_size.y)
    self.rescale_canvas()
    self.recenter_canvas()

  def ask_tool_size(self):
    self.editor.set_current_tool_size(simpledialog.askinteger("Set tool size", "Enter new tool size"))

  def set_fg_color(self):
    color = self.ask_for_color()
    self.editor.set_primary_color(color)
    self.primary_color_button.config(bg = color)

  def set_bg_color(self):
    color = self.ask_for_color()
    self.canvas.config(bg = color)
    self.background_color_button.config(bg = color)
