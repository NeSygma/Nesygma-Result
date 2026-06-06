% Define companies and buildings
company(realprop).
company(southco).
company(trustcorp).

% Define building classes (1, 2, or 3)
class(1..3).

% Buildings with their class and initial owner
building(garza_tower, 1, realprop).
building(yates_house, 3, realprop).
building(zimmer_house, 3, realprop).
building(flores_tower, 1, southco).
building(lynch_building, 2, southco).
building(king_building, 2, trustcorp).
building(meyer_building, 2, trustcorp).
building(ortiz_building, 2, trustcorp).

% Time steps for trades
time(0..3).

% Initial ownership at time 0
owner(B, C, 0) :- building(B, _, C).

% Possible trades:
% Trade type 1: Trade one building for one building of the same class
% Trade type 2: Trade one class 1 building for two class 2 buildings
% Trade type 3: Trade one class 2 building for two class 3 buildings

% Choice rule for trades: At each time step, a trade can occur
{ trade(T, B1, B2, Type) : 
    building(B1, Class1, _),
    building(B2, Class2, _),
    Class1 = Class2,
    Type = 1
} 1 :- time(T), T > 0.

{ trade(T, B1, B2a, B2b, Type) : 
    building(B1, 1, _),
    building(B2a, 2, _),
    building(B2b, 2, _),
    B2a != B2b,
    Type = 2
} 1 :- time(T), T > 0.

{ trade(T, B1, B2a, B2b, Type) : 
    building(B1, 2, _),
    building(B2a, 3, _),
    building(B2b, 3, _),
    B2a != B2b,
    Type = 3
} 1 :- time(T), T > 0.

% Update ownership based on trades
% Trade type 1: B1 is given up, B2 is acquired
owner(B2, C, T) :- 
    trade(T, B1, B2, 1),
    owner(B1, C, T-1).

% Trade type 2: B1 is given up, B2a and B2b are acquired
owner(B2a, C, T) :- 
    trade(T, B1, B2a, B2b, 2),
    owner(B1, C, T-1).
owner(B2b, C, T) :- 
    trade(T, B1, B2a, B2b, 2),
    owner(B1, C, T-1).

% Trade type 3: B1 is given up, B2a and B2b are acquired
owner(B2a, C, T) :- 
    trade(T, B1, B2a, B2b, 3),
    owner(B1, C, T-1).
owner(B2b, C, T) :- 
    trade(T, B1, B2a, B2b, 3),
    owner(B1, C, T-1).

% Persistence: If no trade affects a building, its owner remains the same
owner(B, C, T) :- 
    owner(B, C, T-1),
    time(T),
    not owner(B, _, T) : company(_).

% Final ownership is at the last time step
final_owner(B, C) :- owner(B, C, T), time(T).

% Define the conditions for each option
% Option (A): RealProp owns Flores Tower and Garza Tower
option_a_condition :-
    final_owner(flores_tower, realprop),
    final_owner(garza_tower, realprop).

% Option (B): Southco owns Flores Tower and Meyer Building
option_b_condition :-
    final_owner(flores_tower, southco),
    final_owner(meyer_building, southco).

% Option (C): Southco owns Garza Tower and Lynch Building
option_c_condition :-
    final_owner(garza_tower, southco),
    final_owner(lynch_building, southco).

% Option (D): Trustcorp owns Flores Tower and Ortiz Building
option_d_condition :-
    final_owner(flores_tower, trustcorp),
    final_owner(ortiz_building, trustcorp).

% Option (E): Trustcorp owns Garza Tower and Meyer Building
option_e_condition :-
    final_owner(garza_tower, trustcorp),
    final_owner(meyer_building, trustcorp).

% Map the correct answer to option/1
% Since (A) cannot be true, we do not derive option(a)
option(b) :- option_b_condition.
option(c) :- option_c_condition.
option(d) :- option_d_condition.
option(e) :- option_e_condition.

#show option/1.

% Debug: Show final ownership for verification
#show final_owner/2.