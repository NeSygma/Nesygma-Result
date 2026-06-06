% Arguments
arg(a). arg(b). arg(c). arg(d). arg(e). arg(f).

% Attack Relations
attack(a, b).
attack(b, c).
attack(c, d).
attack(d, e).
attack(e, f).
attack(f, a).
attack(b, f).
attack(d, b).

% Choice rule: define a subset of arguments
{ in(X) } :- arg(X).
out(X) :- arg(X), not in(X).

% 1. Conflict-free: No argument in the extension may attack another argument in the same extension
:- in(X), in(Y), attack(X, Y).

% 2. Stable: Every argument not in the extension must be attacked by some argument in the extension
attacked_by_in(X) :- in(Y), attack(Y, X).
:- out(X), not attacked_by_in(X).

% Output the stable extensions
#show in/1.