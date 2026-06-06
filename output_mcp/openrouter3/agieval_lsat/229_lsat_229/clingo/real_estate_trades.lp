% Real Estate Trading Problem

% ===== 1. DOMAIN DECLARATIONS =====
company(realprop). company(southco). company(trustcorp).
class(1). class(2). class(3).

% Buildings with their initial owners and classes
building(garza_tower). building(yates_house). building(zimmer_house).
building(flores_tower). building(lynch_building).
building(king_building). building(meyer_building). building(ortiz_building).

% Initial ownership facts
owns(realprop, garza_tower, 0). class_of(garza_tower, 1).
owns(realprop, yates_house, 0). class_of(yates_house, 3).
owns(realprop, zimmer_house, 0). class_of(zimmer_house, 3).

owns(southco, flores_tower, 0). class_of(flores_tower, 1).
owns(southco, lynch_building, 0). class_of(lynch_building, 2).

owns(trustcorp, king_building, 0). class_of(king_building, 2).
owns(trustcorp, meyer_building, 0). class_of(meyer_building, 2).
owns(trustcorp, ortiz_building, 0). class_of(ortiz_building, 2).

% Time horizon
time(0..10).

% ===== 2. TRADE GENERATION =====
% Trade type 1: Exchange one building for another of same class
{ trade_type1(C1, B1, C2, B2, T) } :- time(T), company(C1), company(C2), C1 != C2,
    building(B1), building(B2), class_of(B1, Cl), class_of(B2, Cl).

% Trade type 2: One class 1 building for two class 2 buildings
{ trade_type2(C1, B1, C2, B2a, B2b, T) } :- time(T), company(C1), company(C2), C1 != C2,
    building(B1), class_of(B1, 1),
    building(B2a), building(B2b), B2a != B2b,
    class_of(B2a, 2), class_of(B2b, 2).

% Trade type 3: One class 2 building for two class 3 buildings
{ trade_type3(C1, B1, C2, B3a, B3b, T) } :- time(T), company(C1), company(C2), C1 != C2,
    building(B1), class_of(B1, 2),
    building(B3a), building(B3b), B3a != B3b,
    class_of(B3a, 3), class_of(B3b, 3).

% ===== 3. OWNERSHIP DYNAMICS =====
% Ownership persists unless changed by a trade
owns(C, B, T+1) :- owns(C, B, T), time(T), time(T+1), not traded_away(C, B, T).

% A building is traded away if it's part of a trade at time T
traded_away(C, B, T) :- trade_type1(C, B, _, _, T).
traded_away(C, B, T) :- trade_type2(C, B, _, _, _, T).
traded_away(C, B, T) :- trade_type3(C, B, _, _, _, T).

% ===== 4. TRADE EFFECTS =====
% For trade type 1: C1 gives B1 to C2, C2 gives B2 to C1
owns(C2, B1, T+1) :- trade_type1(C1, B1, C2, B2, T), time(T), time(T+1).
owns(C1, B2, T+1) :- trade_type1(C1, B1, C2, B2, T), time(T), time(T+1).

% For trade type 2: C1 gives B1 (class 1) to C2, C2 gives B2a and B2b (class 2) to C1
owns(C2, B1, T+1) :- trade_type2(C1, B1, C2, B2a, B2b, T), time(T), time(T+1).
owns(C1, B2a, T+1) :- trade_type2(C1, B1, C2, B2a, B2b, T), time(T), time(T+1).
owns(C1, B2b, T+1) :- trade_type2(C1, B1, C2, B2a, B2b, T), time(T), time(T+1).

% For trade type 3: C1 gives B1 (class 2) to C2, C2 gives B3a and B3b (class 3) to C1
owns(C2, B1, T+1) :- trade_type3(C1, B1, C2, B3a, B3b, T), time(T), time(T+1).
owns(C1, B3a, T+1) :- trade_type3(C1, B1, C2, B3a, B3b, T), time(T), time(T+1).
owns(C1, B3b, T+1) :- trade_type3(C1, B1, C2, B3a, B3b, T), time(T), time(T+1).

% ===== 5. CONSTRAINTS =====
% Each building can only be owned by one company at any time
:- owns(C1, B, T), owns(C2, B, T), C1 != C2.

% No building can be traded away if it's not owned by the trading company
:- trade_type1(C1, B1, C2, B2, T), not owns(C1, B1, T).
:- trade_type2(C1, B1, C2, B2a, B2b, T), not owns(C1, B1, T).
:- trade_type3(C1, B1, C2, B3a, B3b, T), not owns(C1, B1, T).

% ===== 6. GOAL CONDITION =====
% Trustcorp owns no class 2 buildings at the final time
final_time(T) :- time(T), not time(T+1).
trustcorp_no_class2(T) :- final_time(T), 
    not (owns(trustcorp, B, T), class_of(B, 2)).

% ===== 7. EVALUATE ANSWER CHOICES =====
% (A) RealProp owns a class 1 building
realprop_has_class1(T) :- owns(realprop, B, T), class_of(B, 1).

% (B) Southco owns only class 2 buildings
southco_only_class2(T) :- 
    owns(southco, _, T),
    not (owns(southco, B, T), class_of(B, C), C != 2).

% (C) Southco has made at least one trade with Trustcorp
southco_trustcorp_trade(T) :- 
    trade_type1(southco, _, trustcorp, _, T);
    trade_type1(trustcorp, _, southco, _, T);
    trade_type2(southco, _, trustcorp, _, _, T);
    trade_type2(trustcorp, _, southco, _, _, T);
    trade_type3(southco, _, trustcorp, _, _, T);
    trade_type3(trustcorp, _, southco, _, _, T).

% (D) Trustcorp owns the Garza Tower
trustcorp_has_garza(T) :- owns(trustcorp, garza_tower, T).

% (E) Trustcorp owns the Zimmer House
trustcorp_has_zimmer(T) :- owns(trustcorp, zimmer_house, T).

% ===== 8. FINAL ANSWER MAPPING =====
% We need to find which statement MUST be true when Trustcorp has no class 2 buildings
% This means: In ALL models where trustcorp_no_class2 holds, the statement must also hold

% For "must be true", we need to check if the statement is true in ALL valid final states
% We'll derive the answer by checking if the statement is entailed by the goal condition

% Option (A): RealProp owns a class 1 building
option(a) :- trustcorp_no_class2(_), realprop_has_class1(_).

% Option (B): Southco owns only class 2 buildings  
option(b) :- trustcorp_no_class2(_), southco_only_class2(_).

% Option (C): Southco has made at least one trade with Trustcorp
option(c) :- trustcorp_no_class2(_), southco_trustcorp_trade(_).

% Option (D): Trustcorp owns the Garza Tower
option(d) :- trustcorp_no_class2(_), trustcorp_has_garza(_).

% Option (E): Trustcorp owns the Zimmer House
option(e) :- trustcorp_no_class2(_), trustcorp_has_zimmer(_).

% Show the options
#show option/1.