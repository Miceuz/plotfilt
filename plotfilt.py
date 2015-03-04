#!/usr/bin/python

import numpy as np
from matplotlib.pylab import *
import sys

class Filter:
	filtered = 0
	weight = 0
	def __init__(self, weight):
		self.weight = weight

	def filter(self, newVal):
		self.filtered = self.filtered + ((newVal - self.filtered) >> self.weight) 
		return self.filtered
	def reset(self, value=0):
		self.filtered = value



if len(sys.argv) < 2:
	print "This program allows to analyse digital infinite impulse response filters. More info at http://electronics.stackexchange.com/a/30384"
	print "Usage:"
	print "plotfilt.py weight [weight] .. [weight]"
	print "weight - an integer specifying, how much the current value influences the filtered value, the bigger the less"
	print "the filter formula is filtered = filtered + ((newVal - filtered) >> self.weight)"
	print "each weight represents a single filter cascaded in series"
	exit(1)

MAXVAL = 65535

filterCascade = np.array([])

for i in range(1, len(sys.argv)):
	if not is_numlike(sys.argv[i]):
		filterCascade = np.append(filterCascade, Filter(int(sys.argv[i])))
	else:
		print "Error: all weights have to be integers. Offending weight: ", sys.argv[i]
		exit(1)

filtered = 0

stepResponse = np.zeros(1);
step = MAXVAL

filter1 = Filter(4)

while filtered < step*0.999:
	filtered = step
	for f in filterCascade:
		filtered = f.filter(filtered)
	stepResponse = np.append(stepResponse, filtered * 1.0 / MAXVAL)

plot(stepResponse, label="Step response")


for f in filterCascade:
	f.reset(MAXVAL/2)
noise = np.random.random(len(stepResponse))
noiseFiltered = np.zeros(0)

for v in noise:
	filtered = int(v * MAXVAL)
	for f in filterCascade:
		filtered = f.filter(filtered)
	noiseFiltered = np.append(noiseFiltered, filtered*1.0/MAXVAL)

plot(noiseFiltered, label="Filtered noise")


for f in filterCascade:
	f.reset()

impulseResponse = np.zeros(0)

impulse = MAXVAL

filtered = impulse
for f in filterCascade:
	filtered = f.filter(filtered)
impulseResponse = np.append(impulseResponse, filtered*1.0/MAXVAL)

for i in range(len(stepResponse)-1):
	filtered = 0
	for f in filterCascade:
		filtered = f.filter(filtered)
	impulseResponse = np.append(impulseResponse, filtered*1.0/MAXVAL)
plot(impulseResponse, label="Impulse response")
legend()
show()