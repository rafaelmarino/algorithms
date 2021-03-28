# python3

EPS = 1e-6
PRECISION = 20
import sys

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, row, column):
        self.column = column
        self.row = row
#
# def ReadEquation():
#     size = int(input())
#     a = []
#     b = []
#     for row in range(size):
#         line = list(map(float, input().split()))
#         a.append(line[:size])
#         b.append(line[size])
#     return Equation(a, b)

def ReadEquation():
    # Now I can copy and paste the entire input. Fuck yeah.
    data = sys.stdin.read()
    # Another Error here: split() must be used before selecting first line
    # Otherwise first character of the string will be taken, since data is a string with sepatarors
    size = int(data.split()[0])
    data = data.split()[1:]
    data = list(map(float, data))
    a = []
    b = []
    for _ in range(size):
        a.append(data[0:size])
        b.append(data[size])
        data = data[size + 1:]
    return Equation(a, b)

def SelectPivotElement(a, used_rows, used_columns):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.
    # Rafa:
    zero = 0.000000000000000000000
    # returns first index with False from left to right
    usedColIndex = used_columns.index(False)
    # returns list with actual column values
    column = [row[usedColIndex] for row in a]

    while sum(column) == zero:
        used_columns[usedColIndex] = True
        usedColIndex += 1
        column = [row[usedColIndex] for row in a]

    usedRowIndex = used_rows.index(False)
    row = a[usedRowIndex]
    while row[usedColIndex] == zero:
        usedRowIndex += 1
        row = a[usedRowIndex]

    # used_columns[usedColIndex] = True
    # used_rows[usedRowIndex] = True

    pivot_rc = Position(usedRowIndex, usedColIndex)
    return pivot_rc


def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    # Write your code here
    # Rafa:
    # Must be an in-place algorithm
    pivot_row = pivot_element.row
    pivot_col = pivot_element.column
    pivot_value = a[pivot_row][pivot_col]
    size = len(a[pivot_row])

    # if pivot value is not 1, divide entire row by pivot value
    if pivot_value != 1:
        for col in range(size):
            a[pivot_row][col] = a[pivot_row][col]/pivot_value
            # remember to operate on b as well
        # WARNING: the operation on b goes outside the loop as it is done only once
        # otherwise it would be 'eliminated' once per column iteration (40 min debugging)
        b[pivot_row] = b[pivot_row]/pivot_value

    # turn to zero all elements in pivot column except the pivot
    for row in range(size):
        if row != pivot_row:
            factor = a[row][pivot_col]
            # factor is calculated at the row level, it changes after turning to zero
            for col in range(size):
                a[row][col] = a[row][col] - a[pivot_row][col]*factor
            # b goes outside the loop
            b[row] = b[row] - b[pivot_row]*factor

    pass

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size

    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])


if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
    