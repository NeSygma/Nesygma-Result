% Arguments
arg(a). arg(b). arg(c). arg(d). arg(e). arg(f).

% Attack relations
attack(a,b). attack(b,c). attack(c,d). attack(d,e). attack(e,f). attack(f,a). attack(b,f). attack(d,b).

% Choice rule: decide which arguments are in extension
{ in_ext(X) } :- arg(X).

% Conflict-free: no two arguments in extension attack each other
:- in_ext(X), in_ext(Y), attack(X,Y).

% Self-defending: for each argument in extension, all its attackers must be attacked by some argument in extension
:- in_ext(X), attack(Y,X), not in_ext(Z), attack(Z,Y).

% Maximality: every argument not in extension must be attacked by some argument in extension
:- not in_ext(X), arg(Y), not attack(Y,X), in_ext(Y).

#show in_ext/1.