import math
from manim import *

class P:
  def __init__(self, x, y, o):
    self.x = x
    self.y = y
    self.o = o

class ConvexHull(MovingCameraScene):
  data = [
    (-3, -1), (-1, -2), (1, -1),
    (2, -2), (1, 2), (3, 1),
    (-1.5, 0), (-0.5, 1.2), (-3, 1.5),
  ]

  def pick_lowest(self):
    self.p0 = self.pts[0]
    for pt in self.pts:
      if pt.y < self.p0.y:
        self.p0 = pt

    self.p0.o.animate.set_fill(RED)
    self.play(self.p0.o.animate.scale(1.5).set_fill(RED))
    self.wait(0.2)

    self.pts.remove(self.p0)

  def arrows(self):
    self.arrow_group = VGroup()
    for pt in self.pts:
      ar = Arrow([self.p0.x, self.p0.y, 0], [pt.x, pt.y, 0])
      self.arrow_group.add(ar)
    self.play(ShowCreation(self.arrow_group))
    self.wait(0.5)

  def sort(self):
    self.pts.sort(key = lambda p: math.atan2(p.y - self.p0.y, p.x - self.p0.x))
    self.label_group = VGroup()
    self.label_group.add(Text('0').scale(0.5).next_to(self.p0.o, DOWN))
    for i, pt in enumerate(self.pts):
      t = Text(str(i+1)).scale(0.5).next_to(pt.o, (RIGHT+UP))
      self.label_group.add(t)

    self.play(Write(self.label_group))
    self.wait(0.5)
    self.play(FadeOut(self.arrow_group))
    self.wait(0.5)

  def process(self):
    stack = [self.p0, self.pts[0]]
    hull = []

    ar01 = Arrow(self.p0.o.get_center(), self.pts[0].o.get_center())
    hull.append(ar01)
    self.play(ShowCreation(ar01))

    def cross(px, py, qx, qy): return px*qy - py*qx

    for pt in self.pts[1:]:
      arrow0 = Arrow(stack[-1].o.get_center(), pt.o.get_center())
      arrow1 = hull[-1]
      self.play(ShowCreation(arrow0), run_time = 0.7)

      while cross(stack[-1].x - stack[-2].x, stack[-1].y - stack[-2].y, pt.x - stack[-1].x, pt.y - stack[-1].y) < 0:
        self.play(
          arrow0.animate.set_color(RED),
          arrow1.animate.set_color(RED),
          run_time = 0.7
        )
        arrow2 = Arrow(stack[-2].o.get_center(), pt.o.get_center())
        self.play(
          FadeOut(arrow0),
          FadeOut(arrow1),
          ShowCreation(arrow2),
          run_time = 0.7
        )
        stack.pop()
        hull.pop()
        arrow0, arrow1 = arrow2, hull[-1]

      stack.append(pt)
      hull.append(arrow0)

    arrow_last = Arrow(stack[-1].o.get_center(), self.p0.o.get_center())
    hull.append(arrow_last)
    self.play(ShowCreation(arrow_last))

    hull_group = VGroup()
    for e in hull: hull_group.add(e)
    self.play(hull_group.animate.set_color(BLUE))

  def convex_hull(self, data):
    dot_group = VGroup()
    self.pts = []

    for pt in data:
      o = Dot(point=(pt[0], pt[1], 0))
      p = P(pt[0], pt[1], o)
      dot_group.add(o)
      self.pts.append(p)

    self.play(ShowCreation(dot_group))
    self.wait(0.5)

    self.pick_lowest()
    self.arrows()
    self.sort()
    self.process()
    self.play(FadeOut(self.label_group))
    self.wait(1)

  def construct(self):
    self.camera_frame.scale(0.8)
    self.convex_hull(ConvexHull.data)
