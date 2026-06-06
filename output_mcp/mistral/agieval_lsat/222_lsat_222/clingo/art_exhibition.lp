% Base facts
student(franz; greene; hidalgo; isaacs).
painting_type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student displays exactly one oil and one watercolor
% Use choice rules to assign paintings to students
{ displayed(S, oil, W, P) : wall(W), position(P) } 1 :- student(S).
{ displayed(S, watercolor, W, P) : wall(W), position(P) } 1 :- student(S).

% Each wall has exactly one upper and one lower painting
{ displayed(S, T, W, upper) : student(S), painting_type(T) } 1 :- wall(W).
{ displayed(S, T, W, lower) : student(S), painting_type(T) } 1 :- wall(W).

% No wall has only watercolors (at least one oil per wall)
has_oil(W) :- displayed(_, oil, W, _).
:- wall(W), not has_oil(W).

% No wall has only one student's work
:- wall(W), #count{ S : displayed(S, _, W, _) } = 1.

% No wall has both Franz and Isaacs
:- wall(W), displayed(franz, _, W, _), displayed(isaacs, _, W, _).

% Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
displayed(greene, watercolor, W, upper) :- displayed(franz, oil, W, _).

% Isaacs's oil is in the lower position of wall 4
displayed(isaacs, oil, 4, lower).

% Helper predicate: Greene's oil and Franz's watercolor are on the same wall
same_wall_greene_franz_oil_water(W) :-
    displayed(greene, oil, W, _),
    displayed(franz, watercolor, W, _).

% Enforce the condition that Greene's oil is on the same wall as Franz's watercolor
:- not same_wall_greene_franz_oil_water(_).

% --- Answer Mapping ---
% (A) Greene's oil is displayed in an upper position.
option(a) :- displayed(greene, oil, _, upper).

% (B) Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
option(b) :- displayed(hidalgo, watercolor, W, _), displayed(isaacs, watercolor, W, _).

% (C) Hidalgo's oil is displayed in an upper position.
option(c) :- displayed(hidalgo, oil, _, upper).

% (D) Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
option(d) :- displayed(hidalgo, oil, W, _), displayed(isaacs, watercolor, W, _).

% (E) Isaacs's watercolor is displayed in a lower position.
option(e) :- displayed(isaacs, watercolor, _, lower).

#show option/1.