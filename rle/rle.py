from __future__ import print_function

# itertools izip does not exist in Python3; zip is izip there
try:
    from itertools import izip
    zip = izip
except ImportError:
    pass

from bisect import bisect
import os, sys


class Rle():

    def __init__(self, values=None, lengths=None):
        self.values = []
        self.lengths = []
        self.cum_lengths = []
        self.cum_end_lengths = []
        self.tot_length = 0
        if not (values is None):
            if lengths is None:
                lengths = [1] * len(values)
            assert(len(values) == len(lengths))
            for val, le in zip(values, lengths):
                self.add(val, le)

    def __str__(self):
        return 'Rle of length {} with {} runs\n  Lengths:\t'.format(self.length(), self.nrun()) \
            + str(self.lengths) + '\n  Values : \t' + str(self.values)

    @staticmethod
    def compute_lengths(a_le, b_le):
        if (not a_le) or (not b_le):
            return ([], [], [])
        a = [] # indexes of elements in a_le to include
        b = [] # indexes of elements in b_le to include
        lengths = []
        a_ind = 0
        b_ind = 0
        a_rem = a_le[0]
        b_rem = b_le[0]

        while a_ind < len(a_le) and b_ind < len(b_le):
            nb_to_take = min(a_rem, b_rem)
            lengths.append(nb_to_take)
            a_rem -= nb_to_take
            b_rem -= nb_to_take
            a.append(a_ind)
            b.append(b_ind)
            if a_rem == 0:
                a_ind += 1
                a_rem = 0 if a_ind == len(a_le) else a_le[a_ind]
            if b_rem == 0:
                b_ind += 1
                b_rem = 0 if b_ind == len(b_le) else b_le[b_ind]
        return (lengths, a, b)

    def _element_wise_operation(self, other, op):
        (lengths, a, b) = _compute_lengths(self.lengths, other.lengths)
        values = []
        for (i, j) in zip(a, b):
            values.append(op(self.values[i], other.values[j]))
        return Rle(values, lengths)


    def element_wise_operation(self, other, op):
        assert(self.length() == other.length())
        if self.length() == 0:  # case where both are empty
            return Rle()

        r = Rle()
        a_ind = 0
        a_rem = self.lengths[a_ind]
        b_ind = 0
        b_rem = other.lengths[b_ind]

        while a_ind < self.nrun():  # both have the same length, so no need to check both
            max_vals = min(a_rem, b_rem)
            r.add(op(self.values[a_ind], other.values[b_ind]), max_vals)
            a_rem -= max_vals
            b_rem -= max_vals
            if a_rem == 0:
                a_ind += 1
                a_rem = None if a_ind == self.nrun() else self.lengths[
                    a_ind]  # included case when out of bounds
            if b_rem == 0:
                b_ind += 1
                b_rem = None if b_ind == other.nrun() else other.lengths[
                    b_ind]  # included case when out of bounds
        return r

    def single_operation(self, op):
        r = Rle()
        for val, le in zip(self.values, self.lengths):
            r.add(op(val), le)
        return r

    def __mul__(self, val):
        return self.single_operation(lambda x: x * val)

    def __rmul__(self, val):
        return self.__mul__(val)

    def __add__(self, other):
        return self.element_wise_operation(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.element_wise_operation(other, lambda x, y: x - y)

    # taken from
    # http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
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
        # empty list or not the same element as before
        if (not self.values) or (self.values[-1] != val):
            self.values.append(val)
            self.lengths.append(multiplicity)
            self.cum_lengths.append(self.length())
            self.cum_end_lengths.append(self.length() + multiplicity - 1)
        else:  # same element as before
            self.lengths[-1] += multiplicity
            self.cum_end_lengths[-1] += multiplicity
        self.tot_length += multiplicity
        return self

    def run_length(self):
        return self.lengths

    def run_value(self):
        return self.values

    def nrun(self):
        return len(self.lengths)

    def width(self):
        return self.run_length()

    def start(self):
        return self.cum_lengths

    def end(self):
        return self.cum_end_lengths

    def head(self, n):
        if n < 0:
            n %= self.length()
        res = Rle()
        index = 0
        while n > 0 and index < self.nrun():
            to_take = min(n, self.lengths[index])
            res.add(self.values[index], to_take)
            n -= to_take
            index += 1
        return res

    def decode(self):
        # !!! only works for immutable values!!!
        # see
        # http://stackoverflow.com/questions/4654414/python-append-item-to-list-n-times
        r = []
        for (val, le) in zip(self.values, self.lengths):
            r.extend([val] * le)
        return r

    def length(self):
        return self.tot_length

    def get_index(self, index):
        index %= self.length()
        return bisect(self.start(), index) - 1

    def get(self, index):
        return self.values[self.get_index(index)]

    def find_run(self, indexes):
        return [self.get_index(i) for i in indexes]

    def clear(self):
        self.tot_length = 0
        self.lengths = []
        self.cum_lengths = []
        self.cum_end_lengths = []
        self.values = []

    def append(self, other, after = None):
        after = self.length() if after is None else after
        curr = self.head(after - 1)
        print(curr)
        for (val, le) in zip(other.values, other.lengths):
            curr.add(val, le)
        return curr

    def rev(self):
        return Rle(list(reversed(self.values)), list(reversed(self.lengths)))


    def tail(self, n):
        if n < 0:
            n %= self.length()
        res = Rle()
        index = self.nrun() - 1
        while n > 0 and index >= 0:
            to_take = min(n, self.lengths[index])
            res.add(self.values[index], to_take)
            n -= to_take
            index -= 1
        return res.rev()

    def sorted(self, compare = None):
        compare = (lambda x, y: x < y) if compare is None else compare

        #  check elements inside every run
        for i in range(0, self.length()):
            if self.lengths[i] > 1 and (not compare(self.values[i], self.values[i])):
                return False

        #  check transition between runs
        for i in range(1, self.length()):
            if not compare(self.values[i-1], self.values[i]):
                return False

        return True

    def map(self, f):
        r = Rle()
        for (val, le) in zip(self.values, self.lengths):
            r.add(f(val), le)
        return r

    def filter(self, f):
        r = Rle()
        for (val, le) in zip(self.values, self.lengths):
            if f(val):
                r.add(val, le)
        return r






r1 = Rle([1, 1, 1, 4, 4, 5, 4, 3], [3, 4, 5, 6, 7, 8, 9, 10])
r2 = Rle([2, 2, 3, 3, 1, 1, 4, 4], [10, 9, 8, 7, 6, 5, 4, 3])
r3 = Rle([1], [52])
#print(r2.decode())
#print(r2.head(-3))
#print(r1.append(r2))
print(r2)
print(r2.end())
print(r2.start())
print(r2.tail(5))

# lengths for rle1 and 2
ls1 =  [1, 2]
ls2 =  [1, 1, 1, 5]

expected_lengths = [1, 1, 1]
expected_ls1_indexes = [0, 1, 1]
expected_ls2_indexes = [0, 1, 2]

(result, ls1_indexes, ls2_indexes) = Rle.compute_lengths(ls1, ls2)

assert result == expected_lengths
assert ls1_indexes == expected_ls1_indexes
assert ls2_indexes == expected_ls2_indexes
