import numpy as np

def extend_rle(ls1, ls2):

    length_diff = abs(len(ls1) - len(ls2))

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


def test_compute_lengths():

    a, b = [1, 2, 3], [2]
    result, ax, bx = compute_lengths(a, b)

    assert result == [1, 1, 1, 3]
    assert ax == [0, 1, 1, 2]
    assert bx == [0, 0, -1, -1]


def test_compute_lengths2():

    a, b = [1, 2, 3], [1, 2]
    result, ax, bx = compute_lengths(a, b)

    assert result == [1, 2, 3]
    assert ax == [0, 1, 2]
    assert bx == [0, 1, -1]


def test_compute_lengths3():

    a, b = [1, 2, 3, 4], [1, 2]
    result, ax, bx = compute_lengths(a, b)

    assert result == [1, 2, 3, 4]
    assert ax == [0, 1, 2, 3]
    assert bx == [0, 1, -1, -1]


def test_compute_lengths4():

    a, b = [10, 10, 10], [1, 2]
    result, ax, bx = compute_lengths(a, b)

    assert result == [1, 2, 7, 10, 10]
    assert ax == [0, 0, 0, 1, 2]
    assert bx == [0, 1, -1, -1, -1]


def test_compute_lengths5():

    a, b = [1, 2], [2, 1] * 2
    result, ax, bx = compute_lengths(a, b)

    assert result == [1, 1, 1, 2, 1]
    assert ax == [0, 1, 1, -1, -1]
    assert bx == [0, 0, 1, 2, 3]
