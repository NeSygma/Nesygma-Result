% Domain definitions
student(franz). student(greene). student(hidalgo). student(isaacs).
painting_type(oil). painting_type(watercolor).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).

% Each student has exactly one oil and one watercolor painting
1 { placed(S, oil, W, P) : wall(W), position(P) } 1 :- student(S).
1 { placed(S, watercolor, W, P) : wall(W), position(P) } 1 :- student(S).

% Each wall has exactly one upper and one lower painting
1 { placed(S, T, W, upper) : student(S), painting_type(T) } 1 :- wall(W).
1 { placed(S, T, W, lower) : student(S), painting_type(T) } 1 :- wall(W).

% No wall has only watercolors
:- wall(W), not has_oil(W).
has_oil(W) :- placed(_, oil, W, _).

% No wall has work of only one student
:- wall(W), only_one_student(W).
only_one_student(W) :- wall(W), student(S), placed(S, _, W, _), 
                       not other_student_on_wall(W, S).
other_student_on_wall(W, S) :- wall(W), student(S), student(S2), S != S2, 
                               placed(S2, _, W, _).

% No wall has both Franz and Isaacs
:- wall(W), placed(franz, _, W, _), placed(isaacs, _, W, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- placed(greene, watercolor, W, P), placed(franz, oil, W2, _), W != W2.
:- placed(greene, watercolor, W, P), P != upper.
:- placed(franz, oil, W, _), not placed(greene, watercolor, W, upper).

% Isaacs's oil is displayed in the lower position of wall 4
placed(isaacs, oil, 4, lower).

% Isaacs's watercolor is displayed on wall 2
placed(isaacs, watercolor, 2, _).

% Franz's oil is displayed on wall 3
placed(franz, oil, 3, _).

% Determine what must be on wall 1
on_wall1(S, T) :- placed(S, T, 1, _).

% Check each option
option(a) :- on_wall1(franz, watercolor).
option(b) :- on_wall1(greene, oil).
option(c) :- on_wall1(greene, watercolor).
option(d) :- on_wall1(hidalgo, oil).
option(e) :- on_wall1(hidalgo, watercolor).

#show option/1.
#show placed/4.