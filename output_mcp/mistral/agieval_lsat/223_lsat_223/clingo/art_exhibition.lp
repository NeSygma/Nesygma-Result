% Domains
student(franz; greene; hidalgo; isaacs).
painting_type(oil; watercolor).
wall(1..4).
position(upper; lower).

% Each student displays exactly one oil and one watercolor
1 { displayed(S, oil, W, P) : wall(W), position(P) } 1 :- student(S).
1 { displayed(S, watercolor, W, P) : wall(W), position(P) } 1 :- student(S).

% Each wall has exactly one upper and one lower painting
1 { displayed(S, T, W, upper) : student(S), painting_type(T) } 1 :- wall(W).
1 { displayed(S, T, W, lower) : student(S), painting_type(T) } 1 :- wall(W).

% No wall has only watercolors (must have at least one oil)
:- wall(W), { displayed(S, watercolor, W, P) : student(S), position(P) } = 2.

% No wall has only one student's work (must have at least two students)
:- wall(W), { displayed(S, _, W, _) : student(S) } = 1.

% No wall has both Franz and Isaacs
:- wall(W), displayed(franz, _, W, _), displayed(isaacs, _, W, _).

% Greene's watercolor is in upper position of wall where Franz's oil is displayed
:- displayed(franz, oil, W, _), not displayed(greene, watercolor, W, upper).
:- displayed(greene, watercolor, W, upper), not displayed(franz, oil, W, _).

% Isaacs's oil is in lower position of wall 4
displayed(isaacs, oil, 4, lower).

% Franz's oil is displayed on wall 1 (position not specified, so allow either)
{ displayed(franz, oil, 1, P) : position(P) } 1.

% Map the correct answer to option/1
option(a) :- displayed(franz, watercolor, 4, _).
option(b) :- displayed(greene, oil, 2, _).
option(c) :- displayed(greene, watercolor, 2, _).
option(d) :- displayed(hidalgo, watercolor, 3, _).
option(e) :- displayed(isaacs, oil, 1, _).

#show option/1.