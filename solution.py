import re
from itertools import combinations

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
all_digits = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r + c for r, c in zip(rows, cols)]]
antidiag_units = [[r + c for r, c in zip(rows, reversed(cols))]]
unitlist = row_units + column_units + square_units + diag_units + antidiag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        boxes_len_two = [box for box in unit if len(values[box]) == 2]
        if len(boxes_len_two) >= 2:
            twins = [(box1, box2)
                     for box1, box2 in combinations(boxes_len_two, 2)
                     if values[box1] == values[box2]]
            if len(twins) >= 1:
                for twin in twins:
                    for box in unit:
                        if box is not twin[0] and box is not twin[1]:
                            twin_pattern = '[' + values[twin[0]] + ']'
                            new_value = re.sub(twin_pattern, '', values[box])
                            values = assign_value(values, box, new_value)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    grid_dict = dict()
    for char, box in zip(grid, boxes):
        if char == '.':
            grid_dict[box] = all_digits
        else:
            grid_dict[box] = char
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_boxes = [box for box, value in values.items() if len(value) == 1]
    for box in solved_boxes:
        for peer in peers[box]:
            new_value = values[peer].replace(values[box], '')
            values = assign_value(values, peer, new_value)
    return values

def only_choice(values):
    unsolved_boxes = [box for box, value in values.items() if len(value) > 1]
    for unit in unitlist:
        unsolved_inunit = set(unit).intersection(set(unsolved_boxes))
        solved_inunit = set(unit).difference(set(unsolved_boxes))
        placed_digits = [values[box] for box in solved_inunit]
        for digit in all_digits:
            if digit not in placed_digits:
                places = [box for box in unsolved_inunit
                          if digit in values[box]]
                if len(places) == 1:
                    values = assign_value(values, places[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        values_before = values.copy()
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        stalled = values == values_before
        if len([box for box, value in values.items() if len(value) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(value) == 1 for value in values.values()):
        return values
    num, box = min((len(value), box) for box, value in values.items()
                   if len(value) > 1)
    for digit in values[box]:
        attemp = values.copy()
        attemp = assign_value(attemp, box, digit)
        attemp = search(attemp)
        if attemp:
            return attemp

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid_dict = grid_values(grid)
    return search(grid_dict)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
