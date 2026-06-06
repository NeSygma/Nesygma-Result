% Arguments
arg(a). arg(b). arg(c). arg(d). arg(e). arg(f).
% Attack relations
attacks(a,b).
attacks(b,c).
attacks(c,d).
attacks(d,e).
attacks(e,f).
attacks(f,a).
attacks(b,f).
attacks(d,b).
% Choice of arguments in extension
{in(X)} :- arg(X).
% Helper: arguments attacked by the extension
attacked_by_in(Y) :- in(Z), attacks(Z,Y).
% Conflict-free constraint
:- in(X), in(Y), attacks(X,Y).
% Self-defending constraint
:- in(X), attacks(Y,X), not attacked_by_in(Y).
% Maximality (stable) constraint: every outside argument must be attacked
:- arg(X), not in(X), not attacked_by_in(X).
#show in/1.