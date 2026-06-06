% Persons
person(0..2).
% Names
name(0,"Agatha").
name(1,"Butler").
name(2,"Charles").
% Define butler constant
butler(1).
% Choice for richer relation (open)
{ richer(X,Y) } :- person(X), person(Y), X != Y.
% Choice for hates relation (open)
{ hates(X,Y) } :- person(X), person(Y), X != Y.
% Exactly one killer
1 { killer(P) : person(P) } 1.
% Constraint 1: killer hates victim (Agatha is 0)
:- killer(K), not hates(K,0).
% Constraint 2: killer not richer than victim
:- killer(K), richer(K,0).
% Constraint 3: Charles hates no one that Agatha hates
:- hates(2,Y), hates(0,Y).
% Constraint 4: Agatha hates everybody except the butler (person 1)
% Force hates for all Y != 1
hates(0,Y) :- person(Y), Y != 1.
% Prohibit hate towards butler
:- hates(0,1).
% Constraint 5: Butler hates everyone not richer than Agatha
hates(1,Y) :- person(Y), not richer(Y,0).
% Constraint 6: Butler hates everyone whom Agatha hates
hates(1,Y) :- hates(0,Y).
% Constraint 7: No one hates everyone
some_not_hated(X) :- person(X), person(Y), not hates(X,Y).
:- person(X), not some_not_hated(X).
% Show results
killer_name(N) :- killer(P), name(P,N).
#show killer/1.
#show killer_name/1.