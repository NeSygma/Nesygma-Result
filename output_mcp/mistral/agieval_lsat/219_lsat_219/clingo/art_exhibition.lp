% Domains
student(franz; greene; hidalgo; isaacs).
painting_type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student has exactly one oil and one watercolor
1 { has_painting(S, T) : painting_type(T) } 2 :- student(S).

% Each wall has exactly one upper and one lower painting
1 { displayed(W, P, S, T) : student(S), painting_type(T) } 1 :- wall(W), position(P).

% Each student has exactly one painting per type
:- student(S), painting_type(T), #count{P : displayed(_, P, S, T)} != 1.

% No wall has only watercolors
:- wall(W), not has_oil(W).
has_oil(W) :- wall(W), displayed(W, _, _, oil).

% No wall has only one student
:- wall(W), #count{S : displayed(W, _, S, _)} = 1.

% No wall has both Franz and Isaacs
:- wall(W), displayed(W, _, franz, _), displayed(W, _, isaacs, _).

% Greene's watercolor is upper where Franz's oil is lower
:- displayed(W, lower, franz, oil), not displayed(W, upper, greene, watercolor).
:- displayed(W, upper, greene, watercolor), not displayed(W, lower, franz, oil).

% Isaacs's oil is lower on wall 4
displayed(4, lower, isaacs, oil).

% Define which options are valid based on lower positions
valid_option(a) :-
    displayed(1, lower, franz, oil),
    displayed(2, lower, franz, watercolor),
    displayed(3, lower, greene, oil),
    displayed(4, lower, isaacs, oil).

valid_option(b) :-
    displayed(1, lower, franz, oil),
    displayed(2, lower, hidalgo, watercolor),
    displayed(3, lower, isaacs, watercolor),
    displayed(4, lower, isaacs, oil).

valid_option(c) :-
    displayed(1, lower, greene, oil),
    displayed(2, lower, franz, oil),
    displayed(3, lower, isaacs, oil),
    displayed(4, lower, hidalgo, oil).

valid_option(d) :-
    displayed(1, lower, hidalgo, oil),
    displayed(2, lower, greene, oil),
    displayed(3, lower, greene, watercolor),
    displayed(4, lower, isaacs, oil).

valid_option(e) :-
    displayed(1, lower, hidalgo, watercolor),
    displayed(2, lower, franz, oil),
    displayed(3, lower, greene, oil),
    displayed(4, lower, isaacs, oil).

% Exactly one option is valid
1 { answer(X) : valid_option(X) } 1.

% Map the correct answer to option/1
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.