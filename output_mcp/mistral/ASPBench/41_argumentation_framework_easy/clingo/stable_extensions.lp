% Define the arguments
argument(a). argument(b). argument(c). argument(d). argument(e). argument(f).

% Define the attack relations
attacks(a,b).
attacks(b,c).
attacks(c,d).
attacks(d,e).
attacks(e,f).
attacks(f,a).
attacks(b,f).
attacks(d,b).

% Generate possible extensions
{in(X) : argument(X)}.

% Conflict-free: No argument attacks another in the extension
:- in(X), in(Y), attacks(X,Y).

% Self-defending: For every argument in the extension, all its attackers must be attacked by the extension
:- in(X), attacks(Y,X), not in(Z) : attacks(Z,Y).

% Maximality: Every argument not in the extension is attacked by the extension
:- argument(X), not in(X), not in(Y) : attacks(Y,X).

% Show the stable extensions
#show in/1.