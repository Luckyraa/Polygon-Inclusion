from itertools import islice, cycle


def couples(iterable):
    """Iterates on all couples of given iterable. This will wrap around last element."""
    return zip(iterable, islice(cycle(iterable), 1, None))
