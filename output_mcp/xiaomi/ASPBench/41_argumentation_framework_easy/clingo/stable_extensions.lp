% Arguments
arg(a). arg(b). arg(c). arg(d). arg(e). arg(f).

% Attack relations
attacks(a, b).
attacks(b, c).
attacks(c, d).
attacks(d, e).
attacks(e, f).
attacks(f, a).
attacks(b, f).
attacks(d, b).

% Choose which arguments are in the extension
{ in(X) } :- arg(X).

% An argument is attacked by the extension if some member attacks it
attacked_by_in(Y) :- in(X), attacks(X, Y).

% Constraint 1: Conflict-free - no two arguments in the extension attack each other
:- in(X), in(Y), attacks(X, Y).

% Constraint 2: Self-defending - for every argument in the extension,
% all its attackers must be attacked by some argument in the extension
:- in(Y), attacks(X, Y), not attacked_by_in(X).

% Constraint 3: Maximality - every argument not in the extension must be attacked
:- arg(X), not in(X), not attacked_by_in(X).

% Show the extension members
#show in/1.