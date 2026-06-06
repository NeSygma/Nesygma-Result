% Dreadsbury Mansion Murder Mystery
% People: 0=Agatha, 1=Butler, 2=Charles

% Domain
person(0). person(1). person(2).
victim(0). % Agatha is the victim

% Open relations - allow Clingo to explore possibilities
{ hate(X, Y) } :- person(X), person(Y), X != Y.
{ richer(X, Y) } :- person(X), person(Y), X != Y.

% Constraint 1: Killer always hates their victim
killer(K) :- hate(K, 0), not killer(0), not killer(1), not killer(2).

% Constraint 2: Killer is no richer than victim (victim is Agatha=0)
% "No richer than" means richer(K, 0) is FALSE
:- killer(K), richer(K, 0).

% Constraint 3: Charles hates no one that Agatha hates
% If Agatha hates Y, then Charles does NOT hate Y
:- hate(0, Y), hate(2, Y).

% Constraint 4: Agatha hates everybody except the butler
% Agatha hates Charles (2) but not Butler (1)
hate(0, 2). % Agatha hates Charles
:- hate(0, 1). % Agatha does NOT hate Butler

% Constraint 5: Butler hates everyone not richer than Agatha
% If someone is NOT richer than Agatha, Butler hates them
% "Not richer than" means richer(X, 0) is FALSE
hate(1, X) :- person(X), X != 1, not richer(X, 0).

% Constraint 6: Butler hates everyone whom Agatha hates
% If Agatha hates Y, Butler hates Y too
hate(1, Y) :- hate(0, Y).

% Constraint 7: No one hates everyone
% For each person X, there exists some person Y (Y != X) that X does NOT hate
% We need to ensure that for each X, there is at least one Y that X doesn't hate
:- person(X), not (person(Y), X != Y, not hate(X, Y)).

% Constraint 8: Agatha is the victim (already defined)

% Ensure exactly one killer
1 { killer(X) : person(X) } 1.

% Show the solution
#show killer/1.
#show hate/2.
#show richer/2.