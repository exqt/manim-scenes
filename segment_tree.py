import math
from manim import *

class ArrayObject(VGroup):
  def __init__(self, n, cell_size = 1):
    super().__init__()
    self.n = n
    self.cell_size = cell_size
    self.rect = Rectangle(height=1, width=n*cell_size)
    self.cells = []
    for i in range(n):
      cell = Rectangle(height=1, width=cell_size)
      self.add(cell)
      if i == 0:
        cell.move_to(self.rect, aligned_edge=LEFT)
      else:
        cell.next_to(self.cells[-1], direction=RIGHT, buff=0)
      self.cells.append(cell)

  def createUpperNode(self):
    n1 = ArrayObject(self.n//2, cell_size=self.cell_size*2)
    n1.move_to(self.rect, UP+LEFT)
    return n1

class SegmentTree(Scene):
  def make(self):
    H = 3
    a0 = ArrayObject(2**H)
    self.play(ShowCreation(a0))
    a1 = a0.createUpperNode()
    self.play(
      AnimationGroup(
        AnimationGroup(
          a0.animate.shift(DOWN)
        ),
        FadeIn(a1),
        lag_ratio=1.0
      )
    )
    a2 = a1.createUpperNode()
    self.play(
      AnimationGroup(
        AnimationGroup(
          a0.animate.shift(DOWN),
          a1.animate.shift(DOWN)
        ),
        FadeIn(a2),
        lag_ratio=1.0
      )
    )
    a3 = a2.createUpperNode()
    self.play(
      AnimationGroup(
        AnimationGroup(
          a0.animate.shift(DOWN),
          a1.animate.shift(DOWN),
          a2.animate.shift(DOWN)
        ),
        FadeIn(a3),
        lag_ratio=1.0
      )
    )

  def construct(self):
    self.make()
