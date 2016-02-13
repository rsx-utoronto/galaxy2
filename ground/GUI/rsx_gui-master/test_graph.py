import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from collections import deque
#import sensor_simulator


def three():
	return 300


class graph:

	def __init__(self, max_len, data_fn):

		self.ax = deque([0.0]*max_len)
		self.ay = deque([0.0]*max_len)
		self.max_len = max_len
		self.data_fn = data_fn


	def add_to_buffer(self, buf, val):

		if len(buf) < self.max_len:
			buf.appendleft(val)
		else:
			buf.pop()
			buf.appendleft(val)


	def add(self, data):

		self.add_to_buffer(self.ax, data)


	def update(self, frame_num, line):

		try:
			data = self.data_fn()
			self.add(data)
			line.set_data(range(self.max_len), self.ax)
		except:
			pass

		return line


def make_scrolling_graph(data_fn):

	graph1 = graph(200, data_fn)

	fig = plt.figure()
	ax = plt.axes(xlim=(0,200), ylim=(0,1040))
	line = ax.plot([], [])
	ani = animation.FuncAnimation(fig, graph1.update, fargs=(line), interval=50)

	# return ani
	plt.show()


if __name__ == '__main__':
	make_scrolling_graph(three)