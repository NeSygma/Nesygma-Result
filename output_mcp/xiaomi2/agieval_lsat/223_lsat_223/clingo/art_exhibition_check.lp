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

% Test each option individually
% Option A: Franz's watercolor is displayed on wall 4
test_a :- on_wall(franz, watercolor, 4, _).

% Option B: Greene's oil is displayed on wall 2
test_b :- on_wall(greene, oil, 2, _).

% Option C: Greene's watercolor is displayed on wall 2
test_c :- on_wall(greene, watercolor, 2, _).

% Option D: Hidalgo's watercolor is displayed on wall 3
test_d :- on_wall(hidalgo, watercolor, 3, _).

% Option E: Isaacs's oil is displayed on wall 1
test_e :- on_wall(isaacs, oil, 1, _).

% Show which options are possible
possible_a :- test_a.
possible_b :- test_b.
possible_c :- test_c.
possible_d :- test_d.
possible_e :- test_e.

#show possible_a/0.
#show possible_b/0.
#show possible_c/0.
#show possible_d/0.
#show possible_e/0.
#show on_wall/4.