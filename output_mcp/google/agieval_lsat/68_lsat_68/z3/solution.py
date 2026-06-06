from z3 import *

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(b) for b in books}

solver = Solver()

# Shelf domain: 0=Top, 1=Middle, 2=Bottom
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F
solver.add(shelf['K'] > shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# At least two books on each shelf
count0 = Sum([If(shelf[b] == 0, 1, 0) for b in books])
count1 = Sum([If(shelf[b] == 1, 1, 0) for b in books])
count2 = Sum([If(shelf[b] == 2, 1, 0) for b in books])

solver.add(count0 >= 2)
solver.add(count1 >= 2)
solver.add(count2 >= 2)

# More books on bottom than top
solver.add(count2 > count0)

# Total books = 8
solver.add(count0 + count1 + count2 == 8)

# Options
# (A) O > M
# (B) K > G
# (C) I > F
# (D) G > O
# (E) F > L

options = {
    "A": shelf['O'] > shelf['M'],
    "B": shelf['K'] > shelf['G'],
    "C": shelf['I'] > shelf['F'],
    "D": shelf['G'] > shelf['O'],
    "E": shelf['F'] > shelf['L']
}

results = {}
for label, cond in options.items():
    solver.push()
    solver.add(Not(cond))
    if solver.check() == unsat:
        results[label] = "Must be true"
    else:
        results[label] = "Not necessarily true"
    solver.pop()

print(results)