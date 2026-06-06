% Base facts about companies and their buildings
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

class(garza_tower, 1).
class(yates_house, 3).
class(zimmer_house, 3).
class(flores_tower, 1).
class(lynch_building, 2).
class(king_building, 2).
class(meyer_building, 2).
class(ortiz_building, 2).

% Initial ownership
owns(realprop, garza_tower).
owns(realprop, yates_house).
owns(realprop, zimmer_house).
owns(southco, flores_tower).
owns(southco, lynch_building).
owns(trustcorp, king_building).
owns(trustcorp, meyer_building).
owns(trustcorp, ortiz_building).

% Time horizon for trades
time(0..5).

% State at time 0
building_at(B, C, 0) :- owns(C, B).

% Choice rule: At each time step, a company can perform a trade
{ trade(C1, C2, B1, B2, T) : 
    company(C1), company(C2), 
    building(B1), building(B2), 
    class(B1, Cl), class(B2, Cl), 
    T > 0, T <= 5 } 1 :- 
    time(T), company(C1), company(C2), C1 != C2.

{ trade_class1_for_two_class2(C1, C2, B1, T) : 
    company(C1), company(C2), 
    building(B1), class(B1, 1), 
    T > 0, T <= 5 } 1 :- 
    time(T), company(C1), company(C2), C1 != C2.

{ trade_class2_for_two_class3(C1, C2, B1, T) : 
    company(C1), company(C2), 
    building(B1), class(B1, 2), 
    T > 0, T <= 5 } 1 :- 
    time(T), company(C1), company(C2), C1 != C2.

% Preconditions for trades
% Type 1: Trade one building for one other building of the same class
:- trade(C1, C2, B1, B2, T), 
   not building_at(B1, C1, T-1),
   not building_at(B2, C2, T-1).

% Type 2: Trade one class 1 building for two class 2 buildings
:- trade_class1_for_two_class2(C1, C2, B1, T),
   not building_at(B1, C1, T-1).

% Type 3: Trade one class 2 building for two class 3 buildings
:- trade_class2_for_two_class3(C1, C2, B1, T),
   not building_at(B1, C1, T-1).

% Effects of trades
% Type 1: Trade one building for one other building of the same class
building_at(B1, C1, T) :- 
    trade(C1, C2, B1, B2, T),
    building_at(B1, C1, T-1),
    building_at(B2, C2, T-1).

building_at(B2, C2, T) :- 
    trade(C1, C2, B1, B2, T),
    building_at(B1, C1, T-1),
    building_at(B2, C2, T-1).

% Type 2: Trade one class 1 building for two class 2 buildings
% Ensure the two class 2 buildings are distinct and not already owned by C2
{ building_at(B2_1, C2, T) : 
    building(B2_1), class(B2_1, 2) } 2 :- 
    trade_class1_for_two_class2(C1, C2, B1, T),
    building_at(B1, C1, T-1).

% Type 3: Trade one class 2 building for two class 3 buildings
{ building_at(B3_1, C2, T) : 
    building(B3_1), class(B3_1, 3) } 2 :- 
    trade_class2_for_two_class3(C1, C2, B1, T),
    building_at(B1, C1, T-1).

% Frame axioms: Buildings not involved in a trade remain with their owner
building_at(B, C, T) :- 
    building_at(B, C, T-1),
    time(T),
    not building_lost(B, C, T).

building_lost(B, C, T) :- 
    trade(C, C2, B, _, T),
    company(C2),
    T > 0.

building_lost(B, C, T) :- 
    trade_class1_for_two_class2(C, C2, B, T),
    company(C2),
    T > 0.

building_lost(B, C, T) :- 
    trade_class2_for_two_class3(C, C2, B, T),
    company(C2),
    T > 0.

% Define the final state at time 5
final_ownership(C, B) :- building_at(B, C, 5).

% --- Evaluate the multiple-choice options ---
% (A) The buildings owned by RealProp are the Flores Tower and the Garza Tower.
option(a) :- 
    final_ownership(realprop, flores_tower),
    final_ownership(realprop, garza_tower),
    not final_ownership(realprop, yates_house),
    not final_ownership(realprop, zimmer_house).

% (B) The buildings owned by Southco are the Flores Tower and the Meyer Building.
option(b) :- 
    final_ownership(southco, flores_tower),
    final_ownership(southco, meyer_building),
    not final_ownership(southco, lynch_building).

% (C) The buildings owned by Southco are the Garza Tower and the Lynch Building.
option(c) :- 
    final_ownership(southco, garza_tower),
    final_ownership(southco, lynch_building),
    not final_ownership(southco, flores_tower).

% (D) The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
option(d) :- 
    final_ownership(trustcorp, flores_tower),
    final_ownership(trustcorp, ortiz_building),
    not final_ownership(trustcorp, king_building),
    not final_ownership(trustcorp, meyer_building).

% (E) The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
option(e) :- 
    final_ownership(trustcorp, garza_tower),
    final_ownership(trustcorp, meyer_building),
    not final_ownership(trustcorp, king_building),
    not final_ownership(trustcorp, ortiz_building).

#show option/1.
#show final_ownership/2.