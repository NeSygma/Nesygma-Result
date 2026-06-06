% Positive conjecture: Taylor neither grew up in health-conscious home nor visits gym daily.
fof(grow_up, axiom, ! [X] : (g(X) => s(X))).
fof(eat_salad, axiom, ! [X] : (s(X) => c(X))).
fof(fulfill, axiom, ! [X] : (f(X) => g(X))).
fof(disregard, axiom, ! [X] : (d(X) => ~c(X))).
fof(gym, axiom, ! [X] : (v(X) => f(X))).
fof(taylor_eq, axiom, (g(taylor) <=> d(taylor))).
fof(goal, conjecture, (~g(taylor) & ~v(taylor))).