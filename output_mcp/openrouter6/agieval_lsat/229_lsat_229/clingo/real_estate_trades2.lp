% Real Estate Trading Problem - Generic Model

% Buildings and their classes
building(garza). class(garza, 1).
building(yates). class(yates, 3).
building(zimmer). class(zimmer, 3).
building(flores). class(flores, 1).
building(lynch). class(lynch, 2).
building(king). class(king, 2).
building(meyer). class(meyer, 2).
building(ortiz). class(ortiz, 2).

% Companies
company(realprop). company(southco). company(trustcorp).

% Initial ownership at time 0
owns(realprop, garza, 0).
owns(realprop, yates, 0).
owns(realprop, zimmer, 0).
owns(southco, flores, 0).
owns(southco, lynch, 0).
owns(trustcorp, king, 0).
owns(trustcorp, meyer, 0).
owns(trustcorp, ortiz, 0).

% Time horizon: 0..5 (allow up to 5 trades)
time(0..5).

% Persistence of ownership unless changed
owns(C, B, T+1) :- owns(C, B, T), time(T), time(T+1), not changed(C, B, T).

% Exclusivity: a building cannot be owned by two companies at the same time
:- owns(C1, B, T), owns(C2, B, T), C1 != C2.

% Trade types: we will generate trades via choice rules
% For each time step, we can choose a trade of one of the three kinds
% We'll define a trade as a tuple (T, A, B, Type, X, Y, Z) where X is given by A, Y and Z given by B (for type2/3)
% For type1, Y is given by B, Z is unused.

% Domain of possible trades: we need to consider all possible pairs of companies and buildings
% But we can let Clingo choose via constraints.

% Choice rule: at each time step, we can choose at most one trade (or none)
% We'll define a predicate trade(T, A, B, Type, X, Y, Z) that holds if a trade occurs at time T.

% For type1: choose two companies A != B, choose building X owned by A, building Y owned by B, same class
{ trade(T, A, B, 1, X, Y, none) : company(A), company(B), A != B, building(X), building(Y), class(X, C), class(Y, C), owns(A, X, T), owns(B, Y, T) } 1 :- time(T), T < 5.

% For type2: choose A != B, X owned by A class 1, Y and Z owned by B class 2, Y != Z
{ trade(T, A, B, 2, X, Y, Z) : company(A), company(B), A != B, building(X), class(X, 1), building(Y), class(Y, 2), building(Z), class(Z, 2), Y != Z, owns(A, X, T), owns(B, Y, T), owns(B, Z, T) } 1 :- time(T), T < 5.

% For type3: choose A != B, X owned by A class 2, Y and Z owned by B class 3, Y != Z
{ trade(T, A, B, 3, X, Y, Z) : company(A), company(B), A != B, building(X), class(X, 2), building(Y), class(Y, 3), building(Z), class(Z, 3), Y != Z, owns(A, X, T), owns(B, Y, T), owns(B, Z, T) } 1 :- time(T), T < 5.

% Effects of trades: changed ownership at time T
% For each trade, we mark the buildings that change hands
changed(A, X, T) :- trade(T, A, B, Type, X, _, _).
changed(B, Y, T) :- trade(T, A, B, 1, _, Y, _).
changed(B, Y, T) :- trade(T, A, B, 2, _, Y, _).
changed(B, Z, T) :- trade(T, A, B, 2, _, _, Z).
changed(B, Y, T) :- trade(T, A, B, 3, _, Y, _).
changed(B, Z, T) :- trade(T, A, B, 3, _, _, Z).

% New ownership at T+1
owns(B, X, T+1) :- trade(T, A, B, Type, X, _, _), time(T), time(T+1).
owns(A, Y, T+1) :- trade(T, A, B, 1, _, Y, _), time(T), time(T+1).
owns(A, Y, T+1) :- trade(T, A, B, 2, _, Y, _), time(T), time(T+1).
owns(A, Z, T+1) :- trade(T, A, B, 2, _, _, Z), time(T), time(T+1).
owns(A, Y, T+1) :- trade(T, A, B, 3, _, Y, _), time(T), time(T+1).
owns(A, Z, T+1) :- trade(T, A, B, 3, _, _, Z), time(T), time(T+1).

% Final ownership at time 5 (or last time step)
final_owns(C, B) :- owns(C, B, 5).

% Condition: Trustcorp owns no class 2 buildings at the end
:- final_owns(trustcorp, B), class(B, 2).

% Derive statements
% (A) RealProp owns a class 1 building
realprop_class1 :- final_owns(realprop, B), class(B, 1).

% (B) Southco owns only class 2 buildings
southco_only_class2 :-
    not (final_owns(southco, B), class(B, 1)),
    not (final_owns(southco, B), class(B, 3)).

% (C) Southco has made at least one trade with Trustcorp
southco_trustcorp_trade :-
    trade(T, southco, trustcorp, _, _, _, _).
southco_trustcorp_trade :-
    trade(T, trustcorp, southco, _, _, _, _).

% (D) Trustcorp owns the Garza Tower
trustcorp_garza :- final_owns(trustcorp, garza).

% (E) Trustcorp owns the Zimmer House
trustcorp_zimmer :- final_owns(trustcorp, zimmer).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- realprop_class1.
option(b) :- southco_only_class2.
option(c) :- southco_trustcorp_trade.
option(d) :- trustcorp_garza.
option(e) :- trustcorp_zimmer.

#show option/1.