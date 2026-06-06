% Domain
student(franz; greene; hidalgo; isaacs).
type(oil; watercolor).
wall(1;2;3;4).
position(upper; lower).

% Each student's each type is assigned to exactly one wall-position
{ assigned(S, T, W, P) : wall(W), position(P) } 1 :- student(S), type(T).

% Each wall-position gets exactly one painting
{ assigned(S, T, W, P) : student(S), type(T) } 1 :- wall(W), position(P).

% Constraint 1: No wall has only watercolors
:- wall(W), not { assigned(S, oil, W, _) : student(S) } >= 1.

% Constraint 2: No wall has work of only one student
:- wall(W), #count{ S : assigned(S, _, W, _) } = 1.

% Constraint 3: No wall has both Franz and Isaacs
:- wall(W), assigned(franz, _, W, _), assigned(isaacs, _, W, _).

% Constraint 4: Greene's watercolor is upper on the wall with Franz's oil
:- assigned(franz, oil, W, _), not assigned(greene, watercolor, W, upper).
:- assigned(greene, watercolor, W, upper), not assigned(franz, oil, W, _).

% Constraint 5: Isaacs's oil is lower on wall 4
assigned(isaacs, oil, 4, lower).

% Check each option
option_a_true :- assigned(franz, watercolor, W, _), assigned(greene, oil, W, _), wall(W).
option_b_true :- assigned(franz, watercolor, W, _), assigned(hidalgo, oil, W, _), wall(W).
option_c_true :- assigned(greene, oil, _, upper).
option_d_true :- assigned(hidalgo, watercolor, _, lower).
option_e_true :- assigned(isaacs, watercolor, W, _), assigned(hidalgo, oil, W, _), wall(W).

#show option_a_true/0.
#show option_b_true/0.
#show option_c_true/0.
#show option_d_true/0.
#show option_e_true/0.