from dataclasses import dataclass
DAMPEN_THRESHOLD = 5

@dataclass
class HatPosition:
    x: 0
    y: 0

    def _get(self, coordinate):
        return self.__dict__[coordinate]

    def _update(self, coordinate, value):
        self.__dict__[coordinate] = value

    def minmax(self):
        for i in ['x', 'y']:
            if self._get(i) > 0:
                self._update(i, min(self._get(i), 100))
            else:
                self._update(i, max(self._get(i), -100))

    def dampen(self, threshold=DAMPEN_THRESHOLD):
        for i in ['x', 'y']:
            if abs(self._get(i)) <= threshold:
                self._update(i, 0)

    def get_position(self):
        self.dampen()
        self.minmax()
        return (self.x, self.y)