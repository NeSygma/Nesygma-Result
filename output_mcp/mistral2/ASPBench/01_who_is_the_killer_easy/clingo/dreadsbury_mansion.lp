% Declare people
person(agatha).
person(butler).
person(charles).

% Agatha is the victim
victim(agatha).

% Charles hates no one that Agatha hates
:- hates(agatha, X), hates(charles, X).

% Agatha hates everybody except the butler
hates(agatha, butler).
:- person(X), X != butler, not hates(agatha, X).

% The butler hates everyone not richer than Aunt Agatha
hates(butler, X) :- person(X), not richer(X, agatha).

% The butler hates everyone whom Agatha hates
hates(butler, X) :- hates(agatha, X).

% No one hates everyone
:- person(P), not (hates(P, X) : person(X)).

% Killer always hates their victim
:- killer(K), victim(V), not hates(K, V).

% Killer is no richer than their victim
:- killer(K), victim(V), richer(K, V).

% Choice rule: exactly one killer
{ killer(P) : person(P) } 1.

% Map killer to name
killer_name(agatha) :- killer(agatha).
killer_name(butler) :- killer(butler).
killer_name(charles) :- killer(charles).

% Show the answer
#show killer/1.
#show killer_name/1.

% Allow richer/2 to be open (Clingo will explore possible relations)
{ richer(P1, P2) : person(P1), person(P2) }.

% Ensure reflexive richer is not considered (optional, but clarifies)
:- richer(P, P).