% Base facts: companies and their buildings
company(realprop).
company(southco).
company(trustcorp).

building(garza_tower).
building(yates_house).
building(zimmer_house).
building(flores_tower).
building(lynch_building).
building(king_building).
building(meyer_building).
building(ortiz_building).

% Define classes as facts
class(1).
class(2).
class(3).

% Building classes
class(garza_tower, 1).
class(yates_house, 3).
class(zimmer_house, 3).
class(flores_tower, 1).
class(lynch_building, 2).
class(king_building, 2).
class(meyer_building, 2).
class(ortiz_building, 2).

% Initial ownership
owner(garza_tower, realprop, 0).
owner(yates_house, realprop, 0).
owner(zimmer_house, realprop, 0).
owner(flores_tower, southco, 0).
owner(lynch_building, southco, 0).
owner(king_building, trustcorp, 0).
owner(meyer_building, trustcorp, 0).
owner(ortiz_building, trustcorp, 0).

% Time steps
time(0..5).

% Class count at time 0
class_count(Company, Class, Count, 0) :-
    company(Company),
    class(Class),
    Count = #count { B : owner(B, Company, 0), class(B, Class) }.

% Trade types:
% 1. Trade one building for one building of the same class
% 2. Trade one class 1 building for two class 2 buildings
% 3. Trade one class 2 building for two class 3 buildings

% Possible trade partners
trade_partner(Company1, Company2) :-
    company(Company1),
    company(Company2),
    Company1 != Company2.

% Trade type 1: same class
{ trade(Company1, Building1, Company2, Building2, 1, T) :
    owner(Building1, Company1, T-1),
    owner(Building2, Company2, T-1),
    class(Building1, Class),
    class(Building2, Class),
    T > 0,
    time(T) 
} :-
    trade_partner(Company1, Company2),
    class(Class),
    time(T).

% Trade type 2: class 1 for two class 2
{ trade(Company1, Building1, Company2, Building2_1, 2, T) :
    owner(Building1, Company1, T-1),
    class(Building1, 1),
    owner(Building2_1, Company2, T-1),
    class(Building2_1, 2),
    owner(Building2_2, Company2, T-1),
    class(Building2_2, 2),
    Building2_1 != Building2_2,
    T > 0,
    time(T) 
} :-
    trade_partner(Company1, Company2),
    time(T).

% Trade type 3: class 2 for two class 3
{ trade(Company1, Building1, Company2, Building2_1, 3, T) :
    owner(Building1, Company1, T-1),
    class(Building1, 2),
    owner(Building2_1, Company2, T-1),
    class(Building2_1, 3),
    owner(Building2_2, Company2, T-1),
    class(Building2_2, 3),
    Building2_1 != Building2_2,
    T > 0,
    time(T) 
} :-
    trade_partner(Company1, Company2),
    time(T).

% Apply trades to update ownership
% If a building is traded, its ownership changes
owner(Building, Company2, T) :-
    trade(Company1, Building, Company2, _, _, T),
    time(T).

% If a building is not traded, its ownership remains the same
owner(Building, Company, T) :-
    owner(Building, Company, T-1),
    time(T),
    T > 0,
    not owner(Building, _, T).

% Class count update
class_count(Company, Class, Count, T) :-
    company(Company),
    class(Class),
    Count = #count { B : owner(B, Company, T), class(B, Class) },
    time(T).

% Constraint: Trustcorp owns no class 2 buildings after some trades
:- class_count(trustcorp, 2, Count, T),
   Count > 0,
   time(T),
   T > 0.

% Answer choices
% (A) RealProp owns a class 1 building after the trades
answer(a) :-
    class_count(realprop, 1, Count, T),
    Count > 0,
    time(T),
    T > 0.

% (B) Southco owns only class 2 buildings after the trades
answer(b) :-
    class_count(southco, 1, Count1, T),
    class_count(southco, 3, Count3, T),
    Count1 = 0,
    Count3 = 0,
    class_count(southco, 2, Count2, T),
    Count2 > 0,
    time(T),
    T > 0.

% (C) Southco has made at least one trade with Trustcorp
answer(c) :-
    trade(southco, _, trustcorp, _, _, T),
    time(T),
    T > 0.

answer(c) :-
    trade(trustcorp, _, southco, _, _, T),
    time(T),
    T > 0.

% (D) Trustcorp owns the Garza Tower after the trades
answer(d) :-
    owner(garza_tower, trustcorp, T),
    time(T),
    T > 0.

% (E) Trustcorp owns the Zimmer House after the trades
answer(e) :-
    owner(zimmer_house, trustcorp, T),
    time(T),
    T > 0.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.