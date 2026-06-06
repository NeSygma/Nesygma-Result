% Arguments
arg(a; b; c; d; e; f).

% Attack relations
att(a, b).
att(b, c).
att(c, d).
att(d, e).
att(e, f).
att(f, a).
att(b, f).
att(d, b).

% Each argument is either in the extension or not
{ in(X) } :- arg(X).

% 1. Conflict-free: No argument in the extension attacks another in the extension
:- in(X), in(Y), att(X, Y).

% 2. Self-defending: For every argument in the extension, all its attackers must be attacked by some argument in the extension
% An attacker of X is an argument Y such that att(Y, X)
% For each in(X), for each attacker Y of X, there must exist some Z in the extension such that att(Z, Y)
:- in(X), att(Y, X), not defended(X, Y).

% defended(X, Y) holds if there exists Z in the extension such that att(Z, Y)
defended(X, Y) :- in(X), att(Y, X), in(Z), att(Z, Y).

% 3. Maximality: Every argument not in the extension must be attacked by some argument in the extension
:- arg(X), not in(X), not attacked_by_extension(X).

attacked_by_extension(X) :- arg(X), in(Y), att(Y, X).

% Show the extension
#show in/1.