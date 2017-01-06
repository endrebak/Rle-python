from itertools import izip
import os, sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Rle:
	
	def __init__(self, values = [], lengths = None):
		self.values = []
		self.lengths = []
		self.totLength = 0
		if lengths == None:
			for val in values:
				self.add(val)
		else:
			assert(len(values) == len(lengths))
			for val, le in izip(values, lengths):
				self.add(val, le)

	
	def __str__(self):
		return 'numeric-Rle of length {} with {} runs\n  Lengths:\t'.format(self.length(), self.nrun()) \
			+ str(self.lengths) + '\n  Values : \t' + str(self.values)
	
	def __mul__(self, val):
		r = Rle()
		for v, le in izip(self.values, self.lengths):
			r.add(v * val, le)
		return r
	
	def __rmul__(self, val):
		return self.__mul__(val)
	
	def __add__(self, other):
		assert(self.length() == other.length())
		if self.length() == 0: # case where both are empty
			return Rle()
		
		r = Rle()
		a_ind = 0
		a_rem = self.lengths[a_ind]
		b_ind = 0
		b_rem = other.lengths[b_ind]
		
		while a_ind < self.nrun(): # both have the same length, so no need to check both
			max_vals = min(a_rem, b_rem)
			r.add(self.values[a_ind] + other.values[b_ind], max_vals)
			a_rem -= max_vals
			b_rem -= max_vals
			if a_rem == 0:
				a_ind += 1
				a_rem = None if a_ind == self.nrun() else self.lengths[a_ind] # included case when out of bounds
			if b_rem == 0:
				b_ind += 1
				b_rem = None if b_ind == other.nrun() else other.lengths[b_ind] # included case when out of bounds
		return r
		
	def __sub__(self, other):
		return self.__add__(other.__mul__(-1))
	
	# taken from http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		return NotImplemented
	
	def __ne__(self, other):
		"""Define a non-equality test"""
		if isinstance(other, self.__class__):
			return not self.__eq__(other)
		return NotImplemented

	def __hash__(self):
		"""Override the default hash behavior (that returns the id or the object)"""
		return hash(tuple(sorted(self.__dict__.items())))
	
	def add(self, val, multiplicity=1):
		assert multiplicity > 0
		self.totLength += multiplicity
		if (not self.values) or (self.values[-1] != val): # empty list or not the same element as before
			self.values.append(val)
			self.lengths.append(multiplicity)
		else: # same element as before
			self.lengths[-1] += multiplicity
		return self
	
	def run_length(self):
		return self.lengths
	
	def run_value(self):
		return self.values
	
	def nrun(self):
		return len(self.lengths)
		
	def width(self):
		return self.run_length()
	
	def start(self): # linear time, baaaaad
		res = []
		for i in range(self.nrun()):
			res.append(1 if not res else res[i-1] + self.lengths[i-1])
		return res
	
	def end(self): # linear time, baaaaad
		res = []
		for i in range(self.nrun()):
			res.append(self.lengths[0] if not res else res[i-1] + self.lengths[i])
		return res
	
	def decode(self):
		# !!! only works for immutable values!!!
		# see http://stackoverflow.com/questions/4654414/python-append-item-to-list-n-times
		res = []
		for val, le in izip(self.values, self.lengths):
			res.extend([val] * le)
		return res
	
	def length(self):
		return self.totLength
		

	
			
r1 = Rle([1, 1, 1, 4, 4, 5, 4, 3], [3, 4, 5, 6, 7, 8, 9, 10])
r2 = Rle([2, 2, 3, 3, 1, 1, 4, 4], [10, 9, 8, 7, 6, 5, 4, 3])
r3 = Rle([1], [52])
print r1
print r2
print r3
print r1 + r2
print r1 + r3
print (r1+r3).length()
r4 = Rle()
r4.add(5, 6)
r4.add(5)
r4.add(6, 3)
r4.add(6, 1)
r4.add(5, 1)
print r4
print r4.start()
print r4.end()
print r4
print r2.decode()
r5 = Rle([1])
r6 = Rle([3])
print r5
print r6
r7 = r5-r6
print r7
print (r5-Rle([3]))
print(r7)
print (Rle([1, 1, 3, 4], [2, 3, 1, 2]).run_length())

