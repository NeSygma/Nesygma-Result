% Companies
company(realprop).
company(southco).
company(trustcorp).

% Buildings and their classes
building(garza_tower, 1).
building(yates_house, 3).
building(zimmer_house, 3).
building(flores_tower, 1).
building(lynch_building, 2).
building(king_building, 2).
building(meyer_building, 2).
building(ortiz_building, 2).

% Initial ownership
owner(garza_tower, realprop, 0).
owner(yates_house, realprop, 0).
owner(zimmer_house, realprop, 0).
owner(flores_tower, southco, 0).
owner(lynch_building, southco, 0).
owner(king_building, trustcorp, 0).
owner(meyer_building, trustcorp, 0).
owner(ortiz_building, trustcorp, 0).

% Time steps for trading
max_trades(10).
time(0..max_trades).

% Choice rule: A trade occurs at each time step
% Trade types:
% 1: Trade one building for one building of the same class
% 2: Trade one class 1 building for two class 2 buildings
% 3: Trade one class 2 building for two class 3 buildings

% Trade type 1: One building for one building of the same class
1 { trade(T, B1, B2) : 
        owner(B1, C1, T), owner(B2, C2, T), 
        building(B1, Class), building(B2, Class),
        C1 != C2, time(T) } 1 :- time(T).

% Trade type 2: One class 1 building for two class 2 buildings
1 { trade(T, B1, B2, B3) : 
        owner(B1, C1, T), 
        building(B1, 1), building(B2, 2), building(B3, 2),
        C1 != trustcorp, time(T) } 1 :- time(T).

% Trade type 3: One class 2 building for two class 3 buildings
1 { trade(T, B1, B2, B3) : 
        owner(B1, C1, T), 
        building(B1, 2), building(B2, 3), building(B3, 3),
        C1 != trustcorp, time(T) } 1 :- time(T).

% Apply trades to update ownership
% Trade type 1: One building for one building of the same class
owner(B2, C2, T+1) :- trade(T, B1, B2), owner(B1, C1, T), owner(B2, C2, T), building(B1, Class), building(B2, Class), C1 != C2, time(T).
owner(B1, C1, T+1) :- owner(B1, C1, T), not trade(T, B1, _), not trade(T, _, B1), time(T).

% Trade type 2: One class 1 building for two class 2 buildings
owner(B2, trustcorp, T+1) :- trade(T, B1, B2, B3), owner(B1, C1, T), building(B1, 1), time(T).
owner(B3, trustcorp, T+1) :- trade(T, B1, B2, B3), owner(B1, C1, T), building(B1, 1), time(T).
owner(B1, C1, T+1) :- owner(B1, C1, T), not trade(T, B1, _, _), time(T).

% Trade type 3: One class 2 building for two class 3 buildings
owner(B2, trustcorp, T+1) :- trade(T, B1, B2, B3), owner(B1, C1, T), building(B1, 2), time(T).
owner(B3, trustcorp, T+1) :- trade(T, B1, B2, B3), owner(B1, C1, T), building(B1, 2), time(T).
owner(B1, C1, T+1) :- owner(B1, C1, T), not trade(T, B1, _, _), time(T).

% Persistence for other owners
owner(B, C, T+1) :- owner(B, C, T), not trade(T, B, _), not trade(T, B, _, _), not trade(T, _, B, _), not trade(T, _, _, B), time(T).

% Final state: Trustcorp owns no class 2 buildings
:- owner(B, trustcorp, T), building(B, 2), time(T).

% Answer choice (A): RealProp owns a class 1 building in the final state
answer_a :- owner(B, realprop, T), building(B, 1), time(T).

% Answer choice (B): Southco owns only class 2 buildings in the final state
% This means Southco owns no class 1 or class 3 buildings in the final state
answer_b :- time(T), not owner(B, southco, T) : building(B, 1).
answer_b :- time(T), not owner(B, southco, T) : building(B, 3).
answer_b :- time(T), owner(B, southco, T) : building(B, 2).

% Answer choice (C): Southco has made at least one trade with Trustcorp
% This is true if Southco owns a building that was originally Trustcorp's,
% or Trustcorp owns a building that was originally Southco's, in the final state
answer_c :- owner(B, southco, T), owner(B, trustcorp, 0), time(T).
answer_c :- owner(B, trustcorp, T), owner(B, southco, 0), time(T).

% Answer choice (D): Trustcorp owns the Garza Tower in the final state
answer_d :- owner(garza_tower, trustcorp, T), time(T).

% Answer choice (E): Trustcorp owns the Zimmer House in the final state
answer_e :- owner(zimmer_house, trustcorp, T), time(T).

% Map the correct answer to option/1 (MANDATORY)
% We need to ensure only one option is derived
option(a) :- answer_a, not answer_b, not answer_c, not answer_d, not answer_e.
option(b) :- answer_b, not answer_a, not answer_c, not answer_d, not answer_e.
option(c) :- answer_c, not answer_a, not answer_b, not answer_d, not answer_e.
option(d) :- answer_d, not answer_a, not answer_b, not answer_c, not answer_e.
option(e) :- answer_e, not answer_a, not answer_b, not answer_c, not answer_d.

#show option/1.