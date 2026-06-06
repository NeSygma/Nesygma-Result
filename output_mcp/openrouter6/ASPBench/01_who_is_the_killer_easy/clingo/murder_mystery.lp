% Murder Mystery in Dreadsbury Mansion
% People
person(0). person(1). person(2).
name(0,"Agatha"). name(1,"Butler"). name(2,"Charles").

% Victim
victim(0).

% Exactly one killer
1 {killer(K) : person(K)} 1.

% Wealth levels: each person gets a wealth level from 1 to 3
{wealth(X, W) : W = 1..3} 1 :- person(X).

% Richer relation: X is richer than Y if wealth(X) > wealth(Y)
richer(X, Y) :- wealth(X, W1), wealth(Y, W2), W1 > W2.

% Hatred: choice for all pairs
{hate(X, Y)} :- person(X), person(Y).

% Constraint 4: Agatha hates everybody except the butler
hate(0, X) :- person(X), X != 1.
:- hate(0, 1).  % she does not hate the butler

% Constraint 6: Butler hates everyone whom Agatha hates
hate(1, X) :- hate(0, X).

% Constraint 5: Butler hates everyone not richer than Agatha
% "not richer than Agatha" means wealth(X) <= wealth(0)
hate(1, X) :- person(X), wealth(X, Wx), wealth(0, W0), Wx <= W0.

% Constraint 3: Charles hates no one that Agatha hates
:- hate(0, X), hate(2, X).

% Constraint 1: Killer always hates their victim (Agatha)
hate(K, 0) :- killer(K).

% Constraint 2: Killer is no richer than victim (Agatha)
% i.e., not richer(K, 0)
:- killer(K), richer(K, 0).

% Constraint 7: No one hates everyone
:- person(X), hate(X, 0), hate(X, 1), hate(X, 2).

% Derive killer name
killer_name(N) :- killer(K), name(K, N).

% Show the solution
#show killer/1.
#show killer_name/1.