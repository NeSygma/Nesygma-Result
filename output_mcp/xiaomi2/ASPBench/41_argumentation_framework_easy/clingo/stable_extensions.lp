% ===== Domain: Arguments =====
arg(a). arg(b). arg(c). arg(d). arg(e). arg(f).

% ===== Attack Relations =====
attacks(a, b).
attacks(b, c).
attacks(c, d).
attacks(d, e).
attacks(e, f).
attacks(f, a).
attacks(b, f).
attacks(d, b).

% ===== Choice: Select which arguments are in the extension =====
{ in(X) } :- arg(X).

% ===== Derived: An argument is attacked by the extension if some member attacks it =====
attacked_by_in(Y) :- in(X), attacks(X, Y).

% ===== Constraint 1: Conflict-free =====
% No two arguments in the extension may attack each other
:- in(X), in(Y), attacks(X, Y).

% ===== Constraint 2: Self-defending =====
% For every argument in the extension, all its attackers must be attacked by the extension
:- in(X), attacks(Y, X), not attacked_by_in(Y).

% ===== Constraint 3: Stability (attacks all outside) =====
% Every argument NOT in the extension must be attacked by the extension
:- arg(X), not in(X), not attacked_by_in(X).

% ===== Display =====
#show in/1.