% People
person(0..2).
name(0, "Agatha").
name(1, "Butler").
name(2, "Charles").

% Killer choice
1 { killer(K) : person(K) } 1.

% Relations
{ hates(X, Y) } :- person(X), person(Y).
{ richer(X, Y) } :- person(X), person(Y).

% Constraint 1: A killer always hates their victim (Agatha is 0)
:- killer(K), not hates(K, 0).

% Constraint 2: A killer is no richer than their victim
:- killer(K), richer(K, 0).

% Constraint 3: Charles (2) hates no one that Agatha (0) hates
:- hates(2, Y), hates(0, Y).

% Constraint 4: Agatha hates everybody except the butler (1)
hates(0, 0).
hates(0, 2).
:- hates(0, 1).

% Constraint 5: The butler (1) hates everyone not richer than Aunt Agatha (0)
hates(1, X) :- person(X), not richer(X, 0).

% Constraint 6: The butler (1) hates everyone whom Agatha (0) hates
hates(1, X) :- person(X), hates(0, X).

% Constraint 7: No one hates everyone
:- person(X), #count { Y : hates(X, Y) } = 3.

% Additional logical constraints for richer
:- richer(X, X).
:- richer(X, Y), richer(Y, X).

% Output
killer_name(Name) :- killer(K), name(K, Name).
#show killer/1.
#show killer_name/1.