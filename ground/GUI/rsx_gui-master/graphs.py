import matplotlib.animation as animation
import time
from collections import deque

class scrolling_graph:

    def __init__(self, max_len, data_fn):
        self.ax = deque([0.0]*max_len)
        self.max_len = max_len
        self.data_fn = data_fn


    def add_to_buffer(self, buf, val):
        if len(buf) < self.max_len:
            buf.appendleft(val)
        else:
            buf.pop()
            buf.appendleft(val)


    def update(self):
        data = self.data_fn()
        self.add_to_buffer(self.ax, data)

        return self.ax