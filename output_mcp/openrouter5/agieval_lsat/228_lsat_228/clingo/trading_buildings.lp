%% Problem: Three real estate companies trading buildings
%% We need to determine what MUST be true if RealProp ends up owning only class 2 buildings.

%% --- Domain Definitions ---

%% Companies
company(realprop; southco; trustcorp).

%% Buildings with their classes
building(garza_tower; yates_house; zimmer_house; flores_tower; lynch_building; king_building; meyer_building; ortiz_building).

%% Building classes
class(1;2;3).

%% Initial ownership
% RealProp: Garza Tower (class 1), Yates House (class 3), Zimmer House (class 3)
% Southco: Flores Tower (class 1), Lynch Building (class 2)
% Trustcorp: King Building (class 2), Meyer Building (class 2), Ortiz Building (class 2)

building_class(garza_tower, 1).
building_class(yates_house, 3).
building_class(zimmer_house, 3).
building_class(flores_tower, 1).
building_class(lynch_building, 2).
building_class(king_building, 2).
building_class(meyer_building, 2).
building_class(ortiz_building, 2).

%% Initial ownership
init_owner(garza_tower, realprop).
init_owner(yates_house, realprop).
init_owner(zimmer_house, realprop).
init_owner(flores_tower, southco).
init_owner(lynch_building, southco).
init_owner(king_building, trustcorp).
init_owner(meyer_building, trustcorp).
init_owner(ortiz_building, trustcorp).

%% --- Trading Rules ---
%% Each trade must be exactly one of:
%% 1. One building for one other building of the same class
%% 2. One class 1 building for two class 2 buildings
%% 3. One class 2 building for two class 3 buildings

%% We model trades as sequences. Since we only care about the final state
%% (RealProp owns only class 2 buildings), we can model the final ownership
%% directly with constraints on what trades are possible.

%% The key insight: trades are exchanges. The total set of buildings is fixed.
%% We need to find all possible final ownership configurations reachable via
%% valid trades, and see what MUST be true in all such configurations where
%% RealProp owns only class 2 buildings.

%% Let's model the final ownership as a relation: owns(Company, Building)
%% We start with initial ownership and allow trades.

%% We need to model trades. Let's think about what trades can do.
%% A trade exchanges buildings between companies. The total multiset of buildings
%% by class is preserved (since trades only exchange same-class or equivalent-value bundles).

%% Actually, let's think more carefully:
%% Trade type 1: 1-for-1 same class. Net effect: two buildings of same class swap owners.
%% Trade type 2: 1 class 1 for 2 class 2. Net effect: one company gives 1 class 1, gets 2 class 2; other gives 2 class 2, gets 1 class 1.
%% Trade type 3: 1 class 2 for 2 class 3. Net effect: one company gives 1 class 2, gets 2 class 3; other gives 2 class 3, gets 1 class 2.

%% Since we only care about the final state and what MUST be true,
%% we can model the final ownership directly with constraints that
%% the final state must be reachable via valid trades.

%% Let's think about what constraints the trades impose on the final state.

%% Key invariant: The total number of buildings of each class is conserved.
%% Class 1: Garza Tower, Flores Tower = 2 buildings
%% Class 2: Lynch, King, Meyer, Ortiz = 4 buildings
%% Class 3: Yates House, Zimmer House = 2 buildings

%% Total: 8 buildings.

%% Trade type 2: exchanging 1 class 1 for 2 class 2.
%% This changes the class distribution among companies but preserves totals.

%% Let's model the final ownership.
{ owns(C, B) } :- company(C), building(B).

%% Each building is owned by exactly one company in the final state.
:- building(B), not { owns(C, B) : company(C) } 1.
:- building(B), { owns(C, B) : company(C) } > 1.

%% The final state must be reachable from initial state via valid trades.
%% We can model this by saying there exists a sequence of trades.
%% But that's complex. Instead, let's think about what constraints
%% the trade rules impose on the final multiset of buildings per company.

%% Actually, let's model trades explicitly with a bounded number of trades.

%% Maximum number of trades (we can bound this reasonably)
num_trades(0..6).

%% Each trade involves two parties and some buildings
%% Trade type 1: trade(B1, B2, T) means B1 and B2 (same class) are swapped between their owners at time T
%% Trade type 2: trade2(B1, B2a, B2b, T) where B1 is class 1, B2a,B2b are class 2
%% Trade type 3: trade3(B2, B3a, B3b, T) where B2 is class 2, B3a,B3b are class 3

%% State at time T: owns_at(C, B, T)
time(0..6).

%% Initial state at time 0
owns_at(C, B, 0) :- init_owner(B, C).

%% Each building is owned by exactly one company at each time
:- time(T), building(B), not { owns_at(C, B, T) : company(C) } 1.
:- time(T), building(B), { owns_at(C, B, T) : company(C) } > 1.

%% Frame axiom: ownership persists unless changed by a trade
owns_at(C, B, T+1) :- owns_at(C, B, T), time(T), time(T+1), not changed(B, T).

%% changed(B, T) means building B changes owner at time T
changed(B, T) :- trade1(B, _, T).
changed(B, T) :- trade1(_, B, T).
changed(B, T) :- trade2(B, _, _, T).
changed(B, T) :- trade2(_, B, _, T).
changed(B, T) :- trade2(_, _, B, T).
changed(B, T) :- trade3(B, _, _, T).
changed(B, T) :- trade3(_, B, _, T).
changed(B, T) :- trade3(_, _, B, T).

%% At most one trade per time step
:- time(T), 
   { trade1(_, _, T); trade2(_, _, _, T); trade3(_, _, _, T) } > 1.

%% Trade type 1: swap two buildings of the same class
{ trade1(B1, B2, T) : building(B1), building(B2), B1 < B2, building_class(B1, C), building_class(B2, C) } :- time(T).

%% Effect of trade type 1
owns_at(C2, B1, T+1) :- trade1(B1, B2, T), owns_at(C1, B1, T), owns_at(C2, B2, T).
owns_at(C1, B2, T+1) :- trade1(B1, B2, T), owns_at(C1, B1, T), owns_at(C2, B2, T).

%% Trade type 2: one class 1 for two class 2
{ trade2(B1, B2a, B2b, T) : 
    building_class(B1, 1), 
    building_class(B2a, 2), building_class(B2b, 2), 
    B2a < B2b } :- time(T).

%% Effect of trade type 2: company that had B1 (class 1) gets B2a and B2b (class 2)
%% company that had B2a and B2b gets B1
owns_at(C_giver, B2a, T+1) :- trade2(B1, B2a, B2b, T), owns_at(C_giver, B1, T), owns_at(C_receiver, B2a, T), owns_at(C_receiver, B2b, T).
owns_at(C_giver, B2b, T+1) :- trade2(B1, B2a, B2b, T), owns_at(C_giver, B1, T), owns_at(C_receiver, B2a, T), owns_at(C_receiver, B2b, T).
owns_at(C_receiver, B1, T+1) :- trade2(B1, B2a, B2b, T), owns_at(C_giver, B1, T), owns_at(C_receiver, B2a, T), owns_at(C_receiver, B2b, T).

%% Trade type 3: one class 2 for two class 3
{ trade3(B2, B3a, B3b, T) : 
    building_class(B2, 2), 
    building_class(B3a, 3), building_class(B3b, 3), 
    B3a < B3b } :- time(T).

%% Effect of trade type 3
owns_at(C_giver, B3a, T+1) :- trade3(B2, B3a, B3b, T), owns_at(C_giver, B2, T), owns_at(C_receiver, B3a, T), owns_at(C_receiver, B3b, T).
owns_at(C_giver, B3b, T+1) :- trade3(B2, B3a, B3b, T), owns_at(C_giver, B2, T), owns_at(C_receiver, B3a, T), owns_at(C_receiver, B3b, T).
owns_at(C_receiver, B2, T+1) :- trade3(B2, B3a, B3b, T), owns_at(C_giver, B2, T), owns_at(C_receiver, B3a, T), owns_at(C_receiver, B3b, T).

%% For trade type 2 and 3, the two buildings given by the receiver must be owned by the same company
:- trade2(B1, B2a, B2b, T), owns_at(C1, B2a, T), owns_at(C2, B2b, T), C1 != C2.
:- trade3(B2, B3a, B3b, T), owns_at(C1, B3a, T), owns_at(C2, B3b, T), C1 != C2.

%% The giver and receiver must be different companies
:- trade1(B1, B2, T), owns_at(C1, B1, T), owns_at(C2, B2, T), C1 = C2.
:- trade2(B1, B2a, B2b, T), owns_at(C_giver, B1, T), owns_at(C_receiver, B2a, T), C_giver = C_receiver.
:- trade3(B2, B3a, B3b, T), owns_at(C_giver, B2, T), owns_at(C_receiver, B3a, T), C_giver = C_receiver.

%% Final state: RealProp owns only class 2 buildings
%% RealProp's buildings at the final time must all be class 2
:- time(T), T = 6, owns_at(realprop, B, T), building_class(B, C), C != 2.

%% RealProp must own at least one building (or can it own zero? "owns only class 2 buildings" - could be zero)
%% Let's not force RealProp to own any particular number.

%% Also, RealProp must own only class 2 - meaning no class 1 or class 3.
%% Already enforced above.

%% Now, let's check what MUST be true in ALL such scenarios.
%% We'll use a trick: for each option, check if it's true in ALL models.
%% If an option is false in some model, it's not "must be true".

%% Let's first find all possible final states and then check.

%% To determine what MUST be true, we can use the following approach:
%% For each option, check if there exists a model where the option is false.
%% If no such model exists, the option must be true.

%% Let's define what each option means:

%% (A) Trustcorp owns a class 1 building.
trustcorp_owns_class1 :- owns_at(trustcorp, B, 6), building_class(B, 1).

%% (B) Trustcorp owns the Meyer Building.
trustcorp_owns_meyer :- owns_at(trustcorp, meyer_building, 6).

%% (C) Southco owns a class 2 building.
southco_owns_class2 :- owns_at(southco, B, 6), building_class(B, 2).

%% (D) Southco owns both of the class 3 buildings.
southco_owns_both_class3 :- owns_at(southco, B1, 6), building_class(B1, 3), 
                            owns_at(southco, B2, 6), building_class(B2, 3), B1 != B2,
                            B1 = yates_house, B2 = zimmer_house.

%% (E) Southco owns the Flores Tower.
southco_owns_flores :- owns_at(southco, flores_tower, 6).

%% We want to find if there's a model where each option is false.
%% If option X is false in some model, then X is NOT "must be true".

%% Let's use a different approach: enumerate all models and check.

%% First, let's just find all answer sets and see what's common.

#show owns_at/3.
#show trade1/3.
#show trade2/4.
#show trade3/4.