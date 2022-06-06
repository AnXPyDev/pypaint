class Vector:
  def __init__(self, x = 0, y = None):
    if (y == None):
      y = x
    self.x = x
    self.y = y

  def __eq__(self, other):
    if self.x == other.x and self.y == other.y:
      return True
    return False

  def __str__(self):
    return f"V[x = {self.x}, y = {self.y}]"

  def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y)

  def __mul__(self, other):
    return Vector(self.x * other.x, self.y * other.y)
  
  def __truediv__(self, other):
    return Vector(self.x / other.x, self.y / other.y)
  
  def copy(self):
    return Vector(self.x, self.y)
