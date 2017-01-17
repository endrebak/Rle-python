Read_this_answer = "I need this variable set for Cython to work, see http://stackoverflow.com/questions/8024805/cython-compiled-c-extension-importerror-dynamic-module-does-not-define-init-fu"
# from libcpp.vector cimport vector

import numpy as np

def extend_rle(ls1, ls2):

    sum_lengths1 = np.sum(ls1)
    sum_lengths2 = np.sum(ls2)

    if sum_lengths1 < sum_lengths2:
        diff = sum_lengths2 - sum_lengths1
        ls1 = ls1 + [diff]

    if sum_lengths2 < sum_lengths1:
        diff = sum_lengths1 - sum_lengths2
        ls2 = ls2 + [diff]

    return ls1, ls2


def compute_lengths(a_le, b_le):

    cdef unsigned int a_ind, b_ind, a_rem, b_rem
    cdef signed int prev_a, prev_b

    a_ex, b_ex = extend_rle(a_le, b_le)

    a = [] # indexes of elements in a_ex to include
    b = [] # indexes of elements in b_ex to include
    lengths = []
    a_ind = 0
    b_ind = 0
    a_rem = a_ex[0]
    b_rem = b_ex[0]

    while a_ind < len(a_ex) and b_ind < len(b_ex):
        nb_to_take = min(a_rem, b_rem)
        lengths.append(nb_to_take)
        a_rem -= nb_to_take
        b_rem -= nb_to_take
        a.append(a_ind)
        b.append(b_ind)
        if a_rem == 0:
            a_ind += 1
            a_rem = 0 if a_ind == len(a_ex) else a_ex[a_ind]
        if b_rem == 0:
            b_ind += 1
            b_rem = 0 if b_ind == len(b_ex) else b_ex[b_ind]

    prev_a = -1
    while a[prev_a] > len(a_le) - 1:
        a[prev_a] = -1
        prev_a -= 1

    prev_b = -1
    while b[prev_b] > len(b_le) - 1:
        b[prev_b] = -1
        prev_b -= 1

    return (lengths, a, b)


def compute_lengths_idx(a_le, b_le):

    cdef unsigned int a_ind, b_ind, a_rem, b_rem, nb_to_take

    a_ex, b_ex = extend_rle(a_le, b_le)

    a_ind = 0
    b_ind = 0
    a_rem = a_ex[0]
    b_rem = b_ex[0]
    len_a_ex, len_b_ex = len(a_ex), len(b_ex)
    lengths = [-1] * (len_a_ex + len_b_ex)
    a = [-1] * (len_a_ex + len_b_ex) # indexes of elements in a_ex to include
    b = [-1] * (len_a_ex + len_b_ex) # indexes of elements in b_ex to include

    nlx = 0
    while a_ind < len_a_ex and b_ind < len_b_ex:
        nb_to_take = min(a_rem, b_rem)
        lengths[nlx] = nb_to_take
        a_rem -= nb_to_take
        b_rem -= nb_to_take
        a[nlx] = a_ind
        b[nlx] = b_ind
        nlx += 1
        if a_rem == 0:
            a_ind += 1
            a_rem = 0 if a_ind == len_a_ex else a_ex[a_ind]
        if b_rem == 0:
            b_ind += 1
            b_rem = 0 if b_ind == len_b_ex else b_ex[b_ind]

    prev_a = -1
    while a[prev_a] > len(a_le) - 1:
        a[prev_a] = -1
        prev_a -= 1

    prev_b = -1
    while b[prev_b] > len(b_le) - 1:
        b[prev_b] = -1
        prev_b -= 1

    return (lengths, a, b)
