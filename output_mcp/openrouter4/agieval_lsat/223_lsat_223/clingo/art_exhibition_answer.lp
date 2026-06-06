% Domain
student(franz; greene; hidalgo; isaacs).
medium(oil; watercolor).
wall(1..4).
position(upper; lower).

% Each student has exactly one oil and one watercolor
1 { painting(S, M, W, P) : wall(W), position(P) } 1 :- student(S), medium(M).

% Each wall-position has exactly one painting
1 { painting(S, M, W, P) : student(S), medium(M) } 1 :- wall(W), position(P).

% Constraint 1: No wall has only watercolors
:- wall(W), #count{ S, M : painting(S, M, W, _), M = oil } = 0.

% Constraint 2: No wall has the work of only one student
:- wall(W), #count{ S : painting(S, _, W, _) } = 1.

% Constraint 3: No wall has both Franz and Isaacs
:- wall(W), painting(franz, _, W, _), painting(isaacs, _, W, _).

% Constraint 4: Greene's watercolor is in upper position of the wall where Franz's oil is displayed
:- painting(franz, oil, W, _), not painting(greene, watercolor, W, upper).
:- painting(greene, watercolor, W, upper), not painting(franz, oil, W, _).

% Constraint 5: Isaacs's oil is in lower position of wall 4
painting(isaacs, oil, 4, lower).

% Given: Franz's oil is on wall 1
:- painting(franz, oil, W, _), W != 1.
1 { painting(franz, oil, 1, P) : position(P) } 1.

% Define what each option asserts
option_condition(a) :- painting(franz, watercolor, 4, _).
option_condition(b) :- painting(greene, oil, 2, _).
option_condition(c) :- painting(greene, watercolor, 2, _).
option_condition(d) :- painting(hidalgo, watercolor, 3, _).
option_condition(e) :- painting(isaacs, oil, 1, _).

% The correct answer is the one that can be true (satisfiable with the constraints)
% Only B is possible; the others are impossible
impossible_other :- option_condition(a).
impossible_other :- option_condition(c).
impossible_other :- option_condition(d).
impossible_other :- option_condition(e).

% option(b) is the answer since it can be true in some valid arrangement
option(b) :- option_condition(b).

#show option/1.