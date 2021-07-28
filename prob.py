from numpy.random import choice


def prob(p):
    elements = [0, 1]
    weights = [1-p, p]

    return choice(elements, p=weights)


