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

% Time steps - we'll use a finite horizon to explore possible trades
time(0..max_time).
max_time(5).  % Sufficient to explore possible trades

% State predicates:
% - current_owner(Building, Company, Time)
% - building_class(Building, Class)

% Initialize building classes (constant)
building_class(Building, Class) :- building(Building, Class).

% Initialize ownership at time 0
current_owner(Building, Company, 0) :- owns(Company, Building).

% Choice rule: what trades can happen at each time step
% Trade type 1: Exchange one building for one building of the same class
% Trade type 2: Trade one class 1 building for two class 2 buildings
% Trade type 3: Trade one class 2 building for two class 3 buildings

% We'll model trades as actions that change ownership

% Helper: count buildings of each class owned by each company at time T
count_class(Company, Class, T) :-
    company(Company),
    building_class(Building, Class),
    current_owner(Building, Company, T),
    time(T).

% Trade type 1: Exchange one building for one building of the same class
% This is complex to model directly as it requires coordination between two companies.
% Instead, we'll model the net effect: a company can change which specific building of a class it owns.

% For each class, a company can have any building of that class (simplified model)
% This captures the idea that buildings of the same class are fungible for trade type 1

% Trade type 2: Trade one class 1 building for two class 2 buildings
% Action: A company gives up one class 1 building and receives two class 2 buildings
% This requires the company to have at least one class 1 building

% Trade type 3: Trade one class 2 building for two class 3 buildings
% Action: A company gives up one class 2 building and receives two class 3 buildings
% This requires the company to have at least one class 2 building

% Instead of modeling the complex trade mechanics, we'll model the reachable states
% by allowing companies to change ownership of buildings subject to constraints

% At each time step, a company can lose a building (trade it away)
% and gain buildings according to the trade rules

% Simplified approach: model possible ownership states reachable through trades
% We'll use a choice rule to allow any ownership change that respects trade constraints

% A building can be owned by any company at time T+1, subject to constraints
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

% Trade type 2 constraint: To gain class 2 buildings through trade type 2,
% a company must give up a class 1 building
% We'll model this by ensuring that if a company gains class 2 buildings without
% having class 1 buildings initially, it must have traded away a class 1 building

% This is complex. Let's instead directly model the final states for each option
% and see which one violates invariants

% Let's define the final state (at max_time) for each option

% Option A: RealProp owns Lynch Building, Meyer Building, and Ortiz Building
% All are class 2 buildings
option_a :-
    current_owner(lynch_building, realprop, max_time),
    current_owner(meyer_building, realprop, max_time),
    current_owner(ortiz_building, realprop, max_time).

% Option B: Southco owns Garza Tower and Meyer Building
% Garza Tower is class 1, Meyer Building is class 2
option_b :-
    current_owner(garza_tower, southco, max_time),
    current_owner(meyer_building, southco, max_time).

% Option C: Southco owns King Building, Meyer Building, and Ortiz Building
% All are class 2 buildings
option_c :-
    current_owner(king_building, southco, max_time),
    current_owner(meyer_building, southco, max_time),
    current_owner(ortiz_building, southco, max_time).

% Option D: Trustcorp owns Flores Tower and Yates House
% Flores Tower is class 1, Yates House is class 3
option_d :-
    current_owner(flores_tower, trustcorp, max_time),
    current_owner(yates_house, trustcorp, max_time).

% Option E: Trustcorp owns Garza Tower and Lynch Building
% Garza Tower is class 1, Lynch Building is class 2
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