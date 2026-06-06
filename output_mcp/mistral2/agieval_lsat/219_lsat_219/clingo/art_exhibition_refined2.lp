% Domains
student(franz; greene; hidalgo; isaacs).
type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student has exactly one oil and one watercolor
1 { painting(S, oil) : student(S) } 1 :- student(S).
1 { painting(S, watercolor) : student(S) } 1 :- student(S).

% Each wall has exactly one painting in the upper and one in the lower position
1 { displayed(W, upper, S, T) : student(S), type(T) } 1 :- wall(W).
1 { displayed(W, lower, S, T) : student(S), type(T) } 1 :- wall(W).

% No wall has only watercolors
:- wall(W), { displayed(W, upper, _, watercolor) ; displayed(W, lower, _, watercolor) } = 2.

% No wall has only one student's work
:- wall(W), { displayed(W, upper, S, _) ; displayed(W, lower, S, _) } = 1.

% No wall has both Franz and Isaacs' paintings
:- wall(W), displayed(W, upper, franz, _), displayed(W, lower, isaacs, _).
:- wall(W), displayed(W, upper, isaacs, _), displayed(W, lower, franz, _).

% Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
:- displayed(W, upper, greene, watercolor),
   not (displayed(W, upper, franz, oil) ; displayed(W, lower, franz, oil)).

% Isaacs's oil is in the lower position of wall 4
:- not displayed(4, lower, isaacs, oil).

% Answer mapping
% Option A: Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil
option(a) :-
    displayed(1, lower, franz, oil),
    displayed(2, lower, franz, watercolor),
    displayed(3, lower, greene, oil),
    displayed(4, lower, isaacs, oil).

% Option B: Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil
option(b) :-
    displayed(1, lower, franz, oil),
    displayed(2, lower, hidalgo, watercolor),
    displayed(3, lower, isaacs, watercolor),
    displayed(4, lower, isaacs, oil).

% Option C: Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil
option(c) :-
    displayed(1, lower, greene, oil),
    displayed(2, lower, franz, oil),
    displayed(3, lower, isaacs, oil),
    displayed(4, lower, hidalgo, oil).

% Option D: Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil
option(d) :-
    displayed(1, lower, hidalgo, oil),
    displayed(2, lower, greene, oil),
    displayed(3, lower, greene, watercolor),
    displayed(4, lower, isaacs, oil).

% Option E: Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil
option(e) :-
    displayed(1, lower, hidalgo, watercolor),
    displayed(2, lower, franz, oil),
    displayed(3, lower, greene, oil),
    displayed(4, lower, isaacs, oil).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.