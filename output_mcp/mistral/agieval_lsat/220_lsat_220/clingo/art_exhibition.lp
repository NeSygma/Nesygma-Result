% Domains
student(franz; greene; hidalgo; isaacs).
painting_type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student displays exactly one oil and one watercolor
1 { displayed(S, oil, W, P) : wall(W), position(P) } 1 :- student(S).
1 { displayed(S, watercolor, W, P) : wall(W), position(P) } 1 :- student(S).

% Each wall has exactly one painting in upper position and one in lower position
1 { displayed(S, T, W, upper) : student(S), painting_type(T) } 1 :- wall(W).
1 { displayed(S, T, W, lower) : student(S), painting_type(T) } 1 :- wall(W).

% No wall has only watercolors
has_oil(W) :- displayed(_, oil, W, _).
:- wall(W), not has_oil(W).

% No wall has work from only one student
has_multiple_students(W) :- displayed(S1, _, W, _), displayed(S2, _, W, _), S1 != S2.
:- wall(W), not has_multiple_students(W).

% No wall has both Franz and Isaacs paintings
:- wall(W), displayed(franz, _, W, _), displayed(isaacs, _, W, _).

% Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
:- displayed(franz, oil, W, _), not displayed(greene, watercolor, W, upper).
:- displayed(greene, watercolor, W, upper), not displayed(franz, oil, W, _).

% Isaacs's oil is in the lower position of wall 4
displayed(isaacs, oil, 4, lower).

% Given conditions from the question:
% Isaacs's watercolor is displayed on wall 2 (position not specified)
1 { displayed(isaacs, watercolor, 2, upper) ; displayed(isaacs, watercolor, 2, lower) } 1.

% Franz's oil is displayed on wall 3 (position not specified)
1 { displayed(franz, oil, 3, upper) ; displayed(franz, oil, 3, lower) } 1.

% Map the correct answer to option/1 (MANDATORY)
% Option A: Franz's watercolor is displayed on wall 1
option(a) :- displayed(franz, watercolor, 1, _).

% Option B: Greene's oil is displayed on wall 1
option(b) :- displayed(greene, oil, 1, _).

% Option C: Greene's watercolor is displayed on wall 1
option(c) :- displayed(greene, watercolor, 1, _).

% Option D: Hidalgo's oil is displayed on wall 1
option(d) :- displayed(hidalgo, oil, 1, _).

% Option E: Hidalgo's watercolor is displayed on wall 1
option(e) :- displayed(hidalgo, watercolor, 1, _).

#show option/1.