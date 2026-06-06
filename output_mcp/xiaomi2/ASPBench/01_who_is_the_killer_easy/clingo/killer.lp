% Persons
person(agatha).
person(butler).
person(charles).

% Victim
victim(agatha).

% Index and name mapping
index(agatha,0).
index(butler,1).
index(charles,2).
name(agatha,"Agatha").
name(butler,"Butler").
name(charles,"Charles").

% Choose exactly one killer
1 { killed_by(X) : person(X) } 1.

% Open relations: hates and richer (choice)
{ hates(X,Y) } :- person(X), person(Y).
{ richer(X,Y) } :- person(X), person(Y).

% Irreflexivity of richer (no one is richer than themselves)
:- richer(X,X).

% Constraint 1: Killer hates victim
hates(X, Y) :- killed_by(X), victim(Y).

% Constraint 2: Killer is no richer than victim
:- killed_by(X), victim(Y), richer(X,Y).

% Constraint 3: Charles hates no one that Agatha hates
:- hates(agatha, X), hates(charles, X).

% Constraint 4: Agatha hates everybody except the butler
hates(agatha, X) :- person(X), X != butler.
:- hates(agatha, butler).

% Constraint 5: Butler hates everyone not richer than Aunt Agatha
hates(butler, X) :- person(X), not richer(X, agatha).

% Constraint 6: Butler hates everyone whom Agatha hates
hates(butler, X) :- hates(agatha, X).

% Constraint 7: No one hates everyone
:- person(X), hates(X, agatha), hates(X, butler), hates(X, charles).

% Output killer index and name
killer(I) :- killed_by(X), index(X,I).
killer_name(N) :- killed_by(X), name(X,N).

#show killer/1.
#show killer_name/1.