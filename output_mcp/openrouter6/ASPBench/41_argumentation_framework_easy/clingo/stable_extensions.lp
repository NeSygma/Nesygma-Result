% Abstract Argumentation Framework: Stable Extensions

% Arguments
argument(a). argument(b). argument(c). argument(d). argument(e). argument(f).

% Attack relations
attacks(a, b).
attacks(b, c).
attacks(c, d).
attacks(d, e).
attacks(e, f).
attacks(f, a).
attacks(b, f).
attacks(d, b).

% Choice rule for extension membership
{ in_ext(X) } :- argument(X).

% Helper predicates
% defended_attacker(Y): Y is attacked by some argument in the extension
defended_attacker(Y) :- in_ext(Z), attacks(Z, Y).

% attacked_by_ext(X): X is attacked by some argument in the extension
attacked_by_ext(X) :- in_ext(Z), attacks(Z, X).

% Constraints
% 1. Conflict-free: no two arguments in extension attack each other
:- in_ext(X), in_ext(Y), attacks(X, Y).

% 2. Self-defending: every attacker of an argument in extension must be defended
:- in_ext(X), attacks(Y, X), not defended_attacker(Y).

% 3. Maximality: every argument not in extension must be attacked by extension
:- argument(X), not in_ext(X), not attacked_by_ext(X).

% Show the extension members
#show in_ext/1.