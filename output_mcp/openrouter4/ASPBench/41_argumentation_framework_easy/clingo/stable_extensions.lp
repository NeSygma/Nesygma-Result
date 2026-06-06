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

% An argument is either in the extension or not
{ in(X) } :- arg(X).

% Constraint 1: Conflict-free - No argument in the extension may attack another argument in the same extension
:- in(X), in(Y), att(X, Y), X != Y.

% Constraint 2: Self-defending - For every argument in the extension, all its attackers must be attacked by some argument in the extension
% An attacker of X is Y such that Y attacks X
% For any X in the extension and any Y that attacks X, there must exist some Z in the extension such that Z attacks Y
:- in(X), att(Y, X), not defended_attacker(Y, X).
defended_attacker(Y, X) :- in(X), att(Y, X), in(Z), att(Z, Y).

% Constraint 3: Maximality (Stable) - Every argument not in the extension must be attacked by some argument in the extension
:- arg(X), not in(X), not attacked_by_extension(X).
attacked_by_extension(X) :- arg(X), not in(X), in(Y), att(Y, X).

% Show the extensions
#show in/1.