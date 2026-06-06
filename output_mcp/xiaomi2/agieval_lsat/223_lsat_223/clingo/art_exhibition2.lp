% Domains
student(franz). student(greene). student(hidalgo). student(isaacs).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).

% Each student has one oil and one watercolor painting
painting(franz, oil). painting(franz, watercolor).
painting(greene, oil). painting(greene, watercolor).
painting(hidalgo, oil). painting(hidalgo, watercolor).
painting(isaacs, oil). painting(isaacs, watercolor).

% Assign each painting to exactly one wall and position
{ on_wall(S, T, W, P) : wall(W), position(P) } 1 :- painting(S, T).

% Each wall-position gets exactly one painting
1 { on_wall(S, T, W, P) : painting(S, T) } 1 :- wall(W), position(P).

% Fixed assignments from the problem
:- not on_wall(isaacs, oil, 4, lower).
:- not on_wall(franz, oil, 1, lower).
:- not on_wall(greene, watercolor, 1, upper).

% Constraint 1: No wall has only watercolors
has_oil(W) :- on_wall(_, oil, W, _).
:- wall(W), not has_oil(W).

% Constraint 2: No wall has the work of only one student
two_students(W) :- on_wall(S1, _, W, _), on_wall(S2, _, W, _), S1 != S2.
:- wall(W), not two_students(W).

% Constraint 3: No wall has both Franz and Isaacs
:- wall(W), on_wall(franz, _, W, _), on_wall(isaacs, _, W, _).

% Option conditions
option_a_possible :- on_wall(franz, watercolor, 4, _).
option_b_possible :- on_wall(greene, oil, 2, _).
option_c_possible :- on_wall(greene, watercolor, 2, _).
option_d_possible :- on_wall(hidalgo, watercolor, 3, _).
option_e_possible :- on_wall(isaacs, oil, 1, _).

% Disjunctive rule: at least one option must be true
option(a) | option(b) | option(c) | option(d) | option(e).

% Link options to their conditions
option(a) :- option_a_possible.
option(b) :- option_b_possible.
option(c) :- option_c_possible.
option(d) :- option_d_possible.
option(e) :- option_e_possible.

#show option/1.
#show on_wall/4.