"""Credits and levels computations.
"""
from itertools import accumulate, chain


def total_credits_for_levels(levels):
    needed_credits = accumulate(chain([0], levels), lambda c, l: c + l.credits)
    # last accumulated value is not used - student can't go beyond the last level
    return zip(levels, needed_credits)


def get_needed_credits(world, which_level):
    for level, credits in total_credits_for_levels(world.levels):
        if level == which_level:
            return credits
    raise ValueError('Unknown level: {level}'.format(level=which_level))


def get_level(world, student):
    level = world.levels[0]
    for next_level, needed_credits in total_credits_for_levels(world.levels):
        if student.credits >= needed_credits:
            level = next_level
        else:
            return level
    return level


def get_level_value(world, student):
    return get_level(world, student).level


def get_active_credits(world, student):
    level = get_level(world, student)
    passive_credits = get_needed_credits(world, level)
    active_credits = student.credits - passive_credits
    return active_credits
