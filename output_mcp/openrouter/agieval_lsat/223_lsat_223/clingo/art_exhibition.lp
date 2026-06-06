% Students
student(franz). student(greene). student(hidalgo). student(isaacs).

% Domains
wall(1..4).
pos(upper; lower).

% Each oil painting placed exactly once
1 { placed(oil(S), W, P) : wall(W), pos(P) } 1 :- student(S).
% Each watercolor placed exactly once
1 { placed(water(S), W, P) : wall(W), pos(P) } 1 :- student(S).

% Each wall/position has exactly one painting (either oil or watercolor)
1 { placed(oil(S), W, P) : student(S) ; placed(water(S), W, P) : student(S) } 1 :- wall(W), pos(P).

% Premise: Franz's oil is on wall 1 (any position)
:- placed(oil(franz), W, _), W != 1.

% Greene's watercolor is upper on the same wall as Franz's oil
placed(water(greene), W, upper) :- placed(oil(franz), W, _).

% Isaacs's oil is lower on wall 4
placed(oil(isaacs), 4, lower).

% No wall has only watercolors (must have at least one oil)
oil_on_wall(W) :- placed(oil(_), W, _).
:- wall(W), not oil_on_wall(W).

% No wall has work of only one student (different students on a wall)
student_of(oil(S), S) :- student(S).
student_of(water(S), S) :- student(S).
:- wall(W), placed(P1, W, upper), placed(P2, W, lower), student_of(P1, S), student_of(P2, S).

% No wall has both a painting by Franz and a painting by Isaacs
:- wall(W), placed(P1, W, _), placed(P2, W, _), student_of(P1, franz), student_of(P2, isaacs).

% Options conditions
option(a) :- placed(water(franz), 4, _).
option(b) :- placed(oil(greene), 2, _).
option(c) :- placed(water(greene), 2, _).
option(d) :- placed(water(hidalgo), 3, _).
option(e) :- placed(oil(isaacs), 1, _).

% Exactly one option true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.