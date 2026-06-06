% Domains
student(franz; greene; hidalgo; isaacs).
painting_type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student has exactly one oil and one watercolor to display
1 { assignment(S, T, W, P) : wall(W), position(P) } 1 :- student(S), painting_type(T).

% Each wall has exactly one upper and one lower painting
:- wall(W), #count { S, T, P : assignment(S, T, W, P), P = upper } != 1.
:- wall(W), #count { S, T, P : assignment(S, T, W, P), P = lower } != 1.

% No wall has only watercolors
% Helper: wall_has_oil(W) :- wall(W), assignment(_, oil, W, _).
wall_has_oil(W) :- assignment(_, oil, W, _).
:- wall(W), not wall_has_oil(W).

% No wall has only one student's work
% Helper: student_on_wall(W, S) :- assignment(S, _, W, _).
student_on_wall(W, S) :- assignment(S, _, W, _).
:- wall(W), #count { S : student_on_wall(W, S) } < 2.

% No wall has both Franz and Isaacs
:- wall(W), assignment(franz, _, W, _), assignment(isaacs, _, W, _).

% Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
:- assignment(franz, oil, W, _), not assignment(greene, watercolor, W, upper).

% Isaacs's oil is in the lower position of wall 4
:- not assignment(isaacs, oil, 4, lower).

% Given condition: Hidalgo's oil is on wall 2
assignment(hidalgo, oil, 2, _).

% Now determine which options could be on wall 2
% A) Franz's oil on wall 2
option(a) :- assignment(franz, oil, 2, _).

% B) Greene's watercolor on wall 2
option(b) :- assignment(greene, watercolor, 2, _).

% C) Greene's oil on wall 2
option(c) :- assignment(greene, oil, 2, _).

% D) Hidalgo's watercolor on wall 2
option(d) :- assignment(hidalgo, watercolor, 2, _).

% E) Isaacs's watercolor on wall 2
option(e) :- assignment(isaacs, watercolor, 2, _).

#show option/1.