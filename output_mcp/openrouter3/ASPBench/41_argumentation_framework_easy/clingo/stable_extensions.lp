% Abstract Argumentation Framework - Stable Extensions

% Arguments
argument(a). argument(b). argument(c). argument(d). argument(e). argument(f).

% Attack relations (directed)
attacks(a, b).
attacks(b, c).
attacks(c, d).
attacks(d, e).
attacks(e, f).
attacks(f, a).
attacks(b, f).
attacks(d, b).

% Choice rule for extension membership
{ in_extension(X) } :- argument(X).

% 1. Conflict-free: No argument in extension attacks another in extension
:- in_extension(X), in_extension(Y), attacks(X, Y).

% 2. Self-defending: For every argument in extension, all its attackers must be attacked by some argument in extension
% Helper: attacker(X, Y) means Y attacks X
attacker(X, Y) :- attacks(Y, X).

% For each argument in extension, each of its attackers must be attacked by some argument in extension
:- in_extension(X), attacker(X, Y), not attacked_by_extension(Y).

% Helper: Y is attacked by some argument in extension
attacked_by_extension(Y) :- in_extension(Z), attacks(Z, Y).

% 3. Maximality: Every argument not in extension must be attacked by some argument in extension
:- argument(X), not in_extension(X), not attacked_by_extension(X).

% Show all stable extensions
#show in_extension/1.