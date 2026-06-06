% Define companies
company(realprop).
company(southco).
company(trustcorp).

% Define buildings and their classes
building(garza_tower, 1).
building(yates_house, 3).
building(zimmer_house, 3).
building(flores_tower, 1).
building(lynch_building, 2).
building(king_building, 2).
building(meyer_building, 2).
building(ortiz_building, 2).

% Initial ownership
owns(realprop, garza_tower).
owns(realprop, yates_house).
owns(realprop, zimmer_house).
owns(southco, flores_tower).
owns(southco, lynch_building).
owns(trustcorp, king_building).
owns(trustcorp, meyer_building).
owns(trustcorp, ortiz_building).

% Time steps for planning
time(0..10).

% State: owns(Company, Building, Time)
owns(C, B, 0) :- owns(C, B).

% Choice: which trade to make at each time step
{ trade1(C1, B1, C2, B2, T) : owns(C1, B1, T), owns(C2, B2, T), C1 != C2, building(B1, Class), building(B2, Class) } 1 :- time(T), T > 0.
{ trade2(C1, B1, C2, B2a, C2, B2b, T) : owns(C1, B1, T), owns(C2, B2a, T), owns(C2, B2b, T), C1 != C2, B2a != B2b, building(B1, 1), building(B2a, 2), building(B2b, 2) } 1 :- time(T), T > 0.
{ trade3(C1, B1, C2, B2a, C2, B2b, T) : owns(C1, B1, T), owns(C2, B2a, T), owns(C2, B2b, T), C1 != C2, B2a != B2b, building(B1, 2), building(B2a, 3), building(B2b, 3) } 1 :- time(T), T > 0.

% Exactly one trade per time step
:- time(T), T > 0, 
   #count{ 1 : trade1(_,_,_,_,T); 1 : trade2(_,_,_,_,_,_,T); 1 : trade3(_,_,_,_,_,_,T) } != 1.

% Effects of trade1: swap buildings of same class
owns(C1, B2, T+1) :- trade1(C1, B1, C2, B2, T), time(T+1).
owns(C2, B1, T+1) :- trade1(C1, B1, C2, B2, T), time(T+1).
not owns(C1, B1, T+1) :- trade1(C1, B1, C2, B2, T), time(T+1).
not owns(C2, B2, T+1) :- trade1(C1, B1, C2, B2, T), time(T+1).

% Effects of trade2: C1 gives class1, gets two class2
owns(C1, B2a, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
owns(C1, B2b, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
owns(C2, B1, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C1, B1, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C2, B2a, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C2, B2b, T+1) :- trade2(C1, B1, C2, B2a, C2, B2b, T), time(T+1).

% Effects of trade3: C1 gives class2, gets two class3
owns(C1, B2a, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
owns(C1, B2b, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
owns(C2, B1, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C1, B1, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C2, B2a, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).
not owns(C2, B2b, T+1) :- trade3(C1, B1, C2, B2a, C2, B2b, T), time(T+1).

% Frame axiom: ownership persists if not changed
owns(C, B, T+1) :- owns(C, B, T), time(T+1), 
                   not trade1(C, B, _, _, T), 
                   not trade1(_, _, C, B, T),
                   not trade2(C, B, _, _, _, _, T),
                   not trade2(_, _, C, B, _, _, T),
                   not trade2(_, _, _, _, C, B, T),
                   not trade3(C, B, _, _, _, _, T),
                   not trade3(_, _, C, B, _, _, T),
                   not trade3(_, _, _, _, C, B, T).

% Check each option at final time
% Option A: RealProp owns Flores Tower and Garza Tower
option_a_possible :- time(T), owns(realprop, flores_tower, T), owns(realprop, garza_tower, T).

% Option B: Southco owns Flores Tower and Meyer Building
option_b_possible :- time(T), owns(southco, flores_tower, T), owns(southco, meyer_building, T).

% Option C: Southco owns Garza Tower and Lynch Building
option_c_possible :- time(T), owns(southco, garza_tower, T), owns(southco, lynch_building, T).

% Option D: Trustcorp owns Flores Tower and Ortiz Building
option_d_possible :- time(T), owns(trustcorp, flores_tower, T), owns(trustcorp, ortiz_building, T).

% Option E: Trustcorp owns Garza Tower and Meyer Building
option_e_possible :- time(T), owns(trustcorp, garza_tower, T), owns(trustcorp, meyer_building, T).

% The answer is the option that is NOT possible
option(a) :- not option_a_possible.
option(b) :- not option_b_possible.
option(c) :- not option_c_possible.
option(d) :- not option_d_possible.
option(e) :- not option_e_possible.

#show option/1.