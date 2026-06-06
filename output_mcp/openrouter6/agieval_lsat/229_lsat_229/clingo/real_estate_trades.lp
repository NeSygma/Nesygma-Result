% Real Estate Trading Problem
% Companies: realprop, southco, trustcorp
% Buildings with classes

building(garza). class(garza, 1).
building(yates). class(yates, 3).
building(zimmer). class(zimmer, 3).
building(flores). class(flores, 1).
building(lynch). class(lynch, 2).
building(king). class(king, 2).
building(meyer). class(meyer, 2).
building(ortiz). class(ortiz, 2).

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

% Time horizon: 0..2 (allow up to 2 trades)
time(0..2).

% Persistence of ownership unless changed
owns(C, B, T+1) :- owns(C, B, T), time(T), time(T+1), not changed(C, B, T).

% Trade definitions: ID, Type, A, B, X, Y, Z
% Type1: swap same class (X from A, Y from B)
% Type2: A gives class1 X to B, B gives two class2 Y,Z to A
% Type3: A gives class2 X to B, B gives two class3 Y,Z to A

% Type1 swaps
trade_def(1, type1, realprop, southco, garza, flores, none).
trade_def(2, type1, southco, trustcorp, lynch, king, none).
trade_def(3, type1, southco, trustcorp, lynch, meyer, none).
trade_def(4, type1, southco, trustcorp, lynch, ortiz, none).

% Type2 trades
trade_def(5, type2, realprop, trustcorp, garza, king, meyer).
trade_def(6, type2, realprop, trustcorp, garza, king, ortiz).
trade_def(7, type2, realprop, trustcorp, garza, meyer, ortiz).
trade_def(8, type2, southco, trustcorp, flores, king, meyer).
trade_def(9, type2, southco, trustcorp, flores, king, ortiz).
trade_def(10, type2, southco, trustcorp, flores, meyer, ortiz).

% Type3 trades
trade_def(11, type3, southco, realprop, lynch, yates, zimmer).
trade_def(12, type3, trustcorp, realprop, king, yates, zimmer).
trade_def(13, type3, trustcorp, realprop, meyer, yates, zimmer).
trade_def(14, type3, trustcorp, realprop, ortiz, yates, zimmer).

% Valid trade at time T: companies own the required buildings
valid_trade(ID, T) :-
    trade_def(ID, type1, A, B, X, Y, _),
    owns(A, X, T), owns(B, Y, T).

valid_trade(ID, T) :-
    trade_def(ID, type2, A, B, X, Y, Z),
    owns(A, X, T), owns(B, Y, T), owns(B, Z, T), Y != Z.

valid_trade(ID, T) :-
    trade_def(ID, type3, A, B, X, Y, Z),
    owns(A, X, T), owns(B, Y, T), owns(B, Z, T), Y != Z.

% Choose at most one trade per time step (0 or 1)
{ occurs(T, ID) : valid_trade(ID, T) } 1 :- time(T), T < 2.

% Effects of trades on ownership at T+1
% For each trade ID, derive changed ownership

% Type1 swap: A gives X to B, B gives Y to A
changed(A, X, T) :- occurs(T, ID), trade_def(ID, type1, A, B, X, _, _).
changed(B, Y, T) :- occurs(T, ID), trade_def(ID, type1, A, B, _, Y, _).
owns(B, X, T+1) :- occurs(T, ID), trade_def(ID, type1, A, B, X, _, _), time(T), time(T+1).
owns(A, Y, T+1) :- occurs(T, ID), trade_def(ID, type1, A, B, _, Y, _), time(T), time(T+1).

% Type2: A gives X to B, B gives Y and Z to A
changed(A, X, T) :- occurs(T, ID), trade_def(ID, type2, A, B, X, _, _).
changed(B, Y, T) :- occurs(T, ID), trade_def(ID, type2, A, B, _, Y, _).
changed(B, Z, T) :- occurs(T, ID), trade_def(ID, type2, A, B, _, _, Z).
owns(B, X, T+1) :- occurs(T, ID), trade_def(ID, type2, A, B, X, _, _), time(T), time(T+1).
owns(A, Y, T+1) :- occurs(T, ID), trade_def(ID, type2, A, B, _, Y, _), time(T), time(T+1).
owns(A, Z, T+1) :- occurs(T, ID), trade_def(ID, type2, A, B, _, _, Z), time(T), time(T+1).

% Type3: A gives X to B, B gives Y and Z to A
changed(A, X, T) :- occurs(T, ID), trade_def(ID, type3, A, B, X, _, _).
changed(B, Y, T) :- occurs(T, ID), trade_def(ID, type3, A, B, _, Y, _).
changed(B, Z, T) :- occurs(T, ID), trade_def(ID, type3, A, B, _, _, Z).
owns(B, X, T+1) :- occurs(T, ID), trade_def(ID, type3, A, B, X, _, _), time(T), time(T+1).
owns(A, Y, T+1) :- occurs(T, ID), trade_def(ID, type3, A, B, _, Y, _), time(T), time(T+1).
owns(A, Z, T+1) :- occurs(T, ID), trade_def(ID, type3, A, B, _, _, Z), time(T), time(T+1).

% Final ownership at time 2
final_owns(C, B) :- owns(C, B, 2).

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
    occurs(T, ID),
    trade_def(ID, _, southco, trustcorp, _, _, _).
southco_trustcorp_trade :-
    occurs(T, ID),
    trade_def(ID, _, trustcorp, southco, _, _, _).

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