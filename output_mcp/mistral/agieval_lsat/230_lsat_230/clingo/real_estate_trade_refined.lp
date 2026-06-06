#const max_time = 5.

% Companies
company(realprop).
company(southco).
company(trustcorp).

% Buildings and their classes
% Format: building(Name, Class)
building(garza_tower, 1).
building(yates_house, 3).
building(zimmer_house, 3).
building(flores_tower, 1).
building(lynch_building, 2).
building(king_building, 2).
building(meyer_building, 2).
building(ortiz_building, 2).

% Initial ownership
% Format: owns(Company, Building)
owns(realprop, garza_tower).
owns(realprop, yates_house).
owns(realprop, zimmer_house).
owns(southco, flores_tower).
owns(southco, lynch_building).
owns(trustcorp, king_building).
owns(trustcorp, meyer_building).
owns(trustcorp, ortiz_building).

% Time steps
time(0..max_time).

% State predicates:
% - current_owner(Building, Company, Time)

% Initialize ownership at time 0
current_owner(Building, Company, 0) :- owns(Company, Building).

% Choice rule: what trades can happen at each time step
% A building can change owner at each time step, subject to constraints
{ current_owner(Building, Company, T+1) : company(Company) } 1 :-
    building(Building),
    time(T),
    T < max_time.

% Frame axiom: if no trade affects a building, it stays with the same owner
current_owner(Building, Company, T+1) :-
    current_owner(Building, Company, T),
    building(Building),
    company(Company),
    time(T),
    T < max_time.

% Constraints on trades:

% Trade type 2: Trade one class 1 building for two class 2 buildings
% This means a company can gain class 2 buildings only if it gives up a class 1 building
% We'll model this by ensuring that the total number of class 2 buildings owned by a company
% can only increase if it gives up a class 1 building

% Trade type 3: Trade one class 2 building for two class 3 buildings
% Similarly, a company can gain class 3 buildings only if it gives up a class 2 building

% To simplify, we'll model the final state and check invariants

% Count buildings of each class owned by each company at final time
count_class(Company, Class, T) :-
    company(Company),
    building_class(Building, Class),
    current_owner(Building, Company, T),
    time(T).

building_class(Building, Class) :- building(Building, Class).

% Total number of buildings of each class (constant)
total_class1(3).
total_class2(5).
total_class3(3).

% Total number of buildings owned by each company (constant)
total_buildings(3).

% Each company must own exactly 3 buildings at any time
:- company(C), time(T), #count{ B : current_owner(B, C, T) } != total_buildings.

% Check each option for consistency with trade rules

% Option A: RealProp owns Lynch Building, Meyer Building, and Ortiz Building (all class 2)
% This means RealProp owns 3 class 2 buildings
% To achieve this, RealProp must have traded away its class 1 and class 3 buildings
% and acquired 3 class 2 buildings. This is possible via trade type 2 (class 1 -> 2 class 2)
% and trade type 3 (class 2 -> 2 class 3), but RealProp starts with 1 class 1 and 2 class 3.
% It can trade its class 1 for 2 class 2, then trade 1 class 2 for 2 class 3, but it's complex.
% However, the main issue is that RealProp cannot end up with 3 class 2 buildings
% because it starts with 1 class 1 and 2 class 3, and the trade rules do not allow
% converting class 3 to class 2 directly.
% So Option A may be impossible.

% Option B: Southco owns Garza Tower (class 1) and Meyer Building (class 2)
% Southco starts with Flores Tower (class 1) and Lynch Building (class 2)
% It can trade its class 1 (Flores Tower) for 2 class 2 buildings, then trade one of its class 2
% for 2 class 3 buildings, but it's not clear if it can end up with Garza Tower (class 1).
% However, Garza Tower is initially owned by RealProp, so Southco would need to acquire it
% via trade type 1 (same class trade). This is possible if RealProp trades it for another class 1 building.
% So Option B may be possible.

% Option C: Southco owns King Building, Meyer Building, and Ortiz Building (all class 2)
% Southco starts with 1 class 1 and 1 class 2. To end up with 3 class 2 buildings,
% it can trade its class 1 for 2 class 2 buildings, resulting in 3 class 2 buildings.
% So Option C is possible.

% Option D: Trustcorp owns Flores Tower (class 1) and Yates House (class 3)
% Trustcorp starts with 3 class 2 buildings. To end up with a class 1 and a class 3 building,
% it would need to trade class 2 buildings for class 1 and class 3, but the trade rules
% only allow trading class 1 for class 2, and class 2 for class 3.
% So Trustcorp cannot end up with a class 1 building unless it receives one via trade type 1
% (same class trade), but it starts with class 2 buildings only.
% So Option D may be impossible.

% Option E: Trustcorp owns Garza Tower (class 1) and Lynch Building (class 2)
% Trustcorp starts with 3 class 2 buildings. To end up with a class 1 building,
% it would need to receive Garza Tower via trade type 1 (same class trade), but Garza Tower
% is class 1, and Trustcorp only owns class 2 buildings initially. So it cannot acquire
% a class 1 building unless another company trades it for a class 2 building, which is possible
% via trade type 1. So Option E may be possible.

% To determine which option cannot be true, we'll define predicates for each option
% and check if they can be satisfied under the constraints.

% Option A: RealProp owns Lynch, Meyer, Ortiz (all class 2)
option_a :-
    current_owner(lynch_building, realprop, max_time),
    current_owner(meyer_building, realprop, max_time),
    current_owner(ortiz_building, realprop, max_time).

% Option B: Southco owns Garza Tower and Meyer Building
option_b :-
    current_owner(garza_tower, southco, max_time),
    current_owner(meyer_building, southco, max_time).

% Option C: Southco owns King, Meyer, Ortiz (all class 2)
option_c :-
    current_owner(king_building, southco, max_time),
    current_owner(meyer_building, southco, max_time),
    current_owner(ortiz_building, southco, max_time).

% Option D: Trustcorp owns Flores Tower and Yates House
option_d :-
    current_owner(flores_tower, trustcorp, max_time),
    current_owner(yates_house, trustcorp, max_time).

% Option E: Trustcorp owns Garza Tower and Lynch Building
option_e :-
    current_owner(garza_tower, trustcorp, max_time),
    current_owner(lynch_building, trustcorp, max_time).

% Map the correct answer to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.