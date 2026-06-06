#const max_time = 10.

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

% Trade actions:
% - trade_give(Building, Company, Time): Company gives up Building at Time
% - trade_receive(Building, Company, Time): Company receives Building at Time

% A company can give up a building at a time step
{ trade_give(Building, Company, T) : building(Building, _) } 1 :-
    company(Company),
    time(T),
    T < max_time.

% A company can receive a building at a time step
{ trade_receive(Building, Company, T) : building(Building, _) } 1 :-
    company(Company),
    time(T),
    T < max_time.

% Trade type 1: Trade one building for one other building of the same class
% If a company gives up a building of class C, it can receive another building of class C
trade_receive(OtherBuilding, Company, T) :-
    trade_give(Building, Company, T),
    building(Building, Class),
    building(OtherBuilding, Class),
    Building != OtherBuilding.

% Trade type 2: Trade one class 1 building for two class 2 buildings
% If a company gives up a class 1 building, it must receive two class 2 buildings
trade_receive(OtherBuilding1, Company, T) :-
    trade_give(Building, Company, T),
    building(Building, 1),
    building(OtherBuilding1, 2),
    time(T).
trade_receive(OtherBuilding2, Company, T) :-
    trade_give(Building, Company, T),
    building(Building, 1),
    building(OtherBuilding2, 2),
    OtherBuilding1 != OtherBuilding2,
    time(T).

% Trade type 3: Trade one class 2 building for two class 3 buildings
% If a company gives up a class 2 building, it must receive two class 3 buildings
trade_receive(OtherBuilding1, Company, T) :-
    trade_give(Building, Company, T),
    building(Building, 2),
    building(OtherBuilding1, 3),
    time(T).
trade_receive(OtherBuilding2, Company, T) :-
    trade_give(Building, Company, T),
    building(Building, 2),
    building(OtherBuilding2, 3),
    OtherBuilding1 != OtherBuilding2,
    time(T).

% Update ownership based on trades
% A building changes owner if it is given up by its current owner and received by another company
current_owner(Building, NewCompany, T+1) :-
    trade_give(Building, OldCompany, T),
    trade_receive(Building, NewCompany, T),
    OldCompany != NewCompany,
    building(Building, _),
    time(T),
    T < max_time.

% If a building is not traded, it stays with the same owner
current_owner(Building, Company, T+1) :-
    current_owner(Building, Company, T),
    not trade_give(Building, Company, T),
    building(Building, _),
    company(Company),
    time(T),
    T < max_time.

% Each company must own exactly 3 buildings at any time
:- company(C), time(T), #count{ B : current_owner(B, C, T) } != 3.

% Check each option for consistency with trade rules

% Option A: RealProp owns Lynch Building, Meyer Building, and Ortiz Building (all class 2)
option_a :-
    current_owner(lynch_building, realprop, max_time),
    current_owner(meyer_building, realprop, max_time),
    current_owner(ortiz_building, realprop, max_time).

% Option B: Southco owns Garza Tower (class 1) and Meyer Building (class 2)
option_b :-
    current_owner(garza_tower, southco, max_time),
    current_owner(meyer_building, southco, max_time).

% Option C: Southco owns King Building, Meyer Building, and Ortiz Building (all class 2)
option_c :-
    current_owner(king_building, southco, max_time),
    current_owner(meyer_building, southco, max_time),
    current_owner(ortiz_building, southco, max_time).

% Option D: Trustcorp owns Flores Tower (class 1) and Yates House (class 3)
option_d :-
    current_owner(flores_tower, trustcorp, max_time),
    current_owner(yates_house, trustcorp, max_time).

% Option E: Trustcorp owns Garza Tower (class 1) and Lynch Building (class 2)
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