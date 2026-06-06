% Define buildings and their classes
building(garza_tower). building(yates_house). building(zimmer_house).
building(flores_tower). building(lynch_building).
building(king_building). building(meyer_building). building(ortiz_building).

class(garza_tower, 1). class(yates_house, 3). class(zimmer_house, 3).
class(flores_tower, 1). class(lynch_building, 2).
class(king_building, 2). class(meyer_building, 2). class(ortiz_building, 2).

% Define initial ownership
owns(realprop, garza_tower). owns(realprop, yates_house). owns(realprop, zimmer_house).
owns(southco, flores_tower). owns(southco, lynch_building).
owns(trustcorp, king_building). owns(trustcorp, meyer_building). owns(trustcorp, ortiz_building).

% Define the three trade types
% Type 1: One building for one building of the same class
% Type 2: One class 1 building for two class 2 buildings
% Type 3: One class 2 building for two class 3 buildings

% We need to check each option to see if it can be achieved by exactly one trade

% Helper: Check if a set of buildings is owned by a company in an option
% We'll define the ownership for each option

% Option A ownership
owns_a(realprop, flores_tower). owns_a(realprop, garza_tower).
owns_a(southco, lynch_building). owns_a(southco, yates_house). owns_a(southco, zimmer_house).
owns_a(trustcorp, king_building). owns_a(trustcorp, meyer_building). owns_a(trustcorp, ortiz_building).

% Option B ownership
owns_b(realprop, garza_tower). owns_b(realprop, king_building). owns_b(realprop, ortiz_building).
owns_b(southco, flores_tower). owns_b(southco, lynch_building).
owns_b(trustcorp, meyer_building). owns_b(trustcorp, yates_house). owns_b(trustcorp, zimmer_house).

% Option C ownership
owns_c(realprop, garza_tower). owns_c(realprop, lynch_building).
owns_c(southco, flores_tower). owns_c(southco, yates_house). owns_c(southco, zimmer_house).
owns_c(trustcorp, king_building). owns_c(trustcorp, meyer_building). owns_c(trustcorp, ortiz_building).

% Option D ownership
owns_d(realprop, garza_tower). owns_d(realprop, meyer_building). owns_d(realprop, yates_house).
owns_d(southco, flores_tower). owns_d(southco, lynch_building).
owns_d(trustcorp, king_building). owns_d(trustcorp, ortiz_building). owns_d(trustcorp, zimmer_house).

% Option E ownership
owns_e(realprop, garza_tower). owns_e(realprop, yates_house). owns_e(realprop, zimmer_house).
owns_e(southco, lynch_building). owns_e(southco, ortiz_building).
owns_e(trustcorp, flores_tower). owns_e(trustcorp, king_building). owns_e(trustcorp, meyer_building).

% Check if an option is achievable by exactly one trade
% We need to find what changed from initial to final ownership

% For each option, find buildings that changed ownership
changed_a(Building) :- building(Building), owns(Company, Building), not owns_a(Company, Building).
changed_a(Building) :- building(Building), owns_a(Company, Building), not owns(Company, Building).

changed_b(Building) :- building(Building), owns(Company, Building), not owns_b(Company, Building).
changed_b(Building) :- building(Building), owns_b(Company, Building), not owns(Company, Building).

changed_c(Building) :- building(Building), owns(Company, Building), not owns_c(Company, Building).
changed_c(Building) :- building(Building), owns_c(Company, Building), not owns(Company, Building).

changed_d(Building) :- building(Building), owns(Company, Building), not owns_d(Company, Building).
changed_d(Building) :- building(Building), owns_d(Company, Building), not owns(Company, Building).

changed_e(Building) :- building(Building), owns(Company, Building), not owns_e(Company, Building).
changed_e(Building) :- building(Building), owns_e(Company, Building), not owns(Company, Building).

% Count changed buildings for each option
count_changed_a(N) :- N = #count{B : changed_a(B)}.
count_changed_b(N) :- N = #count{B : changed_b(B)}.
count_changed_c(N) :- N = #count{B : changed_c(B)}.
count_changed_d(N) :- N = #count{B : changed_d(B)}.
count_changed_e(N) :- N = #count{B : changed_e(B)}.

% Check if the changes form a valid trade
% For a valid trade, we need to check if the changed buildings can be grouped into one of the three trade types

% Helper: For each option, check if changes match a trade type
% Trade type 1: One building for one building of same class
% Trade type 2: One class 1 for two class 2
% Trade type 3: One class 2 for two class 3

% For option A
% Let's see what changed in option A
% From initial to A: RealProp loses Yates House and Zimmer House, gains Flores Tower
% Southco loses Flores Tower, gains Yates House and Zimmer House
% Trustcorp unchanged

% Check if this matches a trade type
% RealProp gives two class 3 buildings, gets one class 1 building
% This matches trade type 3 (one class 2 for two class 3) but reversed?
% Actually trade type 3 is: one class 2 building for two class 3 buildings
% Here RealProp gives two class 3 and gets one class 1 - not matching any type

% Let me check each option systematically

% Option A: RealProp gives Yates House (3) and Zimmer House (3), gets Flores Tower (1)
% This is two class 3 for one class 1 - not a valid trade type

% Option B: RealProp gives Yates House (3) and Zimmer House (3), gets King Building (2) and Ortiz Building (2)
% This is two class 3 for two class 2 - not a valid trade type

% Option C: RealProp gives Yates House (3) and Zimmer House (3), gets Lynch Building (2)
% This is two class 3 for one class 2 - matches trade type 3 (one class 2 for two class 3)

% Option D: RealProp gives Yates House (3) and Zimmer House (3), gets Meyer Building (2)
% This is two class 3 for one class 2 - matches trade type 3

% Option E: Southco gives Flores Tower (1), gets Ortiz Building (2)
% This is one class 1 for one class 2 - not a valid trade type

% Let me verify option C more carefully
% Initial: RealProp has Garza(1), Yates(3), Zimmer(3)
% Final C: RealProp has Garza(1), Lynch(2)
% So RealProp gave Yates(3) and Zimmer(3), got Lynch(2)
% This is exactly trade type 3: one class 2 for two class 3

% Check if Southco's changes match
% Initial: Southco has Flores(1), Lynch(2)
% Final C: Southco has Flores(1), Yates(3), Zimmer(3)
% So Southco gave Lynch(2), got Yates(3) and Zimmer(3)
% This is also trade type 3: one class 2 for two class 3

% This is a valid trade between RealProp and Southco

% Now let me verify option D
% Initial: RealProp has Garza(1), Yates(3), Zimmer(3)
% Final D: RealProp has Garza(1), Meyer(2), Yates(3)
% So RealProp gave Zimmer(3), got Meyer(2)
% This is one class 3 for one class 2 - not a valid trade type

% Option D doesn't match any trade type

% So option C is valid

% Let me create the final answer
option(c) :- count_changed_c(4).  % 4 buildings changed in option C

#show option/1.