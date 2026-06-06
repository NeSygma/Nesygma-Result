% Domains
student(franz; greene; hidalgo; isaacs).
wall(1;2;3;4).
position(upper; lower).
type(oil; watercolor).

% Each student has exactly one oil
1 { placed(S, oil, W, P) : wall(W), position(P) } 1 :- student(S).

% Each student has exactly one watercolor
1 { placed(S, watercolor, W, P) : wall(W), position(P) } 1 :- student(S).

% Each wall has exactly one upper painting
1 { placed(S, T, W, upper) : student(S), type(T) } 1 :- wall(W).

% Each wall has exactly one lower painting
1 { placed(S, T, W, lower) : student(S), type(T) } 1 :- wall(W).

% Constraint 1: No wall has only watercolors
:- placed(S1, watercolor, W, upper), placed(S2, watercolor, W, lower).

% Constraint 2: No wall has the work of only one student
:- placed(S, _, W, upper), placed(S, _, W, lower).

% Constraint 3: No wall has both Franz and Isaacs
:- placed(franz, _, W, _), placed(isaacs, _, W, _).

% Constraint 4: Greene's watercolor is upper on the wall where Franz's oil is displayed (lower)
placed(franz, oil, W, lower) :- placed(greene, watercolor, W, upper).
placed(greene, watercolor, W, upper) :- placed(franz, oil, W, lower).

% Constraint 5: Isaacs's oil is lower on wall 4
placed(isaacs, oil, 4, lower).

% Question condition: Hidalgo's oil is on wall 2
:- placed(hidalgo, oil, W, _), W != 2.

% Test option C: Greene's oil is on wall 2
:- not placed(greene, oil, 2, _).