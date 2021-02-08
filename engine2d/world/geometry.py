from dataclasses import dataclass
from typing import List

@dataclass
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float

@dataclass
class Point:
  x: float
  y: float

@dataclass
class Polygon:
  points: List[Point]

@dataclass
class Line:
  begin: Point
  end: Point
