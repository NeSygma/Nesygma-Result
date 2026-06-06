% People in Dreadsbury Mansion
person(0..2).

% Names for output
name(0, "Agatha").
name(1, "Butler").
name(2, "Charles").

% Victim is Agatha (0)
victim(0).

% Exactly one killer, and it's not Agatha (someone else killed her)
1 { killer(K) : person(K) } 1.
:- killer(0).  % Agatha didn't kill herself

% Constraint 1: Killer always hates their victim
% If K is killer and V is victim, then K hates V
hates(K, V) :- killer(K), victim(V).

% Constraint 2: Killer is no richer than their victim
% Cannot be that killer is richer than victim
:- killer(K), victim(V), richer(K, V).

% Constraint 3: Charles hates no one that Agatha hates
% (Charles=2, Agatha=0)
:- hates(0, X), hates(2, X).

% Constraint 4: Agatha hates everybody except the butler
% Agatha hates Charles (2) but not Butler (1)
hates(0, 2).
:- hates(0, 1).

% Constraint 5: The butler hates everyone not richer than Aunt Agatha
% Butler=1, Agatha=0
% If X is not richer than Agatha (i.e., not richer(X, 0)), then Butler hates X
hates(1, X) :- person(X), not richer(X, 0).

% Constraint 6: The butler hates everyone whom Agatha hates
hates(1, X) :- hates(0, X).

% Constraint 7: No one hates everyone
% For each person P, the number of people they hate is less than 3
:- person(P), { hates(P, Q) : person(Q) } = 3.

% Define the richer relation (wealth ordering)
% We allow Clingo to determine a consistent wealth ordering
{ richer(X, Y) : person(X), person(Y), X != Y }.

% Make richer transitive
richer(X, Z) :- richer(X, Y), richer(Y, Z).

% Antisymmetry: if X is richer than Y, Y is not richer than X
:- richer(X, Y), richer(Y, X).

% Show the killer and their name
killer_name(N) :- killer(K), name(K, N).

% Output the solution
#show killer/1.
#show killer_name/1.